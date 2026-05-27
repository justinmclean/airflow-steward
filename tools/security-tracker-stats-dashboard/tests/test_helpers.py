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
"""Unit tests for pure helper functions in _render_helpers."""

import sys
import os
import datetime as dt

import pytest

# Make the tool root importable when pytest is run from the project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from _render_helpers import (
    _minimal_yaml_load,
    deep_merge,
    parse_dt,
    month_of,
    quarter_of,
    month_label,
    quarter_label,
    month_end,
    quarter_end,
    iter_months,
    iter_quarters,
    mean_or_none,
    js_array,
    js_quotes,
    milestone_x,
    eval_predicate,
    is_bot_body,
)


# ---------------------------------------------------------------------------
# _minimal_yaml_load
# ---------------------------------------------------------------------------

class TestMinimalYamlLoad:
    def test_simple_mapping(self):
        r = _minimal_yaml_load("a: 1\nb: hello\n")
        assert r == {"a": 1, "b": "hello"}

    def test_nested_mapping(self):
        r = _minimal_yaml_load("outer:\n  inner: 42\n")
        assert r == {"outer": {"inner": 42}}

    def test_block_sequence(self):
        r = _minimal_yaml_load("items:\n  - alpha\n  - beta\n")
        assert r["items"] == ["alpha", "beta"]

    def test_inline_flow_list(self):
        r = _minimal_yaml_load("tags: [a, b, c]\n")
        assert r["tags"] == ["a", "b", "c"]

    def test_null_values(self):
        r = _minimal_yaml_load("x: null\ny: ~\n")
        assert r["x"] is None
        assert r["y"] is None

    def test_booleans(self):
        r = _minimal_yaml_load("yes: true\nno: false\n")
        assert r["yes"] is True
        assert r["no"] is False

    def test_comment_stripping(self):
        r = _minimal_yaml_load("a: 1  # a comment\nb: 2\n")
        assert r == {"a": 1, "b": 2}

    def test_quoted_string_with_colon(self):
        r = _minimal_yaml_load('key: "host: 8080"\n')
        assert r["key"] == "host: 8080"

    def test_sequence_of_mappings(self):
        yaml = "cats:\n  - name: foo\n    color: red\n  - name: bar\n    color: blue\n"
        r = _minimal_yaml_load(yaml)
        assert r["cats"] == [{"name": "foo", "color": "red"}, {"name": "bar", "color": "blue"}]

    def test_integer_and_float(self):
        r = _minimal_yaml_load("count: 7\nrate: 3.14\n")
        assert r["count"] == 7
        assert r["rate"] == pytest.approx(3.14)

    def test_empty_flow_list(self):
        r = _minimal_yaml_load("items: []\n")
        assert r["items"] == []


# ---------------------------------------------------------------------------
# deep_merge
# ---------------------------------------------------------------------------

class TestDeepMerge:
    def test_simple_overlay(self):
        base = {"a": 1, "b": 2}
        overlay = {"b": 99, "c": 3}
        assert deep_merge(base, overlay) == {"a": 1, "b": 99, "c": 3}

    def test_nested_merge(self):
        base = {"x": {"a": 1, "b": 2}}
        overlay = {"x": {"b": 99}}
        result = deep_merge(base, overlay)
        assert result["x"] == {"a": 1, "b": 99}

    def test_list_replaced(self):
        base = {"items": [1, 2, 3]}
        overlay = {"items": [4, 5]}
        result = deep_merge(base, overlay)
        assert result["items"] == [4, 5]

    def test_none_overlay_returns_base(self):
        base = {"a": 1}
        assert deep_merge(base, None) == base

    def test_non_dict_overlay_replaces(self):
        assert deep_merge({"a": 1}, "scalar") == "scalar"


# ---------------------------------------------------------------------------
# parse_dt
# ---------------------------------------------------------------------------

class TestParseDt:
    def test_none_input(self):
        assert parse_dt(None) is None

    def test_empty_string(self):
        assert parse_dt("") is None

    def test_utc_z_suffix(self):
        d = parse_dt("2026-05-01T12:00:00Z")
        assert d.year == 2026
        assert d.month == 5
        assert d.tzinfo is not None

    def test_offset_suffix(self):
        d = parse_dt("2026-05-01T12:00:00+00:00")
        assert d.hour == 12


# ---------------------------------------------------------------------------
# Bucket functions
# ---------------------------------------------------------------------------

