<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

# Implementation Plan — spec-loop

Maintained by the loop's **plan** mode. It is the prioritised list of
*gaps* found by comparing [`specs/`](specs/) against the actual code
(`.claude/skills/`, `tools/`, `docs/`). The **build** mode takes the
single highest-priority work item, isolates it on its own branch,
implements it, validates it, and commits — **one work item, one branch,
one PR** (the branch-per-feature constraint).

> Priority lives here, not in the specs. The specs describe functional
> areas (unordered); this plan orders the work.

---

## What's been built

- **Spec set** — [`specs/`](specs/): an `overview` plus a functional
  spec per area (the four live modes, the security lifecycle, the
  release-management lifecycle (proposed), the privacy-LLM gate, the
  sandbox, CVE tooling, adoption/setup, adapters, project-agnosticism,
  and meta/quality tooling).
- **Loop scaffolding** — `loop.sh` (plan / build / consolidate; a branch
  per work item; never pushes), `PROMPT_plan.md`, `PROMPT_build.md`,
  `PROMPT_consolidate.md`, `AGENTS.md` (loop-scoped operational context),
  and this plan. Branch-collision guard is inline in `loop.sh`.
- **Pairing — both skills shipped** — `pairing-self-review` and
  `pairing-multi-agent-review` (three independent axis passes; eval
  suites present); `docs/modes.md` Pairing row reflects 2 skills /
  `experimental`. Spec: [`specs/pairing-mode.md`](specs/pairing-mode.md).
- **Mentoring — both skills shipped** — `pr-management-mentor` and
  `good-first-issue-author` (eval suites present); `docs/modes.md`
  Mentoring row reflects 2 skills / `experimental`.
  Spec: [`specs/mentoring-mode.md`](specs/mentoring-mode.md).
- **Contributor skills** — `contributor-nomination`,
  `contributor-activity-sweep`, and `committer-onboarding` shipped with
  eval suites. Formerly tracked under draft PRs #227–#229.
