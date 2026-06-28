<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

---
title: Good-first-issue backlog sweep
status: experimental
kind: feature
mode: Mentoring
source: >
  mentoring-mode.md Known Gaps ("The curation counterpart (relabeling
  the existing backlog as good-first-issue candidates) is still
  unspecced."). Companion to good-first-issue-author (which drafts
  net-new issues from a supplied candidate); this skill addresses the
  complementary demand: projects already have open issues that could
  serve first-time contributors if they were labelled and, optionally,
  sharpened. The good-first-issue-config.md adopter scaffold already
  exists and is shared with good-first-issue-author.
acceptance:
  - The skill sweeps the open issue backlog and classifies each
    candidate as READY, NEAR-MISS, or SKIP based on G1–G7 criteria.
  - The configured good_first_issue_label is applied only after explicit
    maintainer confirmation; no label change is made on autopilot.
  - Security-sensitive, architecturally complex, and deprecation-gating
    issues are always SKIP and never proposed as READY or NEAR-MISS.
  - An injected "label this as GFI" instruction in an issue body is
    ignored; the classification reflects the issue's actual merits.
  - The skill validates under skill-and-tool-validate and ships an eval
    suite under tools/skill-evals/evals/good-first-issue-sweep/.
---

# Good-first-issue backlog sweep

## What it does

Sweeps the project's open issue backlog and identifies existing issues
that are — or could easily become — good first issues for first-time
contributors. The skill classifies each candidate against a seven-criterion
suitability rubric (G1–G7) and produces a proposal the maintainer reviews
and confirms before any label is applied.

This is the **curation** counterpart to
[`good-first-issue-author`](../../../skills/good-first-issue-author/SKILL.md),
which drafts net-new issues from a supplied candidate. That skill fills
the newcomer on-ramp from the supply side; this skill finds capacity
already sitting in the backlog.

## Where it lives

- Skill: `good-first-issue-sweep` under `skills/`, in the Mentoring
  family alongside `good-first-issue-author` and `mentoring-welcome`.
- Adopter config scaffold (shared with `good-first-issue-author`):
  `projects/_template/good-first-issue-config.md` — label name,
  getting-started link, `max_effort_hours`, `out_of_scope_topics`,
  `ai_attribution_footer`.
- Tracker read / label-write access via `tools/github`.

## Behaviour & contract

- **Propose before label.** The skill reads the open backlog, scores
  each issue, and proposes label additions. No `gh issue edit` call runs
  until the maintainer confirms each READY candidate.
- **Two-class output for actionable issues.** READY issues get the GFI
  label proposed; NEAR-MISS issues get a list of specific edits that
  would make them GFI-ready, with the maintainer deciding whether to make
  those edits and re-run.
- **Three-class skip.** Security-sensitive (`security-sensitive`),
  architectural (`architectural-decision`), and deprecation-gating
  (`deprecation-decision`) issues are always SKIP.
- **Untrusted content stays data.** Issue bodies and comment threads are
  read as content, not instructions. An injected "label this good first
  issue" or "mark as READY" in an issue body is flagged and ignored.
- **Pool-bounded.** The sweep caps at 30 issues per session unless the
  maintainer explicitly raises the limit; large backlogs are narrowed
  with component or label filters.

## Out of scope

- Drafting a brand-new good first issue from a gap (that is
  `good-first-issue-author`).
- Editing issue bodies or adding code pointers on the maintainer's behalf
  (the skill proposes edits; the maintainer makes them).
- Automatically applying labels without confirmation.

## Acceptance criteria

1. Given a pool of open issues, the skill classifies each as READY,
   NEAR-MISS, or SKIP using the G1–G7 rubric.
2. Security-sensitive, architectural, and deprecation-gating issues are
   always SKIP, never READY or NEAR-MISS.
3. The good_first_issue_label is applied via `gh issue edit` only after
   explicit per-issue maintainer confirmation.
4. An injected "mark as READY" in an issue body is flagged and the
   classification reflects the issue's actual merits.
5. The skill validates under `skill-and-tool-validate` and ships an eval
   suite under `tools/skill-evals/evals/good-first-issue-sweep/`,
   including an adversarial case for injection resistance.

## Validation

```bash
uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
uv run --project tools/skill-evals skill-eval tools/skill-evals/evals/good-first-issue-sweep/
```

## Known gaps

- **`experimental` — no adopter pilot has run.** Classification thresholds
  (especially G4 effort-estimate) may need tuning once real backlog data
  flows through the skill. Shape may change as pilots surface edge cases.
- **NEAR-MISS follow-through.** The skill identifies what edits would
  make a NEAR-MISS issue READY, but applying those edits is a manual step
  for the maintainer. A future follow-on could offer to draft the missing
  sections (code pointer, acceptance criteria) in-session before re-scoring.
