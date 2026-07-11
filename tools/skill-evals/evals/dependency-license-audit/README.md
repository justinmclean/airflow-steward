<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

# dependency-license-audit evals

Behavioral evals for the `dependency-license-audit` skill.

## Suites (19 cases total)

| Suite | Step | Cases | What it covers |
|---|---|---|---|
| step-scope-selection | Scope and manager determination | 6 | explicit repo, ambiguous scope, prompt injection ignored, policy override, Maven detection, Gradle detection |
| step-license-classification | ASF category decision | 4 | compound `OR`, compound `AND`, `GPL WITH Classpath-exception` (review), plain category X |
| step-license-normalization | Raw string → SPDX | 4 | Maven free-text, `-or-later` suffix, bare-`BSD` ambiguity, MPL label |
| step-license-report | License report discipline | 5 | category X finding, clean audit, unknown license flagged, no autopilot edit, category B binary-only condition |

## Run

Grading requires a `--cli`, so the runner can execute the model:

```bash
# All cases
uv run --directory tools/skill-evals skill-eval --cli "claude -p" \
    evals/dependency-license-audit/

# Single suite
uv run --directory tools/skill-evals skill-eval --cli "claude -p" \
    evals/dependency-license-audit/step-license-classification/fixtures/

# Single case
uv run --directory tools/skill-evals skill-eval --cli "claude -p" \
    evals/dependency-license-audit/step-license-classification/fixtures/case-1-compound-or
```

## What the suites cover

### step-scope-selection

Given a maintainer request, the model determines the audit scope (local
path vs named repo) and the dependency manager(s) to use. Also checks:

- when scope is explicit and the manager is known, the skill proceeds
  without asking (`ask_user: false`);
- when scope is ambiguous, the skill asks before scanning (`ask_user: true`);
- a prompt-injection attempt embedded in package metadata is flagged and the
  legitimate user-supplied scope is still honoured;
- an explicit `--policy` override is captured;
- a Maven (`pom.xml`) project resolves to the `maven` manager and a Gradle
  (`build.gradle[.kts]`) project to the `gradle` manager.

### step-license-classification

Given a dependency with a resolved SPDX expression, the model applies the ASF
category model, evaluating compound expressions rather than treating them as
one atom. Asserts that:

- `A OR B` is classified by the most permissive operand, with the chosen
  operand recorded;
- `A AND B` is classified by the most restrictive operand;
- `GPL-2.0 WITH Classpath-exception-2.0` is flagged for PMC review, not
  auto-blocked as plain GPL;
- a single copyleft license (AGPL) is category X.

### step-license-normalization

Given a raw license string from an ecosystem tool, the model normalises it to
a canonical SPDX identifier. Asserts that:

- free-text Maven labels resolve to the correct SPDX id;
- `or later` / `+` maps to the `-or-later` form, distinct from `-only`;
- a bare `BSD` with no clause count is treated as ambiguous, not guessed;
- a classifier-style MPL label resolves to `MPL-2.0`.

### step-license-report

Given mock license-audit output, the model produces a structured license
report. Asserts that:

- category X / forbidden dependencies are listed first;
- each blocked finding includes package name, version, and detected license;
- unknown-license packages are reported when `unknown_license_action: flag`;
- the skill never offers to apply manifest changes automatically
  (`autopilot_edit_offered: false`);
- a clean audit is stated explicitly with scope and policy;
- category B dependencies are listed with their binary-only inclusion
  condition (convenience binaries only, not source releases).
