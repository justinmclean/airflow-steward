<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Velox Stream — reviewer roster](#velox-stream--reviewer-roster)
  - [Roster](#roster)
  - [Notes](#notes)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

# Velox Stream — reviewer roster

Used by the [`reviewer-routing`](../../skills/reviewer-routing/SKILL.md) skill
to score and propose reviewers for inbound issues and PRs on the
`velox-community/velox-stream` repository.

This is a **fictional fixture** used by the `non-asf-profile-smoke` eval
suite to verify that `reviewer-routing` works with a plain
`reviewer-roster.md` file and no ASF infrastructure.

## Roster

- handle: priya-velox
  areas:
    - component:core
    - component:pipeline
    - velox/core/
    - velox/pipeline/
  max_reviews: 4

- handle: mateo-stream
  areas:
    - component:connectors
    - component:serialization
    - velox/connectors/
    - velox/serialization/
  max_reviews: 5

- handle: yuki-velox
  areas:
    - component:docs
    - component:testing
    - docs/
    - tests/
  max_reviews: 6

## Notes

- `areas` entries are component labels (matching the issue-tracker labels in
  `issue-tracker-config.md`) and file-path prefixes.
- `max_reviews` is the maximum concurrent open review requests per reviewer.
- This roster uses no ASF-specific fields (no `apache_id`, no `committee`,
  no `pmc` membership) — it is valid for the `organization: independent` profile.
