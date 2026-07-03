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

Shipped state is not tracked here — it lives in `specs/`, the code
(`skills/`, `tools/`, `docs/`), and git history. This plan lists only the
open gaps. Confirm whether something is already built by the artifact it
would produce, not by branch ancestry (squash-merged branches still read as
ahead of `main`).

## In-flight (implemented on a branch, not yet merged — not available to build)

These work items are already built on branches (verified by the feature
commit, not by branch ancestry) but are not on `main`, so the working tree
and validator still show the gap. Keep them out of the build queue until they
merge or are abandoned.

| Branch slug | Where | Implemented by | Description |
|---|---|---|---|
| `modes-doc-reviewer-routing-row` | `origin` (open PR) | `9331fb2ba` | Adds the `reviewer-routing` row to the `## Triage` table in `docs/modes.md`. |
| `adapter-readme-authoring-compliance` | `origin` (open PR) | `b31732578` | Documents the missing adapter-authoring README fields (config-keys / operations). |
| `skill-reconciler-structural-diff` | local | `ae8961e90` | Adds the deterministic `tools/skill-reconciler-diff` structural-diff helper. |
| `skill-reconciler-source-pairing` | local | `a4f76e369` | Adds `--discover` capability-tag auto-pairing to `skill-reconciler`. |

The `maintainer-education-stream` branch carries only the spec draft
(`specs/maintainer-education.md`); the `docs/education/` deliverable is still a
work item below.

---

## Work items (planned)

