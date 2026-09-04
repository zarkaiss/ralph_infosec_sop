# Reconnaissance & Enumeration Standard Operating Procedure (SOP)

## 1. Overview

### Purpose

Reconnaissance and enumeration are foundational phases in cybersecurity operations that enable security professionals to systematically gather information about target systems, networks, and applications. This SOP establishes standardized procedures for conducting authorized information gathering activities to:

- **Identify attack surface**: Discover exposed assets, services, and potential entry points
- **Assess vulnerability landscape**: Map known vulnerabilities associated with identified technologies
- **Support threat intelligence**: Correlate findings with known threat actor TTPs (Tactics, Techniques, and Procedures)
- **Enable proactive defense**: Inform security posture improvements before exploitation occurs
- **Facilitate incident response**: Provide context for understanding attack vectors during investigations

### Key Objectives

| Objective | Description |
|-----------|-------------|
| Asset Discovery | Identify all systems, services, and applications within scope |
| Service Enumeration | Determine open ports, running processes, and exposed services |
| Technology Fingerprinting | Identify software versions, frameworks, and configurations |
| Network Mapping | Document network topology and connectivity relationships |
| Credential Harvesting (Authorized) | Collect valid credentials for penetration testing engagements |

### Risk Considerations

- **Data Privacy**: All gathered information must be handled according to data protection regulations (GDPR, CCPA, etc.)
- **Legal Compliance**: Activities must remain within the bounds of authorized scope and written permission
- **Operational Security**: Reconnaissance activities should not trigger defensive mechanisms or alert security teams
- **Evidence Preservation**: Maintain chain of custody for all collected artifacts

---

## 2. Scope Definition

### In-Scope Assets

The following categories define what assets and information are targeted during reconnaissance and enumeration:

#### Network Infrastructure
```yaml
network_scope:
  - ip_ranges:
      - "10.0.0.0/8"
      - "172.16.0.0/12"
      - "192.168.0.0/16"
  - dns_zones:
      - "*.example.com"
      - "*.internal.example.org"
  - subdomains:
      - All registered subdomains from DNS records
```

#### Application Layer
- Web applications (HTTP/HTTPS)
- API endpoints and services
- Mobile application backends
- Cloud infrastructure configurations

#### Identity & Access
- User accounts and groups
- Active Directory/LDAP structures
- Authentication mechanisms
- Session management systems

### Out-of-Scope Assets

The following are explicitly excluded from reconnaissance activities:

- Third-party vendor systems without written authorization
- Systems marked as "critical" in the asset inventory without special approval
- Personally identifiable information (PII) beyond what's necessary for security assessment
- Customer data and proprietary business information

### Authorization Requirements

All reconnaissance activities require:

1. **Written Scope Document** signed by authorized stakeholders
2. **Rules of Engagement (RoE)** defining timing, methods, and constraints
3. **Legal Review** confirming compliance with applicable laws and regulations
4. **Emergency Contact List** for immediate escalation if issues arise

---

## 3. Methodology

### Phase 1: Passive Reconnaissance

Passive reconnaissance gathers information without directly interacting with target systems, minimizing detection risk.

#### 3.1 DNS Enumeration

```bash
# WHOIS lookup for domain registration details
whois example.com

# DNS record enumeration
dig example.com ANY
nslookup -type=ALL example.com

# Subdomain discovery via DNS records
subfinder -d example.com
amass enum -target example.com -silent
```

#### 3.2 Certificate Analysis

```bash
# SSL certificate inspection
openssl s_client -connect target.example.com:443 -showcerts

# Extract certificate information
echo | openssl s_client -connect target.example.com:443 -servername target.example.com 2>/dev/null | openssl x509 -noout -text
```

#### 3.3 Search Engine Discovery

- Google Dorking for exposed files and directories
- Shodan/Censys for internet-facing assets
- Wayback Machine for historical configuration data

### Phase 2: Active Reconnaissance

Active reconnaissance involves direct interaction with target systems to gather detailed information.

#### 4.1 Port Scanning

```bash
# TCP port scanning with timing considerations
nmap -sT -p- --min-rate=50 -oN scan-output.txt target.example.com

# Service version detection
nmap -sV -sC -p- --open target.example.com

# OS fingerprinting
nmap -O --script os-detect target.example.com
```

#### 4.2 Service Enumeration

```bash
# SMB enumeration (Windows)
smbclient -L //target.example.com/share -N

# SSH banner grabbing
ssh -o BatchMode=yes -o ConnectTimeout=5 user@target.example.com

# HTTP service fingerprinting
curl -I http://target.example.com/
nikto -h http://target.example.com/
```

