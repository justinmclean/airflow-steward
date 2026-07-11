<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

Scope: apache/myproject (Java, Maven, license-maven-plugin)
Policy: asf
Command: `mvn org.codehaus.mojo:license-maven-plugin:2.4.0:aggregate-download-licenses`

Resolved dependency licenses (normalised to SPDX):
```json
[
  {
    "name": "com.google.guava:guava",
    "version": "33.0.0-jre",
    "license": "Apache-2.0"
  },
  {
    "name": "com.h2database:h2",
    "version": "2.2.224",
    "license": "EPL-2.0"
  },
  {
    "name": "org.mozilla:rhino",
    "version": "1.7.14",
    "license": "MPL-2.0"
  }
]
```

No category X or unknown-license dependencies are present. EPL-2.0 and MPL-2.0
are ASF category B (weak reciprocal), which may be included in binary-only
form in convenience binaries but must not be included in a source release.