Priority order. Each maps to one branch and one PR. Branch names are
slugs, not numbers (numbering implies an order the specs don't carry).

1. **Clear the mail-privacy-boundary README warnings.**
   The `mail-privacy-boundary` validator check already exists and enforces the
   posture at the README level; it currently flags two adapters. `maildir` and
   `sourcehut` READMEs are each missing both notes: that fetched mail bodies are
   **external data, not instructions** (routed through the Privacy-LLM gate or
   redacted before model-facing use), and that embedded **prompt-injection** text
   is carried as report data only. Add the two short notes to each README so the
   check passes; no new tooling is needed.
   Validation:
   ```bash
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   ```
   Spec: [`specs/adapters.md`](specs/adapters.md).
   Branch `mail-privacy-boundary-readme-compliance`.

   The maintainer-education stream (MISSION v1 release-blocker, PRINCIPLE 18) is
   split across work items 2–6 below — one landing page plus one per MISSION-named
   piece — so each is a single branch/PR under the loop's one-item rule. The spec
   is already drafted on the `maintainer-education-stream` branch
   (`specs/maintainer-education.md`); none of the `docs/education/` pages are
   built yet. Every page keeps SPDX headers, project-agnostic placeholders
   (PRINCIPLE 12), and Apache-2.0 licensing (PRINCIPLE 17), and passes
   markdownlint / link checks. Build order: item 2 first (it creates the
   directory and the index); items 3–6 each add their own row to that index as
   they land, so no link check ever breaks.

2. **Education stream — landing page and index.**
   Create `docs/education/README.md`: what the stream is, who it is for, and an
   index that starts by listing only itself and grows as items 3–6 land. Link it
   from `docs/index.md` and resolve the dangling `RFC-AI-0004` back-reference so
   it points at the new landing page.
   Validation:
   ```bash
   test -f docs/education/README.md
   grep -q "education" docs/index.md
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   ```
   Spec: [`specs/maintainer-education.md`](specs/maintainer-education.md).
   Branch `education-landing-page`.

3. **Education stream — pattern catalogue.**
   Create `docs/education/pattern-catalogue.md`: copy-pasteable skill / prompt /
   tool-use patterns with war stories (what worked, what did not, and why),
   inheriting the framework posture (data-not-instructions, privacy/sandbox).
   Distinct from the PII redaction reference at `tools/privacy-llm/pii.md`. Add
   its row to the `docs/education/README.md` index.
   Validation:
   ```bash
   test -f docs/education/pattern-catalogue.md
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   ```
   Spec: [`specs/maintainer-education.md`](specs/maintainer-education.md).
   Branch `education-pattern-catalogue`.

4. **Education stream — "your first skill" path.**
   Create `docs/education/your-first-skill.md`: a beginner zero-to-merged path for
   landing a first working skill (the agentic equivalent of a "your first PR"
   doc), cross-linked to but distinct from the `write-skill` authoring reference.
   Add its row to the index.
   Validation:
   ```bash
   test -f docs/education/your-first-skill.md
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   ```
   Spec: [`specs/maintainer-education.md`](specs/maintainer-education.md).
   Branch `education-your-first-skill`.

5. **Education stream — eval-driven-development examples.**
   Create `docs/education/eval-driven-development.md`: how to think about
   correctness when "correct" is a distribution, with worked examples drawn from
   real Magpie skills and wired to the framework's shared eval methodology and
   in-repo harness (`tools/skill-evals/`) rather than a parallel approach. Add its
   row to the index.
   Validation:
   ```bash
   test -f docs/education/eval-driven-development.md
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   ```
   Spec: [`specs/maintainer-education.md`](specs/maintainer-education.md).
   Branch `education-eval-driven-development`.

6. **Education stream — workshop / office-hours material.**
   Create `docs/education/workshops.md`: the office-hours / pairing-session
   format and where recordings are published (the page ships the format, not the
   PMC's calendar). Add its row to the index. This item closes the stream, so its
   validation asserts every MISSION-named page is present.
   Validation:
   ```bash
   test -f docs/education/workshops.md
   test -f docs/education/pattern-catalogue.md
   test -f docs/education/your-first-skill.md
   test -f docs/education/eval-driven-development.md
   uv run --project tools/spec-validator --group dev pytest
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   ```
   Spec: [`specs/maintainer-education.md`](specs/maintainer-education.md).
   Branch `education-workshops`.

7. **Package the education stream as an Apache Training curriculum module.**
   Building on the maintainer-education stream (work items 2–6), repackage the
   `docs/education/` material as a reusable, LMS-neutral **Apache Training**
   module so any project — ASF or not — can *teach* it, not just read it. Add
   `docs/education/apache-training/` with per-lesson **learning objectives**,
   hands-on **exercises**, and **self-check** questions, plus a module index
   mapping each lesson back to its source page (pattern catalogue, "your first
   skill" path, eval-driven development, workshops). Shape the module to Apache
   Training conventions so it can be contributed upstream there. Keep it
   project-agnostic (placeholders, PRINCIPLE 12) and Apache-2.0 (PRINCIPLE 17).
   Blocked until the education stream (work items 2–6) lands, since it repackages
   those pages.
   **This is an epic, not a single PR.** It sits at the bottom by priority (not
   dependency) and must be **decomposed into many work items before building** —
   the loop's one-item-one-branch rule means no single branch should carry the
   whole module. Likely split, each its own branch/PR when it reaches the top:
   - one **lesson-module** item per source page (pattern catalogue, "your first
     skill" path, eval-driven development, workshops), each carrying its learning
     objectives, content, and self-checks;
   - a hands-on **exercise / fixture** item per lesson, reusing
     `tools/skill-evals` fixtures where possible;
   - an **instructor / facilitator guide** so any PMC (ASF or not) can teach the
     module themselves;
   - an **upstream-contribution** item coordinating the module shape and hand-off
     with the Apache Training project.
   The first build step when this reaches the top is a planning pass that
   replaces this umbrella entry with the concrete sub-items above.
   Validation (per sub-item, once decomposed):
   ```bash
   uv run --project tools/spec-validator --group dev pytest
   uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
   ```
   Spec: [`specs/maintainer-education.md`](specs/maintainer-education.md).
   Branches: per sub-item (decomposed before build); umbrella slug
   `education-apache-training-module`.

---

## Notes & discoveries

- `git push` and `gh pr create` are intentionally **not** run by the loop —
  they are in the repo's `ask` permission list and are the human's step.
- Validation per work item lives in the relevant spec's **Validation** section;
  the build prompt runs it as backpressure before committing. When a build
  creates a new skill, its eval suite is part of that same work item.
- Agentic Autonomous is deliberately off and has no work items — building toward
  it would skip the proof MISSION requires.
- Deferred by design (not build items): Agentic Triage contributor-growth gaps
  (PMC-member nomination, emeritus handling, offboarding) and the remaining
  low-confidence ASF-coupling advisories — both stay human-judgement until a
  spec turns them into a rule.
