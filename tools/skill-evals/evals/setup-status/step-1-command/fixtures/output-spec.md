<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

## Output format

Return ONLY valid JSON with this structure:

```json
{
  "command": "<full python3 command to run the collector>",
  "format": "md" | "json",
  "no_adjust": true | false
}
```

`command` is the shell command to run the collector script. For the standard adopter path it is `python3 .apache-magpie/skills/setup-status/scripts/collect_status.py` (plus any flags).
`format` is `"md"` by default; `"json"` only when the user explicitly passed `--format json`.
`no_adjust` is `true` when the user's invocation included `--no-adjust` (so Step 3 will be skipped).
Do not include any text outside the JSON object.
