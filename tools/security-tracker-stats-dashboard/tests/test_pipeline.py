# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# SPDX-License-Identifier: Apache-2.0
"""Integration tests: run render.py as a subprocess with fixture data."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

TOOL_DIR = Path(__file__).parent.parent
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture()
def cache_dir(tmp_path):
    """Populate a temp cache dir from the fixture data."""
    shutil.copytree(str(FIXTURES_DIR), str(tmp_path / "cache"))
    return tmp_path / "cache"


@pytest.fixture()
def output_html(tmp_path):
    return tmp_path / "dashboard.html"


def _run_render(cache_dir, output_html, extra_env=None):
    env = os.environ.copy()
    env["TRACKER_STATS_CACHE"] = str(cache_dir)
    env["TRACKER_STATS_OUT"] = str(output_html)
    env["TRACKER_STATS_CONFIG"] = str(FIXTURES_DIR / "test-config.yaml")
    # Use PYTHONPATH so render.py can find _render_helpers.py in its own dir.
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = str(TOOL_DIR) + ((":" + existing) if existing else "")
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, str(TOOL_DIR / "render.py")],
        capture_output=True,
        text=True,
        env=env,
    )


class TestRenderPipeline:
    def test_render_exits_zero(self, cache_dir, output_html):
        result = _run_render(cache_dir, output_html)
        assert result.returncode == 0, f"render.py failed:\n{result.stderr}"

    def test_html_file_created(self, cache_dir, output_html):
        _run_render(cache_dir, output_html)
        assert output_html.exists(), "HTML output file was not created"

    def test_html_is_not_empty(self, cache_dir, output_html):
        _run_render(cache_dir, output_html)
        assert output_html.stat().st_size > 0

    def test_html_contains_doctype(self, cache_dir, output_html):
        _run_render(cache_dir, output_html)
        html = output_html.read_text()
        assert html.lstrip().startswith("<!DOCTYPE html>")

    def test_html_contains_plotly(self, cache_dir, output_html):
        _run_render(cache_dir, output_html)
        html = output_html.read_text()
        assert "plotly" in html.lower()

    def test_html_contains_bucket_labels(self, cache_dir, output_html):
        result = _run_render(cache_dir, output_html)
        html = output_html.read_text()
        # The fixture issues span Jan–Mar 2026; labels must appear in the JS.
        assert "2026-01" in html

    def test_render_without_upstream_repo_omits_pr_charts(self, cache_dir, output_html):
        result = _run_render(cache_dir, output_html)
        html = output_html.read_text()
        # With upstream_repo=null the c_prc/c_prm/c_rel div IDs should be absent.
        assert "c_prc" not in html
        assert "c_prm" not in html
        assert "c_rel" not in html

    def test_quarterly_mode(self, cache_dir, output_html, tmp_path):
        """Verify render works with quarterly bucket mode."""
        # Write a quarterly overlay config
        overlay = tmp_path / "quarterly.yaml"
        overlay.write_text("upstream_repo: null\nbuckets: quarterly\nstart: '2026-Q1'\nmilestones: []\n")
        env = {"TRACKER_STATS_CONFIG": str(overlay)}
        result = _run_render(cache_dir, output_html, extra_env=env)
        assert result.returncode == 0, f"quarterly render failed:\n{result.stderr}"
        html = output_html.read_text()
        assert "2026-Q" in html

    def test_stdout_reports_bucket_count(self, cache_dir, output_html):
        result = _run_render(cache_dir, output_html)
        assert "buckets in range" in result.stdout

    def test_stdout_reports_total_trackers(self, cache_dir, output_html):
        result = _run_render(cache_dir, output_html)
        assert "total trackers: 3" in result.stdout

    def test_render_is_readonly(self, cache_dir, output_html):
        """Render must not modify the cache directory."""
        before = {p: p.stat().st_mtime for p in cache_dir.rglob("*") if p.is_file()}
        _run_render(cache_dir, output_html)
        after = {p: p.stat().st_mtime for p in cache_dir.rglob("*") if p.is_file()}
        # No existing file should be modified (new files must not appear either).
        assert before.keys() == after.keys(), "render.py wrote new files into the cache dir"
        for path in before:
            assert before[path] == after[path], f"render.py modified cached file: {path}"


class TestFetchEventsHelper:
    """Test the fetch_events.fetch_one logic via a direct import."""

    def test_fetch_one_skips_cached_file(self, cache_dir, tmp_path):
        """fetch_one should return (n, True, 'cached') when the file exists."""
        sys.path.insert(0, str(TOOL_DIR))
        import importlib
        import io

        # Patch the environment before the module-level code in fetch_events runs.
        old_env = os.environ.copy()
        os.environ["TRACKER_STATS_CACHE"] = str(cache_dir)
        os.environ["TRACKER_STATS_REPO"] = "test/test"
        try:
            # fetch_events has module-level code that reads issues.json;
            # ensure it's importable with our fixture.
            import fetch_events  # noqa: F401
            importlib.reload(fetch_events)
            n = 1  # event file for issue 1 exists in fixtures
            result = fetch_events.fetch_one(n)
            assert result == (1, True, "cached")
        finally:
            os.environ.clear()
            os.environ.update(old_env)
            sys.path.pop(0)
            if "fetch_events" in sys.modules:
                del sys.modules["fetch_events"]
