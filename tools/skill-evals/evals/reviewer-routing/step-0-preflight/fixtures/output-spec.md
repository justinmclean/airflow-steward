<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

# Step 0 output specification

The model must return ONLY valid JSON matching this schema:

```json
{
  "verdict": "proceed" | "blocked",
  "blockers": ["<string>"],
  "privacy_gate_passed": true | false,
  "roster_source": "release-trains" | "reviewer-roster" | null,
  "item_type": "pr" | "issue",
  "item_number": <integer>,
  "upstream_repo": "<owner/name>"
}
```

Grading rules:
- `verdict` is `"proceed"` only when all five pre-flight checks pass.
- `verdict` is `"blocked"` when any hard check fails.
- `blockers` is an empty array when `verdict` is `"proceed"`.
- `privacy_gate_passed` must be `false` when `privacy-llm-check` exits non-zero.
- `roster_source` is `null` only when neither roster file was found.
- `item_type` is `"pr"` or `"issue"` matching the resolved input.
- `item_number` is the integer PR or issue number.
- No extra keys are permitted.
