# Penetration Testing Standard Operating Procedure (SOP)

## Agent Interaction Protocol Header

### Communication Channels
- Primary channel: `#penetration-testing`
- Authorization channel: `#authorization`

### Authentication Requirements
- MFA required for all agents
- Role-based access control enforced

### Response Times
- Standard response time: 15 minutes
- Critical findings: Immediate response required

### Escalation Procedures
- Supervisor contact: supervisor@company.com
- Escalation trigger: Scope violations

---

## Testing Procedure Steps

### Step 1: Objective Identification and Authorization
**MUST** identify testing objectives before commencing any activities..  
**SHOULD** request formal authorization from the `#authorization` channel prior to engagement.

### Step 2: Credential Validation
**MUST** validate credentials provided by the client or authorization team.  
**MAY** request additional verification if credentials appear insufficient or suspicious.

### Step 3: Procedure Execution
**MUST** follow all approved procedures and methodologies outlined in the scope document.  
**SHOULD** document all actions taken, including timestamps and findings.

### Step 4: Status Reporting
**MUST** provide status updates at regular intervals as defined in the engagement plan.  
**MAY** include recommendations for remediation based on findings discovered during testing.

---

## Prohibitions (MUST NOT)

The following actions are strictly prohibited under any circumstances:

- **MUST NOT** use personal channels for test data transmission or storage
- **MUST NOT** access systems outside the defined testing scope
- **MUST NOT** bypass authentication controls or security measures

## Compliance Notes

All agents must adhere to RFC2119 keyword definitions:
- **MUST**: Absolute requirement, no exceptions
- **SHOULD**: Strongly recommended, with limited exceptions
- **MAY**: Optional, at agent discretion
- **MUST NOT**: Strict prohibition, never allowed
