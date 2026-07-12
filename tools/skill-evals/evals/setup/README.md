<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

# setup evals

Behavioral evals for the `setup` skill.

## Suites (8 cases total)

| Suite | Step | Cases | What it covers |
|---|---|---|---|
| step-verify-drift | verify.md § Check 3 (drift) | 5 | clean, method/URL mismatch, ref mismatch, svn-zip SHA-512 mismatch, local lock missing |
| step-override-bypass | agentic-overrides.md § One-shot defaults run | 3 | `--no-overrides` flag + override exists, `--no-overrides` + no override, no flag + override exists |

## Run

`--cli` is required or nothing is graded; use `--directory`, not
`--project`, and run from the repo root.

```bash
# All cases
uv run --directory tools/skill-evals skill-eval --cli "claude -p" \
    evals/setup/

# Single suite
uv run --directory tools/skill-evals skill-eval --cli "claude -p" \
    evals/setup/step-override-bypass/

# Single case
uv run --directory tools/skill-evals skill-eval --cli "claude -p" \
    evals/setup/step-override-bypass/fixtures/case-1-flag-override-exists
```

## Notes

- `step-verify-drift` cases are fully auto-comparable: all three output
  fields (`status`, `severity`, `remediation`) are enumerated strings.
- `step-override-bypass` cases are fully auto-comparable: `decision` and
  `safety_baseline` are enumerated strings, and `reason` is checked by
  deterministic `regex` predicates in `assertions.json`
  (`has_bypass_reason` for the skip cases, `has_apply_reason` for the
  apply case) — no grader or MANUAL step is required.
