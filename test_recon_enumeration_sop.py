"""
Test suite for docs/recon-enumeration.sop.md
Verifies:
1. Parameters section exists with lowercase_underscore naming convention
2. Table markdown validity
3. Required field logic consistency
"""

import re
from pathlib import Path


EXPECTED_PARAMETERS = [
    "target_host",
    "target_port_range",
    "scan_timeout_seconds",
    "output_format",
    "verbose_level",
    "dns_resolution_enabled"
]

REQUIRED_FIELD = "Yes"
OPTIONAL_FIELD = "No"


def test_parameters_section_exists():
    """Test that Parameters section exists in the SOP document."""
    sop_path = Path("docs/recon-enumeration.sop.md")
    content = sop_path.read_text()
    
    assert "## Parameters" in content, "Parameters section header not found"
    print("✓ Parameters section exists")


def test_lowercase_underscore_naming():
    """Test that all parameters use lowercase_underscore naming convention."""
    sop_path = Path("docs/recon-enumeration.sop.md")
    content = sop_path.read_text()
    
    # Find the table in the Parameters section
    params_section_start = content.find("## Parameters")
    if params_section_start == -1:
        raise AssertionError("Parameters section not found")
    
    # Extract just the table rows (after the separator line)
    # Look for lines containing parameter names (starting with | and a word)
    lines = content[params_section_start:].split("\n")
    
    param_names = []
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines, headers, and separator rows
        if not stripped:
            continue
        
        # Check if this is a table data row (starts with | followed by parameter name)
        if stripped.startswith("|") and "|" in stripped:
            # Extract first column (parameter name)
            cells = [c.strip() for c in stripped.split("|")]
            if len(cells) >= 1 and cells[0]:
                param_name = cells[0]
                # Skip empty parameter names
                if param_name:
                    param_names.append(param_name)
    
    # Check each parameter name follows lowercase_underscore convention
    for param_name in param_names:
        assert param_name == param_name.lower(), f"Parameter '{param_name}' is not lowercase"
        # Allow single word parameters without underscores
        if len(param_name) > 1 and "_" not in param_name:
            raise AssertionError(f"Multi-word parameter '{param_name}' should use underscore naming")
    
    # Verify all expected parameters are present
    for expected_param in EXPECTED_PARAMETERS:
        assert expected_param in param_names, f"Expected parameter '{expected_param}' not found"
    
    print(f"✓ All {len(param_names)} parameters use lowercase_underscore naming")


def test_table_markdown_validity():
    """Test that the markdown table is properly formatted."""
    sop_path = Path("docs/recon-enumeration.sop.md")
    content = sop_path.read_text()
    
    # Find the Parameters section
    params_section_start = content.find("## Parameters")
    assert params_section_start != -1, "Parameters section not found"
    
    # Extract table content (from separator onwards)
    lines = content[params_section_start:].split("\n")
    
    header_found = False
    separator_found = False
    data_rows = []
    
    for line in lines:
        stripped = line.strip()
        
        # Check for header row (contains "Parameter" as first cell)
        if stripped.startswith("| Parameter"):
            header_found = True
        
        # Check for separator row (contains dashes)
        if "---" in stripped or stripped.startswith("|---"):
            separator_found = True
        
        # Collect data rows (table rows that are not headers or separators)
        if stripped.startswith("|") and "|" in stripped:
            cells = [c.strip() for c in stripped.split("|")]
            # Skip header row and separator row
            if not stripped.startswith("| Parameter") and "---" not in stripped:
                data_rows.append(stripped)
    
    assert header_found, "Missing table header row"
    assert separator_found, "Missing table separator row"
    assert len(data_rows) > 0, "No data rows found in table"
    
    print(f"✓ Table markdown is valid with {len(data_rows)} data rows")


def test_required_field_logic():
    """Test that required field logic is consistent."""
    sop_path = Path("docs/recon-enumeration.sop.md")
    content = sop_path.read_text()
    
    # Find the table in the Parameters section
    params_section_start = content.find("## Parameters")
    lines = content[params_section_start:].split("\n")
    
    # Parse data rows
    data_rows = []
    for line in lines:
        stripped = line.strip()
        
        # Skip header, separator, and empty lines
        if not stripped or stripped.startswith("| Parameter") or "---" in stripped:
            continue
        
        # Parse table row
        if stripped.startswith("|") and "|" in stripped:
            cells = [c.strip() for c in stripped.split("|")]
            if len(cells) >= 4:
                param_name = cells[0]
                required_value = cells[3]
                data_rows.append((param_name, required_value))
    
    # Verify only target_host is required
    required_params = [p for p, r in data_rows if r == REQUIRED_FIELD]
    optional_params = [p for p, r in data_rows if r == OPTIONAL_FIELD]
    
    assert len(required_params) == 1, f"Expected exactly 1 required parameter, found {len(required_params)}: {required_params}"
    assert required_params[0] == "target_host", f"Expected 'target_host' to be required, got '{required_params[0]}'"
    
    # Verify all expected parameters are present in the table
    for expected_param in EXPECTED_PARAMETERS:
        assert any(p == expected_param for p, _ in data_rows), f"Parameter '{expected_param}' not found in table"
    
    print(f"✓ Required field logic is consistent: {required_params[0]} is required, {len(optional_params)} optional parameters")


def test_default_values_exist():
    """Test that default values are provided for optional parameters."""
    sop_path = Path("docs/recon-enumeration.sop.md")
    content = sop_path.read_text()
    
    # Check that default values section exists
    assert "Default Value" in content, "Default Value column header not found"
    
    # Verify specific default values mentioned in the doc
    expected_defaults = {
        "target_port_range": "1-1024",
        "scan_timeout_seconds": "300",
        "output_format": "json",
        "verbose_level": "1",
        "dns_resolution_enabled": "true"
    }
    
    for param, expected_default in expected_defaults.items():
        assert f"{param} | {expected_default}" in content or f"| {expected_default} |" in content, \
            f"Default value '{expected_default}' for parameter '{param}' not found"
    
    print(f"✓ Default values are properly documented")


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("Testing docs/recon-enumeration.sop.md")
    print("=" * 60)
    
    try:
        test_parameters_section_exists()
        test_lowercase_underscore_naming()
        test_table_markdown_validity()
        test_required_field_logic()
        test_default_values_exist()
        
        print("=" * 60)
        print("RESULT: PASS")
        print("=" * 60)
        return True
        
    except AssertionError as e:
        print("=" * 60)
        print(f"RESULT: FAIL - {e}")
        print("=" * 60)
        return False


if __name__ == "__main__":
    run_all_tests()
