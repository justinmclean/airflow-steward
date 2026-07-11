<!-- SPDX-License-Identifier: Apache-2.0
     https://www.apache.org/licenses/LICENSE-2.0 -->

Scope: apache/myproject (Python, pip-licenses)
Policy: asf
Command: `pip-licenses --format json --with-urls --output-file /tmp/dep-lic-pip.json`

pip-licenses output (JSON):
```json
[
  {
    "Name": "requests",
    "Version": "2.31.0",
    "License": "Apache Software License",
    "URL": "https://pypi.org/project/requests/"
  },
  {
    "Name": "some-gpl-lib",
    "Version": "1.2.0",
    "License": "GNU General Public License v3 (GPLv3)",
    "URL": "https://pypi.org/project/some-gpl-lib/"
  },
  {
    "Name": "chardet",
    "Version": "5.2.0",
    "License": "GNU Lesser General Public License v2 or later (LGPLv2+)",
    "URL": "https://pypi.org/project/chardet/"
  }
]
```
