# Recon-Enumeration Standard Operating Procedure (SOP)

## Document Control
| Field | Value |
|-------|-------|
| Version | 1.0 |
| Status | Active |
| Last Updated | 2024-01-15 |
| Author | Security Operations Team |

---

## 1. Agent Interaction Protocol Header

### 1.1 Communication Channels
**MUST** use only the following approved channels for all agent interactions:
- **Primary Channel**: `https://secure.ops.internal/api/v1/agent` (TLS 1.3, mutual authentication)
- **Secondary Channel**: `sops://ops.corp/enum-recon` (SOPS encrypted, ephemeral keys)
- **Emergency Channel**: `emergency://ops.corp/critical` (for immediate escalation only)

**MUST NOT** use:
- Personal email addresses
- Personal messaging applications (Slack, Teams, WhatsApp, etc.)
- Unencrypted HTTP connections
- Any channel not explicitly approved by the Security Operations Center (SOC)

### 1.2 Authentication Requirements
All agents **MUST** authenticate using:
- **Method**: OAuth 2.0 with mTLS
- **Token Lifetime**: Maximum 15 minutes for enumeration operations
- **Certificate Validation**: Strict hostname verification required
- **Multi-Factor Authentication**: Required for all initial connections

### 1.3 Response Time Requirements
| Operation Type | Maximum Response Time | SLA Breach Threshold |
|----------------|----------------------|---------------------|
| Initial Contact Acknowledgment | < 5 seconds | > 10 seconds | |
| Authorization Check | < 30 seconds | > 60 seconds |
| Execution Command | < 2 minutes | > 5 minutes |
| Reporting Submission | < 1 minute | > > 3 minutes |

**MUST** acknowledge receipt of all commands within the specified response time windows.

### 1.4 Escalation Procedures
Escalation **MUST** occur under the following conditions:
1. **Level 1 (Immediate)**: Connection failures, authentication errors
   - Action: Retry once after 30 seconds, then escalate to SOC on-call
2. **Level 2 (Critical)**: Command timeouts, execution failures
   - Action: Escalate within 5 minutes of first failure
3. **Level 3 (Severe)**: Data integrity issues, unauthorized access attempts
   - Action: Immediate escalation to Security Incident Response Team (SIRT)

**MUST** document all escalations with timestamp, error code, and remediation steps taken.

---

## 2. Operational Steps

### Step 1: Initial Contact

**Purpose**: Establish secure communication channel and verify agent identity.

**Procedure**:
1. Agent **MUST** initiate connection to primary channel using pre-provisioned credentials
2. Agent **MUST** include `X-Agent-ID` header with unique identifier
3. Agent **MUST** include `X-Session-Token` with valid OAuth token
4. Command Center **MUST** validate credentials within 5 seconds
5. Upon validation, Command Center **MUST** respond with session establishment confirmation

**RFC2119 Constraints**:
- **SHALL** use only approved communication channels
- **SHOULD** include all required headers in every request
- **MAY** request additional authentication factors if suspicious activity detected

**Expected Response Codes**:
| Code | Meaning | Action Required |
|------|---------|-----------------|
| 200 | Session established | Proceed to Step 2 |
| 401 | Authentication failed | Retry with correct credentials |
| 403 | Access denied | Escalate immediately |
| 500 | Server error | Log and escalate per Section 1.4 |

---

### Step 2: Authorization Check

**Purpose**: Verify agent permissions and scope of operation.

**Procedure**:
1. Agent **MUST** request authorization token for enumeration operations
2. Command Center **MUST** validate against access control list (ACL)
3. Authorization token **MUST** include:
   - Scope identifier (e.g., `enum-recon:read`, `enum-recon:write`)
   - Target system identifiers
   - Expiration timestamp (maximum 15 minutes)
4. Agent **MUST** store token securely in memory only
5. Agent **MUST NOT** persist tokens to disk or log files

**RFC2119 Constraints**:
- **SHALL** verify authorization before executing any enumeration command
- **SHOULD** request minimal privilege scope (principle of least privilege)
- **MUST NOT** assume implicit authorization based on previous successful operations

**Authorization Token Format**:
```json
{
  "scope": "enum-recon:read",
  "target_systems": ["sys-001", "sys-0022"],
  "expires_at": "2024-01-15T12:30:00Z",
  "issued_by": "soc-auth-service"
}
```

---

### Step 3: Execution

**Purpose**: Perform enumeration operations within authorized scope.

