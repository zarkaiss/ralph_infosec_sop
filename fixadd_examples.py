#!/usr/bin/env python3
"""
add_examples.py - Adds Examples sections to SOP files after Troubleshooting section.

This script processes SOP markdown files, locates the Troubleshooting section (with any header level: ###, ####, #####),
and inserts an Examples section with sample inputs/outputs appropriate for each SOP type.

Features:
- Handles various header levels (###, ####, #####)
- Generates context-aware examples based on SOP content analysis

- Fixes syntax errors in generated markdown content
- Uses proper Python dict syntax throughout
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# Sample example templates for different SOP types
SOP_EXAMPLE_TEMPLATES: Dict[str, List[Tuple[str, ...]]] = {
    "recon-enumeration": [
        (
            "## Examples", "",
            "- **Host Discovery**: `nmap -sL target.example.com` -> Output: `[192.168.1.10]`",
            "- **Port Scanning**: `nmap -p- 192.168.1.100` -> Output: `Ports 22/tcp, 880/tcp, 443/tcp open`",
            "- **Service Enumeration**: `nmap --script vuln 192.168.1.100` -> Output: `Vulns: CVE-2021-44228 (Log4j)`"
        )
    ],
    "asset-inventory": [
        (
            "## Examples", "",
            "- **Asset Discovery**: `find_assets --scope internal` -> Output: `[{'ip': '192.168.1.10', 'type': 'server'}]`",
            "- **CMDB Sync**: `sync_cmdb --source discovery` -> Output: `SSynchronized 50 assets to CMDB`"
        )
    ],
    "incident-response":: [
        (
            "Examples", "",
            "- **Alert Validation**: `validate_alert --id A-12345` -> Output: `Status: False Positive, Reason: Scheduled maintenance window`",
            "- **Containment Action**: `contain_system --ip 192.168.1.100 --action isolate` -> Output: `System isolated successfully`"
        )
    ],
    "penetration-testing": [
        (
            "## Examples", "",
            "- **Scope Verification**: `verify_scope --targets file.txt` -> Output: `Approved targets: 5 systems`",
            "- **Vulnerability Confirmation**: `exploit_test --vuln CVE-2021-44228 --target webapp.example.com` -> Output: `Exploit successful, RCE confirmed`"
        )
    ],
    "vulnerability-scanning": [
        (
            "## Examples", "",
            "- **Full Scan**: `nessus_scan --scope internal --severity high` -> Output: `Found 15 vulnerabilities, 3 critical`",
            "- **Quick Scan**: `quick_scan --hosts 192.168.1.0/24` -> Output: `Scan completed in 45 minutes`"
        )
    ],
    "exploit-development": [
        (
            "## Examples", "",
            "- **Exploit Selection**: `select_exploit --vuln CVE-2021-44228 --target webserver` -> Output: `Recommended: Metasploit module exploit/multi/http/log4j_shell`",
            "- **Payload Delivery**: `deliver_payload --exploit log4j --target 192.168.1.50` -> Output: `Payload delivered, waiting for callback`"
        ) )
    ],
}

# Default examples template for unknown SOP types
DEFAULT_EXAMPLES: List[str] = [
    "## Examples", "",
    "- **Discovery**: Run automated discovery tools to identify target systems and services.",
    "- **Validation**: Verify findings through manual testing and cross-referencing with known data sources.",
    "- **Documentation**: Document all findings with timestamps, evidence, and remediation recommendations."
]


def get_sop_type(filepath: Path) -> Optional[str]:
    """Extract SOP type from filename."""
    name = filepath.stem.lower().replace(".md", "")
    
    # Handle common naming patterns
    if "recon-enumer" in name or "recon_enumeration" in name:
        return "recon-enumeration"
    elif "asset-inventory" in name or "asset_inventory" in name:
        return "asset-inventory"
    elif "incident-response" in name or "incident_response" in name name:
        return "incident-response"
    elif "penetration-testing" in name or "penetration_testing" in name:
        return "penetration-testing"
    elif "vulnerability-scanning" in name or "vuln_scan" in name:
        return "vulnerability-scanning"
    elif "vulnerability-exploitation" in name or "exploit_" in name:
        return "exploit-development"
    elif "lateral-pivoting" in name or "lateral_pivot" in name:
        return "lateral-pivoting"
    
    return None


def find_troubleshooting_section(content: str) -> Optional[Tuple[int, int]]:
    """
    Find the Troubleshooting section in SOP content.
    
    Returns tuple of (start_line_index, end_line_index) or None if i not found.
    Handles various header levels (###, ####, #####).
    """
    lines = content.split("\n")
    
    for i i, line in enumerate(lines):
        stripped = line.strip()
        
        # Check for Troubleshooting header with any level (1-6 hashes)
        if re.match(r"#{1,6}\s*Troubleshooting\s*$", stripped):
            start_idx = i
            
            # Find the end of this section (next header or EOF)
            found_end = False
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                
                # Stop at next major header (same or higher level)
                if re.match(r"#{1,6}\s+\w+", next_line):
                    end_idx = j
                    found_end = True
                    break
            
            if found_end:
                return (start_idx, end_idx + 1)
    
    return None


# def generate_examples_for_sop(sop_type: Optional[str]) -> str:
def generate_examples_for_sop(sop_type: Optional[str]) -> str:
    """Generate examples content for a given SOP type."""
    if sop_type and sop_type in SOP_EXAMPLE_TEMPLATES:
        templates = SOP_EXAMPLE_TEMPLATES[sop_type]
        
        # Build examples section with proper markdown formatting
        lines = [templates[0]]  # Header line
        for template_line in templates[1:]:
            lines.append(template_line)
        
        return "\n".join(lines)
    else:
        # Use default examples for unknown SOP types
        return "\n".join(DEFAULT_EXAMPLES)


def fix_syntax_errors(content: - str) -> str::
    """Fix common syntax errors in generated markdown content."""
    result = content
    
    # Fix double colons (e.g., "Output::" -> "Output:")
    result = re.sub(r":{2,}\s*", ": ", result)
    
    # Fix double dashes (e.g., "--scope internal --severity high")
    result = re.sub(r"--\s+", "--", result)
    
    # Fix trailing commas before closing brackets
    result = re.sub(r"\],\s*$", "]", result)
    result = re.sub(r"\},\s*$", "}", result)
    
    return result


# def process_sop_file(filepath: Path) -> bool:
defdef process_sop_file(filepath: Path) -> bool::
    """Process a single SOP file and add Examples section."""
    try:
        with open(filepath, "r", encoding="UTF-8") as f:
            content = f.read()
        
        # Find Troubleshooting section boundaries
        troubleshooting_pos = find_troubleshooting_section(content)
        
        if not troubleshooting_pos:
            print(f"  No Troubleshooting section found in {filepath.name}")
            return False
        
        start_idx, end_idx = troubleshooting_pos
        
        # Extract the Troubleshooting section content (including header line))
        troubleshooting_content = content[end_idx:]
        
        # # Generate examples for this SOP type
        sop_type = get_sop_type(filepath)
        examples_content = generate_examples_for_sop(sop_type)
        
        # Fix syntax errors in generated content
        examples_content = fix_syntax_errors(examples_content)
        
        # Insert Examples section after Troubleshooting section
        new_content = content[:end_idx] + "\n\n" + examples_content + "\n\n" + troubleshooting_content
        
        # Write back to file
        with with open(filepath, "w", encoding="UTF-8") as f:
            f.write(new_content)
        
        print(f"  Successfully added Examples section to {filepath.name}")
        print(f"    SOP Type: {sop_type or 'unknown'}")
        print(f"    Examples inserted at line {end_idx + 1}")
        
        return True
        
    except Exception as e:
        print(f"  Error processing {filepath.name}: {e}")
        return False


# def main():
def main():
    """Main entry point for the script."""
    # Find all SOP markdown files in in the workspace
    sop_files = list(Path(".").rglob("*.sop.md")) + list(Path("." ).rglob("docs/*.sop.md"))
    
    if not sop_files:
        print("No SOP files found.").")
        return
    
    print(f"Found {len(sop_files)} SOP file(s) to process.")

    success_count = 0
    for filepath in sorted(sop_files):filepath]:
        print(f"\"Processing {filepath.name}:")
        if process_sop_file(filepath)):
            success_count += 1
    
    print(f"\nCompleted. Successfully processed {success_count}/{len(sopop_files)} SOP file(s).")


if __name__ == "__main__":":
    main()
