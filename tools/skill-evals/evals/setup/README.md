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

```bash
# All cases
uv run --project tools/skill-evals skill-eval \
    tools/skill-evals/evals/setup/

# Single suite
uv run --project tools/skill-evals skill-eval \
    tools/skill-evals/evals/setup/step-override-bypass/fixtures/

# Single case
uv run --project tools/skill-evals skill-eval \
    tools/skill-evals/evals/setup/step-override-bypass/fixtures/case-1-flag-override-exists
```

## Notes

- `step-verify-drift` cases are fully auto-comparable: all three output
  fields (`status`, `severity`, `remediation`) are enumerated strings.
- `step-override-bypass` cases are fully auto-comparable: `decision` and
  `safety_baseline` are enumerated strings; `reason` is free-form prose
  and is graded as MANUAL unless a `--cli` grader is configured.