class TestMonthFunctions:
    def test_month_of(self):
        d = dt.datetime(2026, 5, 15, tzinfo=dt.timezone.utc)
        assert month_of(d) == (2026, 5)

    def test_quarter_of_q1(self):
        d = dt.datetime(2026, 2, 1, tzinfo=dt.timezone.utc)
        assert quarter_of(d) == (2026, 1)

    def test_quarter_of_q4(self):
        d = dt.datetime(2026, 11, 1, tzinfo=dt.timezone.utc)
        assert quarter_of(d) == (2026, 4)

    def test_month_label(self):
        assert month_label(2026, 3) == "2026-03"
        assert month_label(2026, 12) == "2026-12"

    def test_quarter_label(self):
        assert quarter_label(2026, 2) == "2026-Q2"

    def test_month_end_february_leap(self):
        end = month_end(2024, 2)
        assert end.day == 29
        assert end.hour == 23

    def test_month_end_february_non_leap(self):
        end = month_end(2026, 2)
        assert end.day == 28

    def test_quarter_end_q1(self):
        end = quarter_end(2026, 1)
        assert end.month == 3
        assert end.day == 31

    def test_quarter_end_q4(self):
        end = quarter_end(2026, 4)
        assert end.month == 12
        assert end.day == 31


class TestIterBuckets:
    def test_iter_months_range(self):
        result = list(iter_months(2026, 1, 2026, 3))
        assert result == [(2026, 1), (2026, 2), (2026, 3)]

    def test_iter_months_year_boundary(self):
        result = list(iter_months(2025, 11, 2026, 2))
        assert result == [(2025, 11), (2025, 12), (2026, 1), (2026, 2)]

    def test_iter_quarters_range(self):
        result = list(iter_quarters(2025, 4, 2026, 2))
        assert result == [(2025, 4), (2026, 1), (2026, 2)]

    def test_iter_months_single(self):
        assert list(iter_months(2026, 5, 2026, 5)) == [(2026, 5)]


# ---------------------------------------------------------------------------
# mean_or_none
# ---------------------------------------------------------------------------

class TestMeanOrNone:
    def test_empty_returns_none(self):
        assert mean_or_none([]) is None

    def test_single_value(self):
        assert mean_or_none([10.0]) == 10.0

    def test_multiple_values(self):
        assert mean_or_none([1.0, 2.0, 3.0]) == 2.0

    def test_rounding(self):
        assert mean_or_none([1.0, 2.0]) == 1.5


# ---------------------------------------------------------------------------
# js_array / js_quotes
# ---------------------------------------------------------------------------

class TestJsArray:
    def test_integers(self):
        assert js_array([1, 2, 3]) == "[1, 2, 3]"

    def test_none_values(self):
        assert js_array([1, None, 3]) == "[1, null, 3]"

    def test_float_with_fractional(self):
        result = js_array([1.5])
        assert result == "[1.50]"

    def test_float_whole_number(self):
        result = js_array([2.0])
        assert result == "[2]"

    def test_custom_null(self):
        assert js_array([None], fmt_null="undefined") == "[undefined]"

    def test_empty(self):
        assert js_array([]) == "[]"


class TestJsQuotes:
    def test_strings(self):
        assert js_quotes(["a", "b"]) == '["a", "b"]'

    def test_empty(self):
        assert js_quotes([]) == "[]"


# ---------------------------------------------------------------------------
# milestone_x
# ---------------------------------------------------------------------------

class TestMilestoneX:
    def test_monthly_mode(self):
        assert milestone_x("2026-04-20", "monthly") == "2026-04"

    def test_quarterly_mode_q1(self):
        assert milestone_x("2026-02-15", "quarterly") == "2026-Q1"

    def test_quarterly_mode_q4(self):
        assert milestone_x("2026-10-01", "quarterly") == "2026-Q4"

    def test_default_is_monthly(self):
        assert milestone_x("2026-06-01") == "2026-06"


# ---------------------------------------------------------------------------
# eval_predicate
# ---------------------------------------------------------------------------

