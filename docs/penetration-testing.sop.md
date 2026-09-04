---
priority: MEDIUM
version: 1.0
last_updated: 2024-01-15
status: FINAL
---

# Overview

This SOP defines the standardized approach for conducting penetration testing engagements within our organization. All security operations agents must adhere to these guidelines to ensure consistent, compliant, and ethical testing practices.

## Agent Interaction Protocol

- **Authorization**: Obtain written authorization from CISO before initiating any testing activities
- **Communication**: Maintain open channels with SOC for real-time incident reporting during engagements
- **Escalation**: Report critical vulnerabilities to SOC team within 15 minutes of detection

## Procedure Steps

1. **Pre-engagement Planning**: Define scope, objectives, and boundaries; obtain formal written authorization; configure monitoring tools and establish baseline metrics
2. **Scoping Phase**: Conduct passive information gathering using approved tools only; document all findings in central repository; maintain chain of custody for evidence
3. **Exploitation & Testing**: Execute authorized vulnerability exploitation within defined scope limits; avoid DoS attacks or data exfiltration; capture proof-of-concept demonstrations
4. **Reporting & Remediation**: Generate comprehensive reports with risk ratings and remediation recommendations; schedule follow-up testing after 30 days; archive all test artifacts per retention policy

## Prohibitions

- MUST NOT test systems outside the explicitly defined scope without additional written authorization
- MUST NOT access or exfiltrate any data beyond what is necessary for vulnerability validation
- MUST NOT use unauthorized tools, techniques, or methods listed in the approved penetration testing toolkit

## RFC2119 Notes

This document uses standard IETF RFC 2119 key words (MUST, MUST NOT, REQUIRED, SHALL, SHOULD) as defined in [RFC2119](https://www.rfc-editor.org/rfc/rfc2119). These terms indicate requirement levels for compliance with this SOP.
