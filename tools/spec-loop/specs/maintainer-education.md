<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

---
title: Maintainer-education stream
status: proposed
kind: docs
mode: infra
source: >
  MISSION.md § Maintainer education — building agentic projects is a
  different craft; MISSION.md § Initial Goals ("Ship the
  maintainer-education stream alongside v1"); PRINCIPLES.md § 18
  (maintainer education ships with the platform, release-blocking).
  Referenced but not yet delivered by docs/rfcs/RFC-AI-0004.md
  (§ "the maintainer-education stream").
acceptance:
  - A docs/education/ landing page exists and is linked from docs/index.md.
  - The four MISSION-named pieces exist as pages: pattern catalogue,
    "your first skill" path, eval-driven-development examples, and
    workshop / office-hours material.
  - The "your first skill" path is beginner-facing onboarding, distinct
    from the write-skill authoring reference.
  - Pages are project-agnostic (placeholders, PRINCIPLE 12) and land
    under Apache-2.0 (PRINCIPLE 17).
  - The dangling RFC-AI-0004 back-reference resolves to the landing page.
---

# Maintainer-education stream

## What it does

Lowers the on-ramp for maintainers who have never built an agentic
application. MISSION treats this as a first-class part of the project,
not an afterthought wiki page, and PRINCIPLE 18 makes it release-blocking:
"a platform without the education stream alongside it is not adoptable,
regardless of code quality." The mental model is genuinely different from
twenty years of writing services and CLIs — behaviour is probabilistic
not deterministic, prompts and skill files *are* code, evaluating output
is harder than testing a function, and the unit of authorship shifts from
"a function in a file" to "a skill the agent invokes." The stream teaches
that shift with worked, copy-pasteable material.

## Where it lives

Nothing ships this yet. The only reference is
`docs/rfcs/RFC-AI-0004.md`, which points readers at MISSION "for the
maintainer-education stream" with no landing page behind it. The
proposed home is `docs/education/`:

- `docs/education/README.md` — landing page: what the stream is, who it
  is for, and an index of the pieces below. Linked from `docs/index.md`.
- `docs/education/pattern-catalogue.md` — copy-pasteable skill / prompt /
  tool-use patterns with war stories: what worked, what did not, and why.
  Distinct from the PII pattern catalogue at `tools/privacy-llm/pii.md`,
  which is a redaction reference, not a teaching artefact.
- `docs/education/your-first-skill.md` — a beginner "zero-to-merged"
  path for landing a first working skill, the agentic equivalent of a
  "your first PR" doc. Distinct from the `write-skill` skill, which is
  the authoring *reference* for someone who already knows the shape.
- `docs/education/eval-driven-development.md` — how to think about
  correctness when "correct" is a distribution, with worked examples
  drawn from real Magpie skills and wired to a shared eval methodology
  (MISSION § Initial Goals) rather than reinvented per page.
- `docs/education/workshops.md` — office-hours / pairing-session format,
  scheduling, and where recordings are published.
- `docs/education/apache-training/` — the stream repackaged as a
  reusable, LMS-neutral Apache Training module: per-lesson **learning
  objectives**, hands-on **exercises**, and **self-check** questions,
  plus a module index mapping each lesson back to the source page above.
  So any project — ASF or not — can *teach* the material, not just read
  it. Phase 2: lands after the pages above, and is shaped to Apache
  Training conventions so it can be contributed upstream there.

## Behaviour & contract

- **Release-blocking, per PRINCIPLE 18.** Every release ships the docs,
  patterns, eval examples, and workshop material maintainers actually
  need for the skills that release includes. The stream is not a
  follow-up milestone.
- **Project-agnostic, per PRINCIPLE 12.** Pages use
  `<PROJECT>` / `<tracker>` / `<upstream>` placeholders and never bake a
  concrete adopter name into the teaching text.
- **Apache-2.0, per PRINCIPLE 17.** Contributions to the stream land
  under the framework licence; AI-authored contributions carry the
  `Generated-by:` token.
- **Teaches the framework's own posture.** Examples inherit the
  data-not-instructions rule (PRINCIPLE 0), the privacy/sandbox posture
  (PRINCIPLE 1), and eval-as-release-discipline (PRINCIPLE 8) — the
  stream shows the safe pattern, never a shortcut around it.
- **Eval methodology is shared, not per-page.** The eval-driven-
  development page references the framework's shared eval methodology
  and the in-repo eval harness (`tools/skill-evals/`) rather than
  describing a parallel approach.

## Out of scope

- Owning the community-development mentoring *function* — that stays with
  ComDev (and, for podlings, the Incubator) for ASF projects. This stream
  ships education *material*, not a governance role (MISSION § Scope
  boundaries).
- Building a standalone contributor-sentiment eval framework. This
  stream consumes a shared eval methodology; it does not define or
  build one.
- Runtime skill behaviour — the education pages are docs, not skills, and
  make no state changes.

## Acceptance criteria

1. `docs/education/README.md` exists and is linked from `docs/index.md`.
2. All four MISSION-named pieces exist as pages: pattern catalogue,
   "your first skill" path, eval-driven-development examples, and
   workshop material.
3. The "your first skill" path is beginner onboarding, cross-linked to
   but distinct from `write-skill`.
4. Pages carry the SPDX header, use placeholders (no concrete adopter
   name in teaching text), and pass markdownlint / link checks.
5. The RFC-AI-0004 back-reference resolves to the new landing page.
6. The Apache Training module (`docs/education/apache-training/`) exists
   with per-lesson learning objectives, exercises, and self-checks, and
   is shaped for upstream contribution to Apache Training.

## Validation

While this spec is `proposed`, no `docs/education/` page exists yet, so
the per-file existence checks live in the IMPLEMENTATION_PLAN work item
(`maintainer-education-stream`) rather than here — this section only
references paths that exist today. Once the stream lands, the landing
page and the four MISSION pieces are present under `docs/education/` and
linked from `docs/index.md`.

```bash
uv run --project tools/spec-validator --group dev pytest
uv run --project tools/skill-and-tool-validator --group dev skill-and-tool-validate
```

## Known gaps

- **`proposed` — nothing built.** No page in the stream exists yet; the
  only pointer is the dangling RFC-AI-0004 reference. This is the whole
  gap the work item tracks.
- **Workshop cadence undefined.** MISSION commits to "first scheduled
  workshops" but the schedule and hosting belong to the PMC once the
  material lands; the page ships the format, not the calendar.
- **Shared-methodology dependency.** The eval-driven-development page
  can land its worked examples immediately, but the link to the
  framework's shared contributor-sentiment methodology firms up only
  once that methodology is defined.
- **Apache Training module is a phase-2 epic.** The
  `docs/education/apache-training/` packaging depends on the source pages
  existing first, and its final shape depends on coordination with the
  Apache Training project for upstream contribution. It is not a single
  deliverable: it decomposes into many work items (one per lesson module,
  per-lesson exercises, an instructor guide, and the upstream hand-off),
  tracked as an umbrella entry in IMPLEMENTATION_PLAN.md until it reaches
  the top of the queue and is split.
