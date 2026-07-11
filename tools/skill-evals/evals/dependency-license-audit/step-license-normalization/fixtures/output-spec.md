<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

## Output format

Return ONLY valid JSON with this structure:

```json
{
  "spdx": "<canonical SPDX identifier or expression, or empty>",
  "ambiguous": true | false,
  "reason": "<short rationale>"
}
```

`spdx` is the canonical SPDX identifier the raw string resolves to. Preserve
the `-only` vs `-or-later` distinction; they are different identifiers.
`ambiguous` is `true` when the raw string cannot be resolved to a single SPDX
identifier and must be treated as unresolved (do not guess the most common
variant). When `ambiguous` is `true`, `spdx` is empty.

Do not include any text outside the JSON object.
