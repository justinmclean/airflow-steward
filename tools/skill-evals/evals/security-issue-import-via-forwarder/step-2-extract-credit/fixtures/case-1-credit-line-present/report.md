# SPDX-License-Identifier: Apache-2.0

## Context

Matched adapter: `asf-security`

The `asf-security` adapter's `extract_credit()` scans the body for a
`Credit:` line per the ASF forwarding convention.

## Mock: Message body (passed to extract_credit)

```
The Apache Security Team has received the following security report and
is forwarding it to the Airflow security list for triage.

Credit: Alex Vulnerability-Hunter <a.hunter@infosec.example>
GHSA: GHSA-xxxx-yyyy-zzzz

--- Forwarded report below ---

I found a remote code execution vulnerability in Airflow's plugin loader.
An attacker with access to the plugins folder can execute arbitrary code
on the scheduler.

Affected: Apache Airflow 2.10.x
```
