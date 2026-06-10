<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

## Output format

Return ONLY valid JSON with this structure:

```json
{
  "adopted": true | false,
  "proceed": true | false,
  "drift_flag": "none" | "local-lock-absent" | "version-mismatch"
}
```

`adopted` is `true` when `.apache-magpie.lock` (the committed lock) is present.
`proceed` is `true` when the repo is adopted. Drift is non-blocking — a repo with drift still proceeds.
`drift_flag` is `"none"` when locks match or self-adoption (method:local); `"local-lock-absent"` when committed lock exists but no local lock; `"version-mismatch"` when both locks exist but their ref/method/url differs.
Do not include any text outside the JSON object.