class TestEvalPredicate:
    def _ctx(self, labels=None, is_open=True, state_reason=None, pr_merged=False):
        return {
            "labels": set(labels or []),
            "is_open": is_open,
            "state_reason": state_reason,
            "pr_merged_by_snapshot": pr_merged,
        }

    def test_state_open_matches(self):
        assert eval_predicate({"state": "open"}, self._ctx(is_open=True))

    def test_state_open_no_match(self):
        assert not eval_predicate({"state": "open"}, self._ctx(is_open=False))

    def test_state_closed_matches(self):
        assert eval_predicate({"state": "closed"}, self._ctx(is_open=False))

    def test_any_label_match(self):
        ctx = self._ctx(labels=["airflow", "bug"])
        assert eval_predicate({"any_label": ["airflow"]}, ctx)

    def test_any_label_no_match(self):
        ctx = self._ctx(labels=["bug"])
        assert not eval_predicate({"any_label": ["airflow"]}, ctx)

    def test_not_label_blocks(self):
        ctx = self._ctx(labels=["fix released"])
        assert not eval_predicate({"not_label": "fix released"}, ctx)

    def test_not_label_passes(self):
        ctx = self._ctx(labels=["airflow"])
        assert eval_predicate({"not_label": "fix released"}, ctx)

    def test_all_labels_match(self):
        ctx = self._ctx(labels=["a", "b", "c"])
        assert eval_predicate({"all_labels": ["a", "b"]}, ctx)

    def test_all_labels_no_match(self):
        ctx = self._ctx(labels=["a"])
        assert not eval_predicate({"all_labels": ["a", "b"]}, ctx)

    def test_not_any_label(self):
        ctx = self._ctx(labels=["a"])
        assert not eval_predicate({"not_any_label": ["a", "b"]}, ctx)

    def test_pr_merged_by_snapshot_true(self):
        ctx = self._ctx(pr_merged=True)
        assert eval_predicate({"pr_merged_by_snapshot": True}, ctx)

    def test_pr_merged_by_snapshot_false(self):
        ctx = self._ctx(pr_merged=False)
        assert not eval_predicate({"pr_merged_by_snapshot": True}, ctx)

    def test_state_reason_match(self):
        ctx = self._ctx(state_reason="COMPLETED", is_open=False)
        assert eval_predicate({"state_reason": "COMPLETED"}, ctx)

    def test_state_reason_no_match(self):
        ctx = self._ctx(state_reason="NOT_PLANNED", is_open=False)
        assert not eval_predicate({"state_reason": "COMPLETED"}, ctx)

    def test_all_of_dict_both_match(self):
        ctx = self._ctx(is_open=True, labels=["needs triage"])
        pred = {"all_of": {"state": "open", "any_label": ["needs triage"]}}
        assert eval_predicate(pred, ctx)

    def test_all_of_dict_partial_match(self):
        ctx = self._ctx(is_open=False)
        pred = {"all_of": {"state": "open", "any_label": ["needs triage"]}}
        assert not eval_predicate(pred, ctx)

    def test_any_of(self):
        ctx = self._ctx(is_open=True)
        pred = {"any_of": [{"state": "open"}, {"state": "closed"}]}
        assert eval_predicate(pred, ctx)

    def test_no_scope_label_true_when_no_scope(self):
        ctx = self._ctx(labels=["bug"])
        scope = {"airflow"}
        assert eval_predicate({"no_scope_label": True}, ctx, scope_labels=scope)

    def test_no_scope_label_false_when_has_scope(self):
        ctx = self._ctx(labels=["airflow"])
        scope = {"airflow"}
        assert not eval_predicate({"no_scope_label": True}, ctx, scope_labels=scope)

    def test_has_scope_label_true_when_has_scope(self):
        ctx = self._ctx(labels=["airflow"])
        scope = {"airflow"}
        assert eval_predicate({"has_scope_label": True}, ctx, scope_labels=scope)

    def test_unknown_key_returns_false(self):
        ctx = self._ctx()
        assert not eval_predicate({"unknown_key": "value"}, ctx)

    def test_empty_predicate_matches_all(self):
        ctx = self._ctx()
        assert eval_predicate({}, ctx)

    def test_non_dict_predicate_returns_false(self):
        ctx = self._ctx()
        assert not eval_predicate("invalid", ctx)


# ---------------------------------------------------------------------------
# is_bot_body
# ---------------------------------------------------------------------------

class TestIsBotBody:
    def test_empty_body(self):
        assert not is_bot_body("", ("<!-- bot",))

    def test_none_body(self):
        assert not is_bot_body(None, ("<!-- bot",))

    def test_matching_prefix(self):
        assert is_bot_body("<!-- airflow-s status rollup v1 -->", ("<!-- airflow-s status rollup v",))

    def test_non_matching_prefix(self):
        assert not is_bot_body("Human comment here", ("<!-- bot",))

    def test_no_prefixes(self):
        assert not is_bot_body("<!-- bot comment -->", ())

    def test_leading_whitespace_stripped(self):
        assert is_bot_body("  <!-- bot -->", ("<!-- bot",))