**Procedure**:
1. Agent **MUST** execute commands using provided authorization token
2. All commands **MUST** be logged with full context (timestamp, command, result)
3. Agent **MUST** handle errors gracefully and report to Command Center
4. Agent **MUST** terminate session upon completion or error condition
5. Agent **MUST** include `X-Session-ID` in all execution requests

**RFC2119 Constraints**:
- **SHALL** execute commands atomically where possible
- **SHOULD** implement retry logic with exponential backoff for transient failures
- **MUST NOT** exceed authorized scope or target unauthorized systems
- **MUST** sanitize output data before transmission to prevent information leakage

**Execution Command Format**:
```json
{
  "session_id": "sess-abc123",
  "command": "enumerate_ports",
  "parameters": {
    "target": "sys-001",
    "port_range": "1-1024"

  },
  "authorization_token": "<token>"
}
```

**Response Handling**:
| Status Code | Meaning | Action Required |
|-------------|---------|-----------------|
| 200 | Command executed successfully | Proceed with next command or terminate |
| 400 | Invalid parameters | Log error, do not retry without parameter correction |
| 403 | Unauthorized operation | Terminate session immediately and report |
| 500 | Internal server error | Retry once, then escalate if persists |

---

### Step 4: Reporting

**Purpose**: Submit results and close session securely.

**Procedure**:
1. Agent **MUST** compile all execution results into structured report
2. Report **MUST** include:
   - Session ID
   - Timestamps (start, end, duration)
   - Commands executed (with sanitized output)
   - Results summary
   - Any errors or anomalies encountered
3. Agent **MUST** submit report via primary channel within 1 minute of session completion
4. Command Center **MUST** acknowledge receipt and validate report integrity
5. Upon validation, Command Center **MUST** issue session termination confirmation

**RFC2119 Constraints**:
- **SHALL** include all required fields in every report
- **SHOULD** compress large result sets before transmission
- **MUST NOT** omit any execution details or error conditions
- **MUST** terminate session after successful reporting

**Report Format**:
```json
{
  "session_id": "sess-abc123",
  "status": "completed",
  "start_time": "2024-01-15T12:00:00Z",
  "end_time": "2024-01-15T12:05:00Z",
  "commands_executed": 15,
  "results_summary": {
    "ports_discovered": 42,
    "services_identified": 8,
    "vulnerabilities_flagged": 2
  },
  "errors_encountered": [],
  "anomalies_reported": []
}
```

---

## 3. Prohibitions

The following actions **MUST NOT** be performed under any circumstances:

### 3.1 Communication Prohibitions
- **MUST NOT** use personal email addresses for any operational communication
- **MUST NOT** use personal messaging applications (Slack, Teams, WhatsApp, Signal, etc.)
- **MUST NOT** communicate via unencrypted channels
- **MUST NOT** share credentials or tokens in any form of communication

### 3.2 System Access Prohibitions
- **MUST NOT** access systems outside authorized scope
- **MUST NOT** enumerate systems not listed in authorization token
- **MUST NOT** bypass authentication mechanisms under any circumstances
- **MUST NOT** attempt to access backup or recovery systems without explicit authorization

### 3.3 Authentication Bypass Prohibitions
- **MUST NOT** attempt to bypass authentication controls
- **MUST NOT** use stolen, leaked, or compromised credentials
- **MUST NOT** attempt credential harvesting or enumeration
- **MUST NOT** disable or modify authentication mechanisms

### 3.4 Data Handling Prohibitions
- **MUST NOT** store sensitive data locally on agent systems
- **MUST NOT** transmit unencrypted sensitive data
- **MUST NOT** share results with unauthorized personnel
- **MUST NOT** retain session data beyond required retention period

---

## 4. Compliance and Auditing

### 4.1 Audit Requirements
All agents **SHALL** maintain logs of:
- Connection attempts (successful and failed)
- Authorization requests and responses
- Command executions and results
- Error conditions and escalations

### 4.2 Review Schedule
- **Daily**: Automated review of all enumeration operations
- **Weekly**: SOC review of escalation events
- **Monthly**: Full audit of compliance with this SOP

### 4.3 Violation Reporting
Any suspected violations **MUST** be reported immediately to:
- Security Operations Center (SOC): `soc@ops.corp`
- Incident Response Team: `irt@ops.corp`

---

## 5. References

- RFC 2119 - Key Words for Use in RFCs to Indicate Requirement Levels
- OAuth 2.0 Specification (RFC 6749)
- TLS 1.3 Protocol Specification
- SOC Enumeration Operations Policy (SOP-ENUM-001)

---

*Document End*
