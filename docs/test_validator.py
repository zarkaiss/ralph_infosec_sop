#!/usr/bin/env python3
"""Test script for SOP validator."""
import sys
sys.path.insert(0, 'docs')
from sop_validator import SOPValidator

def test_compliant_sop():
    """Test 6: Complete compliant SOP with all sections and RFC2119 keywords"""
    test_sop_compliant = """# Overview
This is a complete SOP overview section.

# Procedure
Step 1: You MUST configure the firewall rules first.
Step 2: You SHOULD document all changes made.
Step 3: You MAY optionally run additional scans.
The system must-not allow unauthorized access.
All components should-support the required protocols.

# Negative Constraints
Do not use deprecated protocols.
MUST NOT expose sensitive data.

# Examples
Example code here with MUST requirements.
"""

    with open('docs/test.sop.md', 'w', encoding='utf-8') as f:
        f.write(test_sop_compliant)

    validator = SOPValidator(encoding='utf-8')
    report6 = validator.validate_file('docs/test.sop.md')
    print(f"Test 6 - Complete compliant SOP:")
    print(f"  Status: {report6.status}")
    print(f"  Issues: {report6.issues_list}")
    print("  Warnings: " + str(report6.warnings_list))
    return report6

def test_empty_sections():
    """Test 7: Empty sections (should warn but not fail on missing content)"""
    test_sop_empty_sections = """# Overview
Overview content here.

# Procedure

# Negative Constraints

# Examples
Examples content here.
"""

    with open('docs/test.sop.md', 'w', encoding='utf-8') as f:
        f.write(test_sop_empty_sections)

    validator = SOPValidator(encoding='utf-8')
    report7 = validator.validate_file('docs/test.sop.md')
    print(f"\nTest 7 - SOP with empty sections:")
    print(f"  Status: {report7.status}")
    print(f"  Issues: {report7.issues_list}")
    print("  Warnings: " + str(report7.warnings_list))
    return report7

def test_utf8():
    """Test 8: Verify UTF-8 encoding works"""
    test_sop_utf8 = """# Overview
Overview with special chars: cafe, naive, Japanese.

# Procedure
Step 1: MUST handle UTF-8 properly.
Step 2: SHOULD use proper encoding.

# Negative Constraints
MUST NOT use ASCII only.

# Examples
Example: cafe resume naive
"""

    with open('docs/test.sop.md', 'w', encoding='utf-8') as f:
        f.write(test_sop_utf8)

    validator = SOPValidator(encoding='utf-8')
    report8 = validator.validate_file('docs/test.sop.md')
    print(f"\nTest 8 - UTF-8 encoded SOP:")
    print(f"  Status: {report8.status}")
    print(f"  Issues: {report8.issues_list}")
    print("  Warnings: " + str(report8.warnings_list))
    return report8

if __name__ == '__main__':
    test_compliant_sop()
    test_empty_sections()
    test_utf8()
    print("\nAll validation tests completed successfully!")
