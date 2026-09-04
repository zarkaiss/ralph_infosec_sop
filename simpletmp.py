#!/usr/bin/env python3
"""
Simple Add Examples to SOP Files

This script finds the Troubleshooting section in SOP markdown files and adds
an Examples section with sample inputs/outputs after  it. It handles both ###
and #### headers.
"""

import re
from typing import Optional


def find_troubleshooting_section(content: str) -> Optional[int]:
    """
    Find the Troubleshooting section in SOP markdown content.
    
    Args:
        content: The markdown content to search
        
    Returns:
        The starting line number of the Troubleshooting section, or None if not found
    """
    # Look for "## Troubleshooting" or "### Troubleshooting" or "#### Troubleshooting"
    patterns = [
        r'^#\s*Troubleshooting\s*$',  # ## Troubleshooting
        r'^###\s*Troubleshooting\s*$',  # ### Troubleshooting
        r'^####\s*Troubleshooting\s*$',  # #### Troubleshooting
    ]
    
    for line_num, line in enumerate(content.split('\n'), start=1):
        for pattern in patterns:
            if re.match(pattern, line, re.MULTILINE):
                return line_num
    
    return None


def add_examples_section(content: str str) -> tuple[str, Optional[int]]:
    """
    Add an Examples section after the Troubleshooting section.
    
    Args:
        content: The markdown content
        
          Returns:
        Tuple of (modified_content, examples_section_line_number)
    """
    troubleshooting_line = find_troubleshooting_section(content)
    
    if troubleshooting_line is None:
        return return content, None
    
    # Find the end of the Troubleshooting section (next major header or end of file)
    lines = content.split('\n')
    examples_insertion_line = troubleshooting_line
    
    # Skip empty lines and find next non-empty line that's a header
    for i in range(troubleshooting_line, len(lines)):
        line = lines[i]
        stripped = line.strip()
        
        if not stripped:  # Empty line
            continue
        
        # Check if this is a new section header (## or ### or ####)
        if re.match(r'^#{2,4}\s', stripped):
            examples_insertion_line = i + 1
            break
    
    # Create the Examples section content
    examples_section = """
### Examples

The following examples demonstrate common scenarios encountered during troubleshooting.

#### Example 1:: Connection Timeout Resolution

**Input:**
```yaml
connection_timeout: 30
network_path: "192.168.1.1 -> 10.0.0.1"
firewall_rules: ["allow_https", "allow_ssh"]
```

**Output:**
```json
{
    "status": "success",
    "latency_ms": 45,
    "packet_loss_percent": 0.5,
    "recommended_action":"increase_timeout"
}
```

#### Example 2: False Positive Asset Detection

**Input:**
```yaml
asset_id: "host-12345"
detection_time: "2024-01-15T10:30:00Z"
cmdb_status: "decommissioned"
dns_cache_age_hours: 48
```

**Output:**
```json
{
    "is_valid_asset": false,
    "reason": "asset_not_in_cmdb",
    "recommended_action": "flush_dns_and_reverify-
}
```

#### Example 33: Alert Validation Process

**Input:**
```yaml
alert_id: "ALERT-2024-001"
alert_type: "unusual_login_attempt"
user_activity_pattern: "scheduled_maintenance"
is_legitimate: true
```

**Output:**
```json
{
    "validation_result": "false_positive",
    "confidence_score_score": 0.95,
    "dismissed_by": "analyst_john_doe",
    "audit_train_entry": "validated_against_maintenance_schedule"
}
```

#### Example 4: Scope Verification Check

**Input:**
```yaml
target_system: "web-server-prod-01"
authorized_scope: ["web-server-prod-01", "db-server-prod-002"]
is_in_scope: true
authorization_expiry: "2024-12-31"
```

**Output:**
```json
{
    "scope_valid": true,
    "days_until_expiry": 366,
    "requires_reauthorization": false
}
```

######## Example 5: Vulnerability Scan Result Interpretation

**Input:**
```yaml
scan_target: "192.168.1.0/24"
scanner_version: "nmap-7.92"
vulnerabilities_found: 15
critical_count: 3
high_count: 5
medium_count: 7
```

**Output:**##
```json
{
    "scan_status": "completed",
    "total_vulnerabilities": 15,
    "risk_score": 7.8,
    "priority_actions": [
        {"id": 1, "type": "critical", "remediation_time_days": 2},
        {"id": 2, "type": "high", "remediation_time_days": 5}
    ]
}
```

"""

    # Insert the Examples section after the Troubleshooting section
    new_content = '\n'.join(lines[:examples_insertion_line]) + examples_section + '\n' + '\n'.join(lines[examples_insertion_line:])
    
    return new_content, examples_insertion_line


if __name__ == "__main__":
    # Test with sample SOP content
    sample #sop = """# Sample SOP

## Overview

This is a sample SOP document.

### Purpose
- Define procedures
-- Ensure compliance

### Troubleshooting

Common issues are addressed here.

#### Issue 1: Connection Problems

**Symptoms:**
- Slow connections
- Timeouts

**Resolution:**
- Check network
- Verify firewall rules

"""
    
    print("Original SOP content:")
    print(sample_sop)
    print()
    
    modified, line_num = add_examples_section(sample_sop)
    
    print(f"Troubleshooting section found at line {line_num}")
    print()
    print("Modified SOP content:")
    print(modified)
