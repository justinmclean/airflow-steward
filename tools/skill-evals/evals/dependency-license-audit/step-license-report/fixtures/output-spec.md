<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

## Output format

Return ONLY valid JSON with this structure:

```json
{
  "findings_present": true | false,
  "category_x_listed_first": true | false,
  "each_finding_has_package_version_license": true | false,
  "unknown_license_flagged_when_applicable": true | false,
  "autopilot_edit_offered": false,
  "scope_and_policy_included": true | false,
  "clean_stated_explicitly": true | false,
  "category_b_binary_only_noted": true | false,
  "reason": "<short rationale>"
}
```

`findings_present` is `true` when the input contains any category X,
unknown-license, or category B dependency — anything that needs a report entry
beyond a plain category A allow. It is `false` only when every dependency is
category A.
`category_x_listed_first` is `true` when category X / forbidden findings
appear before category B / unknown-license entries. Vacuously `true` when
there are no findings at all.
`each_finding_has_package_version_license` is `true` when each reported
finding includes the package name, installed version, and detected license.
`unknown_license_flagged_when_applicable` is `true` when there are
unknown-license packages in the input AND they are reported in the output
(given `unknown_license_action: flag`). Vacuously `true` when there are no
unknown-license packages.
`autopilot_edit_offered` MUST always be `false` — the skill never offers to
apply manifest changes automatically.
`clean_stated_explicitly` is `true` when every dependency is category A (no
category X, unknown-license, or category B dependency) AND the report
explicitly states the audit is clean. A tree that contains category B
dependencies is not a bare clean: those must be surfaced with their
binary-only condition instead of a clean statement.
`category_b_binary_only_noted` is `true` when the input contains a category B
(weak-reciprocal, e.g. MPL-2.0 / EPL-2.0 / CDDL) dependency AND the report
lists it with its binary-only inclusion condition (may ship in convenience
binaries but not in a source release) rather than as a forbidden finding or as
clean-with-no-mention. Vacuously `true` when the input has no category B
dependencies.
Do not include any text outside the JSON object.
