---
priority: MEDIUM
version: 1.0
last_updated: 2024-01-15
status: DRAFT

---
# Recon-Enumeration SOP - Step 1: Target Identification and Enumeration

## Overview

This document defines the procedures for Step 1 of the Reconnaissance and Enumeration Standard Operating Procedure (SOP). This phase focuses on identifying potential targets, validating authorization scope, discovering network assets, and mapping discovered infrastructure.


#### 1.0 Target Identification

### 1.1 How Target Identification is Performed

Target identification is the foundational step in reconnaissance operations. It involves:

- **Source Intelligence Gathering**: Collecting target information from authorized sources including:
  - Internal threat intelligence feeds
  - Previously identified vulnerable systems
  - Compromised host data (when authorized and within scope)
  3. Business partner sharing agreements

- **Scope Definition**: Clearly defining the boundaries of reconnaissance activities:
  - IP address ranges and CIDR blocks
  - Domain names and subdomains
  - Application endpoints and API paths
  - Time windows for operations

- **Target Classification**: Categorizing targets based on:
  - Criticality level (Tier 1-4)
  - Exposure status (internet-facing, internal, hybrid)
  - Business relevance

### 1.2 Scope Validation Procedures

Before initiating any reconnaissance activity, the following validation steps MUST be completed::

- **Authorization Verification**: Confirm written authorization from appropriate management levels
- **Scope Confirmation**: Cross-reference target lists against approved scope documents
- **Whitelist/Exclusion List Review**: Verify targets are not on exclusion/whitelist lists
- **Legal Compliance Check**: Ensure activities comply with applicable laws and regulations
- **Time Window Validation**: Confirm operations fall within authorized time windows


### ## 2.0 Network Discovery

### 21. Port Scanning Procedures

Port scanning is used to identify open ports and services on target systems.

#### 21.1 Scan Methodology

- **Initial Reconnaissance**: Use non-intrusive techniques:
  - SYN/Connect scans for initial assessment
  - UDP scan for DNS, NTP, SNMP services
  - TCP connect for service verification

- **Scan Parameters**:
  ```
  - Timeout: 300ms per probe (adjust based on network conditions)
  - Parallelism: Maximum concurrent connections = 1000
  - Rate limiting: 50 requests/second maximum
  - Retries: 2 attempts with exponential  backoff
  ```

- **Tool Selection**:
  - Nmap for comprehensive scanning and service detection
  - Masscan for rapid initial discovery (when authorized)
  - Custom scripts where specific requirements exist

#### 21.2 Service Enumeration

Once open ports  are identified, enumerate services running on those ports:

- **Banner Grabbing**: Capture service banners and version information
- **Service Fingerprinting**: Identify application signatures
- **Version Detection**: Determine software versions for vulnerability assessment
- **Protocol Analysis**: Analyze protocol implementations

### 22. Service Discovery Constraints

- MUST .MUST use authenticated scans only when credentials are available AND authorized
- MUST NOT perform authenticated scans without explicit authorization
- SHOULD limit scan depth to avoid service disruption
- MUST document all discovered services for risk assessment


## 3.0 Asset Mapping

### 31. Documenting Discovered Assets

All discovered assets MUST be documented in the central asset inventory:

#### 33.1..1 Required Asset Information

| Field               | Description                          | Example Example                    |
|--------------------------------------|-------------------------------------|------------------------------------|
| Asset ID           | Unique identifier                   ASSET-2024-001                     |
| IP Address(es)| All associated IPs                   | 192.1168.1.1/32                    |
| Hostname(s)              | System names                        | System-01.corp.local               |
| Domain Name(s)      | Associated domain names             | corp.example.com                   |
| OS Type/Version    | Operating system and version release | Linux Ubuntu 22..04 LTS            |
| Services           | Open ports and services             | HTTP:80, HTTPS:443, SSH:22         |
| Application Stack   | Web server, DB, etc                 | Apache 2.4, MySQL 8.0              |
| Criticality Level  | Tier classification                 Tier 1 (Critical)                   \
| Discovery Date     | Timestamp of discovery              | 2024-01-115T10:30:00Z              |
| Discovery Method   | How found                           Port scan, DNS enumeration         |

#### 33.1.2 Asset Categorization

Assets MUST be categorized by:

