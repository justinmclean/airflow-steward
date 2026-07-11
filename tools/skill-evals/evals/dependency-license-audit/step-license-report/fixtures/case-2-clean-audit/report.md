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
    "Name": "urllib3",
    "Version": "2.2.1",
    "License": "MIT License",
    "URL": "https://pypi.org/project/urllib3/"
  },
  {
    "Name": "charset-normalizer",
    "Version": "3.3.2",
    "License": "MIT License",
    "URL": "https://pypi.org/project/charset-normalizer/"
  }
]
```
