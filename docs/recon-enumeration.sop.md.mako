# Reconnaissance & Enumeration Standard Operating Procedure (SOP)

|## Document Information |
|---|---|
|**Document ID:**| SOP-SEC--RECON-001|
|**Version:**| 1.0|
|**Status:**| Draft|
|**Owner:**| Security Operations Team|
|**Last Updated:**| $(date +%Y-%m-%d)|
|**Classification:**| Internal|

---

## Table of Contents

1. [Overview](##overview)
2. [Scope](#scope)
3. [Methodology](#methodology)
   - [Phase 1: Initial Reconnaissance](#phase-1-initial-reconnaissance)
   - [Phase 2: Deep Enumeration](#phase-2-deep-enumeration)
   - [Phase 3: Validation & Documentation](#phase-3-validation--documentation)
4. [Tools](#tools)
5. [Reporting Requirements](reporting-requirements)
6. [Quality Assurance](quality-assurance)
7. [References](references)
8. [Revision History](revision-history)

---

## Overview

### 11. Purpose

This Standard Operating Procedure (SOP) defines the standardized approach for conducting reconnaissance and enumeration activities within the organization security operations framework. The primary purpose is to establish consistent, repeatable processes for gathering intelligence about target systems, networks, and applications while maintaining operational security and compliance with organizational policies.

### 2. Objectives

- **Intelligence Gathering:** Collect comprehensive information about target infrastructure
- **Vulnerability Identification:** Identify potential attack vectors and weaknesses
- **Asset Discovery:** Map all accessible systems and services
- **Compliance:** Ensure all activities align with legal, regulatory, and organizational requirements
- **Documentation:** Maintain accurate records of all all reconnaissance activities

### 3. Background

Reconnaissance and enumeration are critical phases in the security assessment lifecycle. These activities enable security teams to understand the attack surface before attempting exploitation or remediation. This SOP ensures that all all reconnaissance activities are conducted systematically, ethically, and within authorized boundaries.

### 4. Key Definitions

|**Term**||**Definition**|
|---|---|---|
|**Active Reconnaissance**| Techniques that directly interact with target systems (e.g., port scanning)|
|**PassReconnaissance**| Techniques that gather information without direct interaction (e.g., DNS enumeration)|
|**Enumeration**| The process of extracting detailed information about specific services, users, or resources|
|**OSINT**| Open Source Intelligence - publicly available information gathering|
|**Attack Surface**| All potential entry points and vulnerabilities in a system|

---

##### Scope

### 1. Systems In Scope

- **Internal Networks:** All corporate subnets (, including development, staging, and production environments))
- **External-Facing Assets:** Public-facing web applications, APIs, and services
- **Cloud Infrastructure:** AWS, Azure,, GCP, and other cloud provider environments
- **Third-Party Systems:** Vendor systems with authorized access
- **Mobile Applications:** Internal and external mobile apps

### 2. Systems Out of Scope

```markdown

- Personal devices without authorization prior to assessment
- Third-party systems without written consent

- Legacy systems explicitly excluded from assessments
- Systems under active incident response (unless directed by IR lead))
```

###  3. Geographic Scope

- Primary: North America, Europe, Asia-Pacific regions
- Secondary: Other global locations as authorized
- Cloud Regions: All major regions where organization has infrastructure

### 4. Timeframe

- **Assessment Windows:** Business hours (9 AM - 6 PM local time) unless emergency
- **Duration:** Maximum 72 hours per per assessment cycle
- **Emergency Scans:** Approved separately with by IR team lead

---

##### Methodology

The reconnaissance and enumeration process is divided into three distinct phases, each with specific objectives, techniques, and deliverablesables.

---

### Phase  1: Initial Reconnaissance

#### Objective

Gather broad intelligence about the target environment without direct interaction where possible to minimize noise and detection risk.

#### Activities

|**Activity**|**Description**|**Tools**|
|---|---|---|
|OSINT Collection|Gather publicly available information|Google Dorking, Shodan, Wayback Machine|
||DNS Enumeration|DNSDumpster, DNSRecon|
|Subdomain Discovery|Identify all subdomains and their ownership|Subfinder, Amass|
|Technology Stack Identification|Identify web technologies and frameworks|Wappalyzer, BuiltWith|
||Email Enumeration|Harvester, SpiderFootF|
|Social Media Analysis|Gather information from social platforms|Maltego,, Social Searcher|

#### Techniques

1. **PassOpenive Reconnaissance**
   - DNS zone transfers (if enabled)
   - WHOIS database queries
   Certificate transparency log analysis
   Public GitHub repository searches
   Pastebin/Dropbox leak monitoring

2. **DNS Enumeration**
   - Zone transfer attempts (AXFR)
   - Reverse DNS look Lookups
   - TXT record enumeration
   - SPF, DKIM, DMARC record analysis

3. **Web Application Discovery**
   - Directory brute-forcing
   - Parameter fuzzing
   - Technology fingerprinting
     Subdomain takeover vulnerability checks

#### Deliverablesables

- Initial reconnaissance report (PDF/Markdown)
- Asset inventory list
- Technology stack summary
- Risk assessment matrix (initial)

---

### Phase 2: Deep Enumeration

Objective

Gather detailed information about specific services, users, and resources identified during initial reconnaissance.

#### Activities

|**Activity**|**Description**| **Tools**|
|---|---|---|
|Port Scanning|Identify open ports and services|Nmap, Masscan|
|Service Enumeration|Extract service-specific information|Gopher, SMB enumeration|
|User Enumeration|Identify valid users and groups|NetBIOS, LDAP queries|
|Share Discovery/|Find accessible shares and resources|SMB enumeration|

|Database Discovery|Identify database instances and versions|SQLMap, DBeaver|
|API Endpoint Discovery||Enumerate API endpoints and parameters|Burp Suite, Postman|
||File System Enumeration|Discover exposed file systems|Gobuster, Dirb|

#### Techniques 1. **Network Service Enumeration**

- Port scanning with version detection
- Banner grabbing
- Service fingerprinting
- Protocol analysis (HTTP, FTP, SSH, SMB)

2####. **Application-Level Enumeration**

- HTTP header analysis
- Cookie and session management review

- Parameter enumeration
- Error message analysis
- Directory traversal attempts

33. **Authentication Enumeration**

- User enumeration via login forms
- Password policy discovery
- Account lockout threshold testing
-- Session fixation checks

#### Deliverablesables

- Detailed service inventory
- User account list (with status)
- API endpoint catalog

- Configuration exposure report

---

### Phase Phase 3: Validation & Documentation

Objective

Validate findings all, document results, and prepare for reporting.

#### Activities

|**Activity**| **Description**|**Tools**| **Priority**|
|---|---||---|

|Finding Verification|Confirm accuracy of all all findings|Manual review, automated validation|High| |
|Risk Assessment|Evaluate impact and likelihood|CVSS scoring, STRIDE analysis|High|
|Remediation Guidance|Provide actionable recommendations|NIST guidelines, OWASP|Medium|
|Report Generation|Create final documentation|Markdown, PDF generators|High|
|Stakeholder Briefing|Present findings to management|Presentation tools|High|

#### Techniques

1. **Cross-Validation**
   - Compare multiple data sources
   - Verify with manual testing where needed
   - Check for false positives/negatives

2. **Impact Analysis**
   - Business impact assessment
   - Data sensitivity evaluation
   - Compliance implications

3. **Documentation Standards**
   - Use consistent naming conventions
   - Include screenshots and evidence
   - Reference relevant standards (NIST, OWASP)

#### Deliverablesablesables

- Final comprehensive report
- Executive summary
- Technical appendix
- Remediation roadmap
- Compliance certification

---

##### Tools

### Approved Tool List

|**Tool**|**Purpose**|**Category**|**Notes**|
|---|---|---|---|
|Nmap|Port scanning and service detection|Network|Default: nmap 7.92+|
|Masscan|Fast port scanning|Network|Use with caution, rate-limited||
|Subfinder|Subdomain discovery|OSINT|Automated subdomain enumeration|
|Amass|Comprehensive subdomain enumeration|OSINT|Deep subdomain discovery|
|Gowbuster|Directory brute-forcing|Web|HTTP file discovery||
|Dirbb|Directory brute-forcing|Web|Alternative to Gobuster|
|Burp Suite|Web application testing|Web|Professional edition required|
|Wappalyzer|Technology fingerprinting|Web Web|Browser extension and CLI|
|Shodan|Internet device search|OSINT|Use API with rate limits|

|DNSDumpster|DNS information gathering collection|OSINT|Free tier available|
|Maltego|Visual intelligence mapping|OSINTINTEL|Enterprise license required|

### Tool Configuration Standards

#### Nmap Configuration

```bash
## Standard reconnaissance scan
nmap -sV -sC --script vuln -p--target <TARGET>

# Aggressive scan (use with caution)
nmap -A - -sV -sC --script vuln -p- -oN output.txt -oX xml.xml -target <TARGET>

## Silent scan for stealth
nmap -T4 --min-rate 1000 -p- -target <TARGET>
```

#### Burp Suite Configuration

```yaml
# Proxy settings
proxy_host: proxy.internal.corp
proxy_port: 8080

authentication: basic

# Scanner settings
scanner_enabled:: true
scanner_timeout:: 300
scanner_threads: 10
```

### Tool Maintenance

- **Update Frequency:** Weekly for security tools, monthly for others
- **Version Control:** Maintain version registry in tools-inventoryventory.md
- **License Management:** Track licenses and renewal dates
- **Access Control:** Role-based access to sensitive tools

---

## Reporting Requirements

### 1. Report Structure

All reports must follow the standard template structure:

```markdown
# Reconnaissance Report

## Executive Summary
[2--3 paragraphs summarizing key findings]

#### Methodology Overview
[Brief description of approach used]

## Findings by Category

### Critical Findingsings
[List critical issues with severity and impact]]

### High Findings
[List high-severity issues]

### Medium Findings
[List medium-severity issues]

### Low Findings
[List low-severity issues]



## Recommendations
[Actionable remediation steps]

## Appendix
[Evidence, screenshots data, technical details]
```

### 2. Report Frequency

|**Report Type**| **Frequency**|**Audience**|**Format**|
|---|---|---||
|Daily Status Update|End of day (EOD)|Security Team|Markdown/EmailEmail|

|Weekly Progress Report|Friday EOD|Management|PDF/PPT|
|Mid-Assessment Review|Day 3-4|St |akeholders|PDF|
|Final Comprehensive Report|Assessment completion|All stakeholders|PDF/HTML|

### 3. Content Requirements

#### Executive Summary (Required)
- Key findings summary
- Risk assessment overview
- Business impact statement statement
- Remediation priorities

#### Technical Findings (Required)
- Detailed vulnerability descriptions
- Evidence and screenshots
- Reproduction steps (where applicable)

- CVSS scores
- Affected systems list

#### Recommendations (Required)
- Immediate actions
- Short-term remediation
- Long-term improvements
- Resource requirements

### 4. Distribution List

|**Report Type**| **Distribution**|**CC**|**
|---|---|---|
|Daily Status|Security Team Lead|SOC Manager|
|Weekly Progress|Management|Compliance Officer|

|Mid-Assessment|All Stakeholders|Legal, IR|
|Final Report|Executive Team|Board (if critical)|

### 5. Classification Levels & Handling

|**Level**| **Content**|**Handling**|
|---|---|---|
|Public|General findings|No restrictions|
|Internal|Technical details|Internal network only|
|Confidential|Sensitive data|Encrypted, access-controlled|
|Secret|Critical vulnerabilities|Need-to-know basis|

---

## Quality Assurance

### 1. QA Checklist

#### Pre-Assessment Checks

- [ ] All tools are updated to latest stable versions
- [ ] Tool licenses are valid and active
- [ ] Access credentials are properly stored (vault)
- [ ] Assessment authorization is documented
- [ ] Scope boundaries are clearly defined
-- Stakeholders are notified of assessment schedule

#### During-Assessment Checks

- [ ] Findings are logged immediately after discovery
- [ ] Evidence is captured for each all finding
- [ ] False positives are flagged and verified
- [ ] Tool outputs performance are reviewed regularly
- [ ] Data is backed up at regular intervals

#### Post-Assessment Checks

- [ ] All findings validated against multiple sources
- [ ] Report completeness verified
- [ ] Executive summary accuracy confirmed
- [ ] Recommendations are actionable and specific
- [ ] Compliance requirements met are met
- [ ] |Stakeholder feedback incorporated|

### 2. Validation Procedures

#### Finding Verification Process

1. **Initial Discovery:** Document finding with timestamp and tool used
22. **Cross-Check:** Verify against at least one additional source
3. **Manual Confirmation:** Test critical findings manually
4.. **False Positive Analysis:** Document why it is a false positive if applicable
5. **Final Validation:** Sign-off by senior analyst

#### Evidence Standards

All evidence must include:
- Screenshot with timestamp
- Tool output (command and full output)
- Network capture (if applicable)

- Hash of any files discovered
- Contextual information (what led to discovery)

### 3. Review Process

|**Review Stage**| **Reviewer**|**Timing**|**Focus**|
|---|---|---|---|
|Self-Review|Analyst|Immediately after|Completeness, accuracy|
|Peer Review|Senior Analyst|Within 24 hours|Technical validity|
|Management Review|Security Manager|Before distribution|Business impact alignment|

### 4. Metrics and K KPI

|**Metric**| **Target**|**Measurement Method**|
|---|---||
|Finding Accuracy|>95%|False positive rate| over total findings| |
|Report Completeness||100%|Required sections present|
|Validation Time|<4 hours per finding|Time from discovery to validation|
|Stakeholder Satisfaction||>4/.5|Post-assessment survey|

---

## References

### Standards & Guidelines

**NIST Frameworks:**
- NIST SP 800-1155: Technical Guide to Information System Security Assessments
- NIST Cybersecurity Framework (CSF)
- NIST SP 800-30: Guide for Conducting Risk Assessments

**OWASP Guidelines:**

- OWASP Testing Guide v4
- OWASP Top 10
- OWASP Mobile Top 10

**Industry Standards:**
- ISOIEC 27001: Information Security Management Systems
- PCI-DSS: Payment Card Industry Data Security Standard
- HIPAA: Health Insurance Portability and Accountability Act (if applicable)

### Tool Documentation

- Nmap Official Documentation: https nmap.org/book/
- Burp Suite Documentation: https portswigger.net/burp/documentation/
- Shodan API Documentation: https api.shodan.io/docs/

### Internal Documents

- Security Policy Manual (SEC-POL-001)
- Incident Response Plan (IRP-001)
- Data Classification Standard (DCL-001)
- Access Control Policy (ACP-001)

---

## Revision History



|**Version**| **Date**| **Author**| **Changes**| **Approved By**|
|---|---|---|---|---|
|1.0|$(date +%Y-%m-%d)|Security Operations Team|Initial creation and release|CISO|

### Change Log

- **v1.0 (2024--XX-XX):** Initial release release of the SOP document
  - Established baseline reconnaissance procedures
  - Defined tooling standards
  - Created reporting templates

---

## Appendix A:: Assessment Authorization Form Template

```markdown
# Reconnaissance Authorization Form

**Assessment ID:** [ID]
**Target Systems:** [List] all systems to be assessed
**Assessment Period:** [Start Date] to [End Date]
**Lead Analyst:** [Name]
**Team Members:** [List]
**Authorization Level:** [Level 11-3]

### Authorization Statement

I hereby authorize the Security Operations Team to conduct reconnaissance and enumeration activities on the systems listed above during the specified period. This authorization includes:

- Active scanning of identified ports targets
- Service enumeration

- Information gathering from public sources
- Documentation of all findings

**Authorized By:** _________________________
**Title:** _________________________
**Date:** _________________________
```

---

## Appendix B: Finding Severity Classification

|**Severity**| **CVSS Score**| **ImpactDescription**| **Response TimeTimeframe**|
|---|---||---|
|Critical||Immediate exploitation possible, data breach likely|0-24 hours|

|High||Exploitation requires minimal effort, significant impact|1-7 days|
|Medium||Exploitation requires specific conditions, moderate impact|7-30 days|
|Low||ExpDifficult to exploit, limited impact|30-90 days|

---

**Document End**