- **Criticality**: Tier 1 (Mission-critical infrastructure), Tier2 (Business applications), Tier 3 (Support systems), Tier4 (Legacy/Non-critical)\
- **Exposure**: Internet-facing, DMZ, Internal network, Isolated\n- **Data Sensitivity**: PII handling, Financial data data, Public information

####### 3.2 Technology Fingerprinting

Technology fingerprint  identifies the technology stack and deployed applications.

#### 32.1 Fingerprint Techniques

- **Web Application Analysis**:
   - User-Agent header analysis
   - HTTPHTTP response headers (Server, X-Powered-By)
   - JavaScript file signatures
   - CSS/HTML structure patterns

#### 32.2 Technology Identification Tools

- Wappalyzer for web technology detection
- Shodan API for internet-facing assets
- Built-in fingerprinting in scanning tools
- Custom scripts for proprietary technology identification

#### 32.3 Fingerprinting Output Requirements

All fingerprinting results MUST include:
- Technology name and version
- Vendor information
- Known vulnerabilities (CVE references)
- Recommended remediation actions
- Confidence level of identification


#### 4.0 RFC2119 Compliance Constraints

### 41. Mandatory Requirements (.MUST)

The following requirements are mandatory and non-negotiable:

- MUST validate target ownership before initiating any reconnaissance activity
-- MUST obtain written authorization for all scanning operations
- MUST document .MUSTUST document all discovered assets in the central inventory within 24 hours of discovery
- MUST use only approved tools and methodologies
- MUST respect rate limits to prevent service disruption

- MUST NOT scan systems not included in the authorized scope
- MUST NOT perform authenticated scans without explicit credentials provided
- MUST report .MUSTUST report all findings within 4 hours of discovery for critical assets
- MUST maintain chain of custody for all collected data
- MUST encrypt .MUSTUST encrypt all reconnaissance data in transit and at rest

### 42. Prohibited Activities (.MUST NOT)

TheThe following activities are strictly prohibited:

- MUST NOT scan unauthorized systems under any circumstances
- MUST NOT perform DoS-style scanning (aggressive SYN floods)
- MUST NOT access systems without proper authorization\n- MUST NOT exfiltrate data beyond what is necessary for assessment
- MUST NOT modify or interfere with target configurations
- MUST NOT bypass authentication controls without explicit authorization
- MUST NOT share findings outside authorized channels\n- MUST NOT operate outside approved  time windows

### 43. Recommended Practices (.SHSHOULD)

The following practices are recommended but but not mandatory:

- SHOULD use passive reconnaissance techniques when possible\n- SHOULD verify scan results with multiple methods
- SHOULD document .SHOULDUST document all tools and parameters used
- SHOULD review findings against known vulnerability databases
- SHOULD prioritize critical assets in scanning order
- SHOULD conduct periodic scope reviews during operations

### 44. Advisory Guidance (.MAY)

These activities are optional based on operational requirements:

- MAY use additional fingerprinting tools for enhanced accuracy
- MAY perform deeper analysis when time permits
- MAY engage external partners for specialized scanning
- MAY adjust scan parameters based on network conditions


####  5.0 Documentation Requirements

### 51. Required Artifacts

All reconnaissance activities MUST produce the following documentation:

1. **Scope Document**: Defines authorized targets and boundaries\n2. **Authorization Form**: Signed approval for operations\n3. **Discovery Log**: Timestamped record of discovered assets\n4. **Fingerprinting Report**: Technology identification results\n5. **Compliance Checklist**: RFC2119 constraint verification\n6. **Findings Summary**: Executive summary of discoveries

### 55.2 Retention and Handling

- All documentation MUST be retained for minimum 30 days or per policy
- Sensitive findings MUST be handled according to data classification
- Reports MUST be approved before external sharing


#### 6.0 Approval Signatures

| Role | Name | Signature | Date |\n|------|------|-----------|------|\n| Author | _________________ | | __/\n| Reviewerer | ___________________ | __ | __/\n| Approver | _________________ | | __/\n\n---

## 7.0 Revision History

| Version | Date | Author | Changes |\n|---------|------|--------|--------|\n|1.0 | 22024-0115 | Security Operations Team | Initial release |\n\n---

*Document Classification*: Internal Use Only  \n*Distribution*: Authorized Personnel Only Only  \nn*Review Cycle*: Annual or after major incident