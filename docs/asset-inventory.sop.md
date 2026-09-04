---
priority: MEDIUM
version: 1.0
last_updated: 2024-01-15
status: FINAL
---
# Asset Inventory SOP

## Agent Interaction Protocol

This section documents the mandatory interaction protocols that agents MUST follow when communicating with users during asset inventory operations. All procedures adhere to RFC2119 keyword constraints for clear compliance verification.

### Header Section - Communication Requirements

#### Agent Communication Channels (MUST)
- **MUST** use designated secure communication channels for all user interactions interactions
- **MUST** verify channel authorization before transmitting sensitive information
- **MUST NOT** use unauthorized or unencrypted communication methods
- **SHOULD** maintain encrypted channels for all data exchanges

#### User Authentication Requirements (MUST)
- **MUST** verify user identity before processing any requests
- **MUST** validate credentials against authorized authentication systems
- **MUST** reject requests from unauthenticated users immediately
- **MAY** request additional verification methods for high-risk operations

#### Response Time Expectations (SHOULD)
- **SHOULD** respond to user inquiries within 15 minutes during business hours
- **SHOULD** acknowledge receipt of all requests within 5 minutes
- **MUST** provide status updates at minimum every 30 minutes for ongoing operations
- **MAY** extend response times for complex operations with documented justification

#### Escalation Procedures (MUST)
- **MUST** escalate sensitive requests to supervisor immediately upon identification
- **MUST** document all escalation actions with timestamps and rationale
- **MUST NOT** proceed with sensitive operations without proper authorization
- **SHOULD** notify relevant stakeholders within 10 minutes of escalation


## Procedure

### Step Documentation - Interaction Protocols

#### Step 1: Initial Contact (
**Purpose**: Establish secure communication channel and identify user intent.

**Requirements:**
- **MUST** identify user intent immediately upon contact
- **SHOULD** request explicit authorization before proceeding with any operations
- **MUST** verify the requesting party's identity and role
- **MAY** provide templated introduction messages for standard engagements
- **MUST NOT** proceed without confirmed authorization

**Actions:**
1. Greet user and confirm identity verification status
2. Request and validate scope of work authorization
3. Document initial contact timestamp and communication channel
4. Confirm understanding of operational boundaries


#### Step 2: Authorization Check (
**Purpose**: Validate credentials and ensure proper authorization before execution.

**Requirements:**
- **MUST** validate all credentials against authorized systems
- **MAY** request additional verification for elevated privilege operations
- **MUST** reject requests lacking proper authorization documentation
- **SHOULD** cross-reference with engagement plan and scope documents
- **MUST NOT** bypass authentication controls under any circumstances

**Actions:**
1. Verify user credentials against identity management system
2. Cross-check authorization levels with required permissions
3. Document validation results in audit trail
4. Request additional verification if authorization is unclear
5. Escalate to supervisor if authorization cannot be validated


#### Step 3: Execution (
**Purpose**: Conduct asset inventory operations following approved procedures.

**Requirements:**
- **MUST** follow all approved procedures and documented workflows
- **SHOULD** document all actions taken with timestamps and details
- **MUST** maintain audit trails of all interactions and operations
- **MAY** use templated responses for common queries and standard operations
- **MUST NOT** engage in unauthorized data collection activities
- **MUST NOT** collect data outside defined scope boundaries

**Actions:**
1. Execute inventory scanning according to approved methodology
2. Document each step with relevant metadata and timestamps
3. Record any deviations from standard procedure with justification
4. Maintain real-time audit trail of all operations
5. Flag any unexpected findings for review


#### Step 4: Reporting (
**Purpose**: Provide comprehensive status updates and recommendations.

**Requirements:**
- **MUST** provide status updates at regular intervals during operations
- **MAY** include recommendations for improvement in final reports
- **MUST** document all findings with supporting evidence
- **SHOULD** highlight critical issues requiring immediate attention
- **MUST** ensure all reports meet compliance documentation requirements

**Actions:**
1. Compile inventory results with complete metadata
2. Document any anomalies or unexpected findings
3. Provide status summary to stakeholders
4. Include recommendations for remediation where applicable
5. Submit final report through approved channels


## Troubleshooting

This section addresses common issues encountered during asset inventory operations. Operators MUST review this section when encountering unexpected results or operational failures.

### False Positive Asset Detections

**Definition**: Identification of assets that do not exist, are decommissioned, or belong to out-of-scope environments.

**Causes and Mitigations**:
- **Network scanning artifacts**: Scanners MAY detect ephemeral services (e.g., Docker containers, temporary daemonsema) that close immediately after detection. Operators SHOULD verify asset persistence by cross-referencing with CMDB records within 24 hours of discovery.
- **DNS cache pollution**: Stale DNS records MAY cause detection of decommissioned hosts. Operators MUST flush local DNS caches and verify against authoritative sources before documenting assets.

### Connection Issues During Scanning

**Definition**: Interruptions in scanning operations due to network or infrastructure issues.

**Resolution Steps**:
- **MUST** validate network connectivity before resuming operations
- **SHOULD** implement retry logic with exponential backoff for transient failures
- **MAY** adjust timeout parameters based on observed network conditions
- **MUST** document all connection issues and resolutions in audit trail

### Authentication Failures

**Definition**: Inability to authenticate against target systems during inventory.

**Resolution Steps**:
- **MUST** verify credentials are current and properly formatted
- **SHOULD** attempt alternative authentication methods if available
- **MAY** request credential refresh from system administrators
- **MUST NOT** attempt brute force or unauthorized access attempts
- **MUST** escalate to supervisor if authentication issues persist


## Compliance Notes

This SOP adheres to RFC 2119 terminology standards where:
- **MUST** indicates a requirement that is essential to the correct implementation (RFC 2119 Section: "must" or "shall")
- **SHOULD** indicates a recommendation that is generally considered best practice (RFC 2119 Section: "should")
- **MUST NOT** indicates a prohibition that must never be violated (RFC 2219 Section: "must not" or "shall not")
- **MAY** indicates an optional action that is permitted but not required (RFC 2119 Section: "may")

All agents MUST comply with these constraints to maintain operational integrity and regulatory compliance.









priority: MEDIUM
version: 1.0
last_updated: 2024-01-15
status: FINAL
