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
"""Replay-mode eval — drives `classify_response` end-to-end against a
canned GraphQL response fixture, asserts the full per-issue
classification AND the bucket distribution.

The fixture
(`fixtures/synthetic_workspace_sweep.json`) is purpose-built to
exercise every rule in `bulk-mode.md` § Pre-flight no-op
classifier — one issue per rule path, plus a fall-through and a
bot-login-detection case. Each issue's `_purpose` field documents
which rule it should land on.

This is the eval-fixture pattern the README points at: a rule
change that alters the distribution will fail one of the asserts
below; the diff in the failing assertion tells the reviewer how
the rule affects coverage before they look at any real adopter
data. The eval is **deterministic** — every timestamp is relative
to a pinned `now` value below.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from preflight_audit.classifier import Decision, classify_response

# Pinned `now` — every fixture timestamp is computed relative to this
# moment. Shifting it requires rebuilding the fixture in lock-step.
NOW = datetime(2026, 6, 1, 12, 0, 0, tzinfo=UTC)

FIXTURE = Path(__file__).parent / "fixtures" / "synthetic_workspace_sweep.json"


@pytest.fixture(scope="module")
def response() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_synthetic_sweep_breakdown_no_extra_bots(response: dict) -> None:
    """Without `--bot-logins` overrides, the synthetic sweep should
    skip 6 of 12 trackers and dispatch the rest (one urgent)."""
    classifications = classify_response(response, now=NOW)
    by_decision: dict[Decision, list[int]] = {}
    for c in classifications:
        by_decision.setdefault(c.decision, []).append(c.issue.number)
    for d in by_decision.values():
        d.sort()

    assert by_decision.get(Decision.SKIP_NOOP, []) == [101, 103, 104, 105, 106, 107, 108]
    assert by_decision.get(Decision.DISPATCH_URGENT, []) == [102]
    assert by_decision.get(Decision.DISPATCH, []) == [100, 109, 110, 111]


def test_synthetic_sweep_breakdown_with_extra_bot(response: dict) -> None:
    """Adding `company-private-bot` to the override moves #109 from
    `dispatch` to `skip-noop` (Rule 7 fires once the personal-bot
    is recognised as bot-equivalent)."""
    classifications = classify_response(
        response, now=NOW, extra_bot_logins=frozenset({"company-private-bot"})
    )
    decisions = {c.issue.number: c.decision for c in classifications}
    assert decisions[109] == Decision.SKIP_NOOP
    # Other classifications stay put.
    assert decisions[100] == Decision.DISPATCH
    assert decisions[102] == Decision.DISPATCH_URGENT
    assert decisions[103] == Decision.SKIP_NOOP


def test_synthetic_sweep_each_issue_lands_in_documented_bucket(response: dict) -> None:
    """Per-issue assertions matching the `_purpose` annotation each
    fixture entry carries. Keeps the fixture documentation in
    lock-step with the rule behaviour."""
    classifications = classify_response(response, now=NOW)
    by_number = {c.issue.number: c for c in classifications}

    # Rule 1 dispatch (recent human activity).
    assert by_number[100].decision == Decision.DISPATCH
    assert "recent human activity" in by_number[100].reason

    # Rule 1 yields → Rule 7 fires.
    assert by_number[101].decision == Decision.SKIP_NOOP
    assert "awaiting advisory" in by_number[101].reason

    # Rule 2 dispatch-urgent.
    assert by_number[102].decision == Decision.DISPATCH_URGENT
    assert "reporter" in by_number[102].reason

    # Rule 3 — post-announce.
    assert by_number[103].decision == Decision.SKIP_NOOP
    assert "post-announce" in by_number[103].reason

    # Rule 4 — stale closed.
    assert by_number[104].decision == Decision.SKIP_NOOP
    assert "stale closed" in by_number[104].reason

    # Rule 5 — all phases done.
    assert by_number[105].decision == Decision.SKIP_NOOP
    assert "all phases done" in by_number[105].reason

    # Rule 6 — awaiting release.
    assert by_number[106].decision == Decision.SKIP_NOOP
    assert "awaiting release" in by_number[106].reason

    # Rule 7 — awaiting advisory.
    assert by_number[107].decision == Decision.SKIP_NOOP
    assert "awaiting advisory" in by_number[107].reason

    # Bot login detection (Rule 7).
    assert by_number[108].decision == Decision.SKIP_NOOP
    assert by_number[108].last_is_skill_or_bot is True

    # Personal-account bot — without override, dispatches.
    assert by_number[109].decision == Decision.DISPATCH
    assert by_number[109].last_is_skill_or_bot is False

    # Fall-through dispatch.
    assert by_number[110].decision == Decision.DISPATCH

    # Recently-closed non-skill comment — dispatches (Rule 1 catches recent updatedAt).
    assert by_number[111].decision == Decision.DISPATCH


def test_skip_rate_meets_target(response: dict) -> None:
    """Assert the fixture sees a skip-rate ≥30%, matching the
    real-world target after the v2 rule tuning. If a rule edit
    pushes the rate below this, either the rule needs reviewing
    or the fixture needs an extra positive case for the
    relaxation."""
    classifications = classify_response(response, now=NOW)
    skips = sum(1 for c in classifications if c.decision == Decision.SKIP_NOOP)
    rate = skips / len(classifications)
    assert rate >= 0.30, f"skip-rate {rate:.0%} below 30% target"
