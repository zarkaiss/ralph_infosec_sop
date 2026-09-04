---
priority: MEDIUM
version: 1.0
last_updated: 2024-01-15
status: DRAFT
---

# Reconnaissance and Enumeration SOP - Step 1



## Table of Contents



- [Overview](#overview)

- [Target Identification](#target-identification)

    - [Scope Definition](#scope-definition)

    - [Reconnaissance Techniques](#reconnaissance-techniques)

    - [Target Validation](#target-validation)

- [Network Discovery](#network-discoveryco)

    - [Port Scanning](#port-scanning)

        - - [Scan Methodology](#scan-methodology)

        - [Service Enumeration](#service-enumeration)

        - [Constraints](#constraints)

    - [Asset Mapping](#asset-mapping)

        - [Documenting Discovered Assets](#documenting-discovered-assets-1)

        - [Technology Fingerprinting](#technology-fingerprinting)

- [RFC 2119 Constraints](#rfc--2119-constraints)

- [Deliverables](#delivera)



## Overview



This Standard Operating Procedure (SOP) outlines the systematic approach for conducting reconnaissance and enumeration activities during the initial phases of a penetration test or security assessment. The procedures described herein are designed to gather comprehensive information about target systems, networks, and applications while maintaining operational security and adhering to established ethical guidelines and legal frameworks.



The primary objectives of this phase include:



- **Information Gathering**: Collecting publicly available information data about the target organization

- **Attack Surface Mapping**: Identifying accessible entry points and potential vulnerabilities

- **Technology Identification**: Determining the technologies, software versions, and configurations in current use

- **Network Topology Understanding**: Building a mental model of network architecture and segmentation

- **Baseline Establishment**: Creating a reference point for subsequent vulnerability assessment



This document serves as a foundational guide for security professionals conducting authorized penetration testing engagements. All activities must be performed within the scope defined by written authorization Authorization and in compliance with applicable laws and regulations.



## Target Identification



Target identification is the critical first step in any reconnaissance operation. This phase establishes what systems, networks, and applications will be assessed and ensures that all subsequent activities remain within authorized boundaries.



### Scope Definition



Scope definition establishes the precise boundaries of the engagement and must be documented in writing before any testing begins. A well-defined scope prevents unauthorized access to out-of-scope assets and provides legal protection for both the assessment team and the client organization.



#### In-Scope Assets



In-scope assets are explicitly authorized for testing and include:



- **IP Address Ranges**: Documented CIDR blocks
- **Domain Names**: Fully qualified domain names (FQDNs)
- **Application Endpoints**: API paths, web applications, and services
- **Port Ranges**: Specific ports to be scanned or tested

#### Out-of-Scope Assets



Out-of-scope assets are explicitly excluded from testing and include:



- **Production Systems Not Authorized**: Critical infrastructure not included in scope
- **Third-Party Systems**: Unless explicitly authorized
- **Customer Data**: PII, PHI, or other sensitive data without proper authorization
- **Regulated Environments**: Healthcare (HIPAA), Finance (PCI-DSS) systems without specific approval



## Reconnaissance Techniques



Reconnaissance techniques are the methods used to gather information about target systems. These techniques range from passive to active and should be applied based on engagement rules and client requirements.



### Passive Reconnaissance



Passive reconnaissance involves gathering information without directly interacting with target systems:



- **OSINT (Open Source Intelligence)**: Searching public sources for information
- **DNS Enumeration**: Analyzing DNS records from public WHOIS databases
- **Subdomain Enumeration**: Using tools to discover subdomains from historical data
- **Technology Fingerprinting**: Identifying technologies from HTTP headers and footers

### Active Reconnaissance



Active reconnaissance involves direct interaction with target systems:



- **Port Scanning**: Identifying open ports and services
- **Service Version Detection**: Determining software versions running on targets
- **Vulnerability Scanning**: Checking for known vulnerabilities
- **Network Mapping**: Discovering network topology and segmentation



## Network Discovery



Network discovery focuses on understanding the target's network architecture and identifying accessible systems. This phase is critical for building a comprehensive attack surface model.



### Port Scanning



Port scanning is used to identify open ports and services resources on target systems. The scan methodology should be carefully selected based on:



- **Target Sensitivity**: More aggressive scans for less sensitive targets
- **Time Constraints**: Faster scans when time is limited
- **Detection Risk**: Stealthier scans when avoiding detection is important

### Scan Methodology



The following approaches are recommended:



- **TCP Connect Scan**: Standard full TCP handshake scan
- **SYN Scan (Half-Open)**: Less detectable, doesn't complete TCP handshake
- **UDP Scan**: For identifying UDP services
- **Stealth Scans**: Using timing and fragmentation to avoid detection

### Service Enumeration



Service enumeration identifies the specific applications running on open ports:



- **Banner Grabbing**: Collecting service banners and version information
- **HTTP Header Analysis**: Identifying web servers, frameworks, and configurations
- **SSL/TLS Fingerprinting**: Determining cipher suites and certificate details
- **Database Detection**: Identifying database instances and versions

### Constraints



Port scanning must adhere to the following constraints:



- **Rate Limiting**: Control scan speed to avoid overwhelming targets
- **Time Windows**: Perform scans during authorized time periods only
- **Protocol Restrictions**: Only scan protocols within scope
- **Evasion Techniques**: Use appropriate methods to avoid IDS/IPS detection when required



## Asset Mapping



Asset mapping involves documenting all discovered assets and their relationships. This creates a comprehensive inventory for subsequent phases of the engagement.



### Documenting Discovered Assets



All discovered assets should be documented with:



- **IP Addresses**: All identified IP addresses
- **Domain Names**: Associated domain names and subdomains
- **Service Information**: Open ports, services, and versions
- **Technology Stack**: Identified technologies and frameworks
- **Network Segments**: Subnets and network boundaries

### Technology Fingerprinting



Technology fingerprinting identifies the software stack running on discovered assets:



- **Web Servers**: Apache, Nginx, IIS, etc.
- **Application Frameworks**: React, Angular, Django, Flask, etc.
- **Database Systems**: MySQL, PostgreSQL, MongoDB, etc.
- **Operating Systems**: Linux distributions, Windows versions, etc.
- **Cloud Services**: AWS, Azure, GCP services and configurations



## RFC 2119 Constraints



All requirements in this SOP must adhere to RFC 2119 terminology:



- **MUST**: Absolute requirement
- **SHOULD**: Strong recommendation
- **MAY**: Optional behavior
- **NOT REQUIRED**: Not necessary
- **SHALL NOT**: Prohibited



## Deliverables



The following deliverables are expected from this phase:



- **Target List**: Complete list of authorized targets
- **Scope Document**: Written scope definition and authorization
- **Asset Inventory**: Discovered assets with metadata
- **Network Map Map**: Network topology diagram
- **Technology Report**: Technology stack analysis
- **Risk Assessment**: Initial risk evaluation based findings

## References



- [RFC 2119](https://tools.ietf.org/html/rfc2119) - Key words for use in RFCs to indicate requirement levels
- [OSINT Framework](https://www.osintframework.com/) - Open source intelligence resources
- [NIST SP 800-115](https://csrc.nist.gov/publications/detail/sp/800-115/final) - Technical Guide to Information Security



## Revision History



| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 2024-01-15 | Security Team | Initial draft version |
