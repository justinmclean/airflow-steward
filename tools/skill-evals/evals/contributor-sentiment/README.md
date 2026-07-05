<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

# contributor-sentiment evals

Behavioral eval suite for the `contributor-sentiment` skill — 10 cases across 3 steps.

> **The numbers here are illustrative test values, not benchmarks.** These
> fixtures exercise the skill's mechanics; they say nothing about what a
> "good" project looks like. The gate's thresholds measure a project
> against its own baseline, are not comparable across communities, and
> different communities with very different numbers can both be healthy. A
> community is not just numbers. See
> [`docs/contributor-sentiment.md`](../../../../docs/contributor-sentiment.md#purpose)
> for the interpretive caveats before drawing any conclusion from a score.

## Steps covered

| Step | Cases | What is tested |
|---|---|---|
| `step-0-resolve-inputs` | 3 | Input resolution: standard 6-month window; new project with no baseline; explicit baseline override |
| `step-2-score-signals` | 4 | Signal scoring: healthy project (all pass); multi-signal decline (all fail); single tone regression; injection attempt in first-reply text |
| `step-3-generate-report` | 3 | Report structure: gate pass with full baseline; gate fail with notes; no-baseline snapshot-only output |

## Case inventory

### step-0-resolve-inputs

| Case | Scenario | Key assertion |
|---|---|---|
| `case-1-standard-window` | Default 6-month window, ASF project, baseline available | Dates computed correctly; `baseline_available: true`; `profile: asf` |
| `case-2-no-baseline-new-project` | 3-month window, project created after baseline start | `baseline_available: false`; note about pre-dating project creation |
| `case-3-explicit-baseline-override` | User supplies `baseline:YYYY-MM-DD..YYYY-MM-DD` argument | Baseline overridden; note about user-supplied override |

### step-2-score-signals

| Case | Scenario | Key assertion |
|---|---|---|
| `case-1-healthy-project` | All signals within thresholds | `overall_gate_pass: true`; all four `gate_pass: true` |
| `case-2-declining-retention` | All four signals fail threshold | `overall_gate_pass: false`; all four `gate_pass: false`; four entries in `gate_notes` |
| `case-3-tone-regression` | Only thread tone fails (delta_pp = 8.4 > 5) | `overall_gate_pass: false`; tone `gate_pass: false`; other three pass; one `gate_notes` entry |
| `case-4-injection-in-reply` | Injection attempt in one first-reply text; excluded from sample | `injection_attempts_found: 1`; injected item excluded from tone scoring; gate fails due to remaining dismissive fraction |

### step-3-generate-report

| Case | Scenario | Key assertion |
|---|---|---|
| `case-1-gate-pass` | All signals pass; full baseline available | `gate_pass: true`; `save_offered: true`; `gate_notes: []` |
| `case-2-gate-fail` | All signals fail; full baseline available | `gate_pass: false`; four entries in `gate_notes`; `save_offered: true` |
| `case-3-no-baseline` | New project; no baseline comparison available | `baseline_available: false`; all deltas `null`; `gate_pass: true` with note; `save_offered: true` |
