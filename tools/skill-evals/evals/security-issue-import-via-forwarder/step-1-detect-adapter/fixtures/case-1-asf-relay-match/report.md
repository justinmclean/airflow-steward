# SPDX-License-Identifier: Apache-2.0

## Mock: Registered adapters (forwarders.enabled)

```json
[
  {
    "name": "asf-security",
    "sender_pattern": "security@apache.org",
    "preamble_match": "The Apache Security Team has received"
  }
]
```

## Mock: Inbound message

```
From: security@apache.org
Subject: [SECURITY] SSRF via HTTP operator task callback URL (forwarded from external researcher)
Date: Mon, 2 Jun 2025 09:14:22 +0000
Message-ID: <CABcde123@apache.org>

The Apache Security Team has received the following security report and
is forwarding it to the Airflow security list for triage.

Credit: Sam Vulnerability-Researcher <s.researcher@infosec.example>
GHSA: GHSA-0000-0000-0001

--- Forwarded report below ---

Hi,

I found a server-side request forgery (SSRF) vulnerability in Airflow's HTTP
operator when handling task callback URLs. An authenticated attacker can cause
the scheduler to issue arbitrary HTTP requests to internal services.

Affected: Apache Airflow 2.9.x
```
