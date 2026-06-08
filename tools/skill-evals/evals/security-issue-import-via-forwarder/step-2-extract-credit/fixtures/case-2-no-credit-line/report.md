# SPDX-License-Identifier: Apache-2.0

## Context

Matched adapter: `asf-security`

The `asf-security` adapter's `extract_credit()` scans the body for a
`Credit:` line. This message has no such line.

## Mock: Message body (passed to extract_credit)

```
The Apache Security Team has received the following security report and
is forwarding it to the Airflow security list for triage.

GHSA: GHSA-aaaa-bbbb-cccc

--- Forwarded report below ---

The Airflow webserver leaks internal hostnames in HTTP response headers
when the `expose_config` setting is enabled.

No credit line was included in this forwarded report.
```