#### 4.3 Directory & File Discovery

```bash
# Directory brute-forcing
gobuster dir -u http://target.example.com/ -w /path/to/wordlist.txt

# Sensitive file detection
ffuf -u http://target.example.com/ -w /path/to/sensitive-files.txt

# Git repository discovery
git-dumpster https://target.example.com/repo.git
```

### Phase 3: Enumeration Techniques

#### 5.1 User Enumeration

```bash
# Username enumeration via login attempts
hydra -l user -P /path/to/passwords.txt ssh://target.example.com/

# LDAP enumeration
ldapsearch -x -H ldap://target.example.com -b dc=example,dc=com "(objectClass=*)"

# Active Directory enumeration
enum4linux -a target.example.com
```

#### 5.2 Service-Specific Enumeration

| Service | Enumeration Tool | Command Example |
|---------|------------------|-----------------|
| SMB | enum4linux | `enum4linux -a target` |
| SNMP | snmpwalk | `snmpwalk -c public -v1 target.example.com` |
| Redis | redis-cli | `redis-cli -h target -p 6379 ping` |
| MongoDB | mongo | `mongo --host target --eval "db.serverStatus()"` |
| Elasticsearch | curl | `curl http://target:9200/_cat/indices?v` |

#### 5.3 Technology Fingerprinting

```bash
# WAF detection
wafw00f -u http://target.example.com/

# Framework detection
whatweb http://target.example.com/

# CMS detection
cmsmap -t http://target.example.com/
```

### Phase 4: Data Collection & Analysis

#### 6.1 Information Organization

All collected data must be organized in a structured format:

```yaml
recon_report:
  target: "example.com"
  scan_date: "2024-01-15"
  findings:
    dns_records:
      - record_type: "A"
        value: "192.168.1.1"
        ttl: 3600
    open_ports:
      - port: 80
        service: "http"
        version: "nginx/1.18.0"
    vulnerabilities:
      - cve_id: "CVE-2024-XXXXX"
        severity: "HIGH"
        description: "..."
```

#### 6.2 Documentation Standards

All reconnaissance activities must be documented with:

- Timestamp of each action
- Tool and version used
- Parameters and options applied
- Raw output preserved in evidence folder
- Analysis notes and conclusions

### Phase 5: Reporting & Escalation

#### 7.1 Report Structure

```markdown
# Reconnaissance Report

## Executive Summary
[High-level findings and risk assessment]

## Methodology
[Tools, techniques, and authorization references]

## Findings
### Critical
[List of critical vulnerabilities and exposures]

### High
[List of high-severity issues]

### Medium
[List of medium-severity issues]

### Low/Informational
[List of informational findings]

## Recommendations
[Prioritized remediation steps]

## Appendices
- Raw scan outputs
- Evidence collection logs
- Tool configurations used
```

#### 7.2 Escalation Procedures

| Severity Level | Response Time | Escalation Path |
|----------------|---------------|-----------------|
| Critical | Immediate (< 1 hour) | CISO, Legal, IR Team |
| High | < 4 hours | Security Manager, Engineering Lead |
| Medium | < 24 hours | Security Analyst Team |
| Low/Info | Next business day | Standard reporting cycle |


## 4. Compliance & Best Practices

### Tool Usage Guidelines

- Use only approved tools from the organization's security toolkit
- Maintain toolchain integrity and verify signatures
- Document all tool versions for reproducibility
- Never use tools that could cause denial of service

### Data Handling Requirements

- Encrypt all collected data at rest and in transit
- Store sensitive information in secure, access-controlled repositories
- Implement data retention policies aligned with legal requirements
- Redact PII before sharing reports externally

### Continuous Improvement

- Review SOP effectiveness quarterly
- Incorporate lessons learned from incidents
- Update tooling based on threat landscape changes
- Conduct regular training on new reconnaissance techniques


## 5. References

- [NIST SP 800-115](https://csrc.nist.gov/publications/detail/sp/800-115/final) - Technical Guide to Information Security Testing and Assessment
- [OWASP Reconnaissance](https://owasp.org/www-project-web-security-testing-guide/) - Web Application Security Testing Guide
- [MITRE ATT&CK](https://attack.mitre.org/) - Knowledge base of adversary TTPs
- [CWE Top 25](https://cwe.mitre.org/data/top25.html) - Common Weakness Enumeration


*Document Version: 1.0*  
*Last Updated: $(date +%Y-%m-%d)*  
*Classification: INTERNAL USE ONLY*  
*Approved By: Security Operations Team*
