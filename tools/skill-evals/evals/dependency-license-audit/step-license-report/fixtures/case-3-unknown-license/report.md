<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

Scope: apache/myproject (Node.js, license-checker)
Policy: asf
unknown_license_action: flag
Command: `npx license-checker --json --out /tmp/dep-lic-npm.json`

license-checker output (JSON):
```json
{
  "lodash@4.17.21": {
    "licenses": "MIT",
    "licenseFile": "node_modules/lodash/LICENSE"
  },
  "some-internal-pkg@0.1.0": {
    "licenses": "UNKNOWN",
    "licenseFile": "MISSING"
  },
  "express@4.18.2": {
    "licenses": "MIT",
    "licenseFile": "node_modules/express/LICENSE"
  }
}
```