- **Drafting — issue-fix-workflow and audit-finding-fix skills** —
  both shipped with eval suites (covers generic drafting from triaged
  issues and audit findings, formerly tracked as `generic-drafting` /
  #296). Spec: [`specs/drafting-mode.md`](specs/drafting-mode.md).
- **Docs — mode economics page** — `docs/mode-economics.md` exists
  (per-mode token-cost shape, vendor-neutral).
- **Meta — spec-status index** — `tools/spec-status-index/` exists as a
  `uv` tool that prints specs grouped by status.
  Spec: [`specs/meta-and-quality-tooling.md`](specs/meta-and-quality-tooling.md).
- **Meta — spec validator** — `tools/spec-validator/` exists as a `uv`
  project with `pyproject.toml` and `tests/`, validating spec frontmatter
  and body sections. Spec: [`specs/meta-and-quality-tooling.md`](specs/meta-and-quality-tooling.md).
- **Agent isolation — Python packaging + tests** — `tools/agent-isolation/`
  has `pyproject.toml`, `src/`, and a `tests/` directory with pytest
  coverage for the sandbox profiles and clean-env wrapper.
  Spec: [`specs/agent-isolation-sandbox.md`](specs/agent-isolation-sandbox.md).
- **Eval coverage — complete** — 37 skill eval suites exist in
  `tools/skill-evals/evals/`, covering all skills including the full
  setup-family (setup, setup-isolated-setup-doctor,
  setup-isolated-setup-install, setup-isolated-setup-update,
  setup-isolated-setup-verify, setup-override-upstream,
  setup-shared-config-sync).

---

## In-flight (local branches and open PRs — not available to build)

The following items are already built on local branches or open as PRs.
Do not duplicate them.

| Branch slug | PR | Description |
|---|---|---|
| `injection-guard` | merged (#473) | Prompt-injection hardening on forwarder-relay ingest |
| `check-headers` | #474 | License-header enforcement check in spec-validator |
| `spec-validator-known-gaps` | #490 | Enforce Known-gaps section in every functional spec |
| `spec-validate-hook` | #489 | pre-commit hook for spec-validate |
| `skill-quality-fix` | #488 | Stabilise setup-verify eval + extend check-1 coverage |
| `check-eval-coverage` | #481 | SOFT eval-coverage check (check #8) |
| `eval-quick-merge` | #480 | pr-management-quick-merge skill + evals |
| `spec-validator-path-check` | local | Validate paths referenced in Validation blocks |
| `spec-validator-spdx` | local | Enforce SPDX header on spec files |
| `tracker-dashboard-tests` | local | pyproject + pytest suite for security-tracker render.py |
| `loop-imp` | #467 | Incremental update runs from .last-sync marker |
| `loop-cli-ux` | #472 | Explicit loop.sh argument handling |
| `node-bump-markdownlint` | local | Node 22.13→22.20 bump for markdownlint |
| `token-reduction` | #479 | Slim AGENTS.md into a glossary |
| `docs-modes-sync` | #483 | Sync modes.md skill inventory |
| `docs-mentoring-sync` | #482 | Sync mentoring spec to experimental |
| `eval-setup-status` | #484 | Fix setup-status eval prompts |

---

## Work items (planned)

Priority order. Each maps to one branch and one PR. Branch names are
slugs, not numbers (numbering implies an order the specs don't carry).

1. **First release-management skill: release-vote-draft.**
   `specs/release-management-lifecycle.md` is the only `proposed` spec
   with zero implemented skills. The adopter contract templates
   (`projects/_template/release-management-config.md`,
   `release-build.md`, `pmc-roster.md`, `release-trains.md`,
   `site-repo.md`) already exist. `release-vote-draft` is the most
   standalone and highest-frequency PMC task: it takes RC metadata
   (project name, version, RC number, artifact URLs) and produces a
   VOTE email draft following ASF conventions. Include an eval suite
   in `tools/skill-evals/evals/release-vote-draft/`.
   Validation:
   ```bash
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   uv run --project tools/skill-evals skill-eval tools/skill-evals/evals/release-vote-draft/
   ```
   Spec: [`specs/release-management-lifecycle.md`](specs/release-management-lifecycle.md).
   Branch `release-vote-draft`.

2. **Second release-management skill: release-announce-draft.**
   Companion to `release-vote-draft`. Takes a successful vote tally
   (binding +1 count, RC metadata) and produces the ANNOUNCE email
   draft for the ASF announce@ and dev@ lists, following ASF posting
   conventions (subject: `[ANNOUNCE] Apache <Project> <Version>
   released`). Also standalone: it does not depend on
   `release-vote-draft` being run in the same session. Include an
   eval suite.
   Validation:
   ```bash
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   uv run --project tools/skill-evals skill-eval tools/skill-evals/evals/release-announce-draft/
   ```
   Spec: [`specs/release-management-lifecycle.md`](specs/release-management-lifecycle.md).
   Branch `release-announce-draft`.

3. **Stale-issue sweep for general triage.**
   `specs/triage-mode.md` Known Gaps explicitly names stale-handling
   as missing from the general-issue side (the security side covers
   this via `security-issue-sync`). Add a new skill
   `issue-stale-sweep` that surfaces issues with no activity past a
   configurable threshold and proposes closure or an update request
   (waits for maintainer confirmation before posting). Include an eval
   suite.
   Validation:
   ```bash
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   uv run --project tools/skill-evals skill-eval tools/skill-evals/evals/issue-stale-sweep/
   ```
   Spec: [`specs/triage-mode.md`](specs/triage-mode.md).
   Branch `issue-stale-sweep`.

4. **First-contribution welcome/orientation skill.**
   `specs/mentoring-mode.md` Known Gaps names the "first-contribution
   welcome/orientation skill" as missing. Add `mentoring-welcome`,
   which greets first-time contributors on a newly opened issue or PR
   with orientation context: contributing guide link, community norms,
   expected next steps, and a pointer to the good-first-issue pool.
   Waits for maintainer confirmation before posting. Include an eval
   suite.
   Validation:
   ```bash
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   uv run --project tools/skill-evals skill-eval tools/skill-evals/evals/mentoring-welcome/
   ```
   Spec: [`specs/mentoring-mode.md`](specs/mentoring-mode.md).
   Branch `mentoring-welcome`.

5. **ASF-coupling advisory lint (fold into `skill-and-tool-validator`).**
   `specs/project-agnosticism.md` Known Gaps names the absence of an
   automated ASF-coupling check as its first gap. Add a new SOFT advisory
   category to `tools/skill-and-tool-validator` that reuses the existing
   walk, file allowlist, and inline `e.g.`/`example:` markers (the same
   machinery as the placeholder check). It flags a curated, tiered set of
   ASF-coupled tokens in skill bodies (high-confidence:
   `svn (mv|commit|co)`, `announce@apache.org`, `dist/(dev|release)/`,
   Vulnogram URLs; low-confidence: bare `PMC` / `ICLA` / `incubator`) and
   tags each hit with a remedy class (placeholder / adapter /
   capability-flag). SOFT only: surfaces on stderr, never fails the build.
   Extend the validator tests with a coupled fixture and an allowlisted
   fixture.
   Validation:
   ```bash
   uv run --project tools/skill-and-tool-validator --group dev pytest
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   ```
   Spec: [`specs/project-agnosticism.md`](specs/project-agnosticism.md).
   Branch `asf-coupling-lint`.

6. **Sync drafting-mode spec Known Gaps to reflect shipped skills.**
   `specs/drafting-mode.md` Known Gaps still says "Generic
   (non-security, non-issue) Drafting from audit-tool findings is
   `proposed`", but `audit-finding-fix` shipped with a full eval suite.
   Update the Known Gaps section to reflect the current state and
   remove the stale `proposed` claim so new plan passes do not
   re-raise this as a gap.
   Validation:
   ```bash
   uv run --project tools/spec-validator --group dev spec-validate tools/spec-loop/specs/
   uv run --project tools/spec-validator --group dev pytest
   ```
   Spec: [`specs/drafting-mode.md`](specs/drafting-mode.md).
   Branch `drafting-spec-sync`.

7. **Non-ASF adopter profile fixture + smoke eval.**
   `specs/project-agnosticism.md` acceptance #3 requires that a non-ASF
   profile can be declared without editing any skill body, but there is
   no fixture to prove it. Add a worked non-ASF profile under
   `projects/_template/` (non-ASF values for the existing placeholders
   and any capability flags) plus a smoke eval that drives a
   representative skill through it and asserts no skill-body edits are
   needed. This turns acceptance #3 into a measurable gate. Pure
   engineering, no policy decision required.
   Validation:
   ```bash
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   uv run --project tools/skill-evals skill-eval tools/skill-evals/evals/non-asf-profile-smoke/
   ```
   Spec: [`specs/project-agnosticism.md`](specs/project-agnosticism.md).
   Branch `non-asf-profile-fixture`.

---

## Notes & discoveries

- The general Ralph-loop technique pushes after every iteration. That
  step is intentionally **removed** here: `git push` and `gh pr create`
  are in the repo's `ask` permission list and are the human's step.
- Validation per work item lives in the relevant spec's **Validation**
  section; the build prompt runs it as backpressure before committing.
- Auto-merge is deliberately off and has no work items — building toward
  it would skip the proof MISSION requires.
- When a build iteration creates a new skill, its eval suite is part of
  that same work item — not a separate one.
- **Release-management family:** only the two most standalone skills
  (`release-vote-draft`, `release-announce-draft`) are planned here.
  The remaining eight (`release-prepare`, `release-keys-sync`,
  `release-rc-cut`, `release-verify-rc`, `release-vote-tally`,
  `release-promote`, `release-archive-sweep`, `release-audit-report`)
  should be planned in subsequent passes once the first two establish
  the skill-authoring patterns for this family.
- **Triage contributor-growth gaps** (PMC-member nomination,
  emeritus-committer handling, contributor offboarding) noted in
  `triage-mode.md` Known Gaps are intentionally deferred: they are
  vague enough that a spec-RFC conversation is more appropriate than
  a direct build item.
- **Project-agnosticism:** two of the three gaps in
  `project-agnosticism.md` are buildable and planned now: the ASF-coupling
  advisory lint (work item 5) and the non-ASF adopter profile fixture
  (work item 7). The remaining gap, the capability-flag vocabulary for
  contributor intake (ICLA vs DCO), security intake, and CVE allocation,
  is deferred only until someone enumerates the option sets and defaults,
  following the backend-flag precedent already set by
  `release-management-lifecycle.md` (distribution / approval / announcement
  backends). That is a spec-authoring task, not yet a build item.
- **General-issue dedupe and backlog dashboard** (`triage-mode.md` Known
  Gaps) are deferred behind `issue-stale-sweep` (work item 3): dedupe
  overlaps the existing `security-issue-deduplicate` matching approach and
  a backlog dashboard overlaps `pr-management-stats`, so both should reuse
  those patterns once stale-sweep establishes the general-issue skill
  shape. Not dropped, sequenced after item 3.
- **Repo-health family** (`triage-mode.md` Known Gaps: the standalone
  `ci-runner-audit` plus candidate siblings, GitHub Actions security
  audit, dependency-update triage, license/NOTICE compliance, flaky-test
  detection) is deferred pending a family spec; it is a multi-skill area
  that wants its own spec before any build item.
