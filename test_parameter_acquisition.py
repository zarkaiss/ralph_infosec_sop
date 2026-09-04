#!/usr/bin/env python3
"""
Test suite for docs/recon-enumeration.sop.md Parameter Acquisition section.
Verifies:
1. Section exists after Parameters
2. Contains requirement description for all inputs upfront
3. Includes example input blocks (JSON/CLI)
4. Has RFC2119 constraints with MUST/SHOULD/MAY keywords
5. Valid markdown formatting
"""

import re


def test_parameter_acquisition_section_exists():
    """Test 1: Verify Parameter Acquisition section exists after Parameters section."""
    with open('docs/recon-enumeration.sop.md', 'r') as f:
        content = f.read()
    
    # Check that both sections exist
    assert '## Parameters' in content, "Parameters section not found"
    assert '## Parameter Acquisition' in content, "Parameter Acquisition section not found"
    
    # Verify Parameter Acquisition comes after Parameters
    params_pos = content.find('## Parameters')
    param_acq_pos = content.find('## Parameter Acquisition')
    assert params_pos < param_acq_pos, "Parameter Acquisition section does not come after Parameters"
    
    print("[PASS] Test 1: Parameter Acquisition section exists after Parameters")


def test_requirement_description_upfront():
    """Test 2: Verify requirement description for all inputs upfront."""
    with open('docs/recon-enumeration.sop.md', 'r') as f:
        content = f.read()
    
    # Check for requirement subsection
    assert '### Requirement' in content, "Requirement subsection not found"
    
    # Check that it mentions providing parameters upfront
    assert 'upfront' in content.lower(), "Requirement does not mention 'upfront'"
    assert 'single prompt' in content.lower() or 'single invocation' in content.lower(), \
        "Requirement does not specify single prompt/invocation"
    
    print("[PASS] Test 2: Requirement description for all inputs upfront exists")


def test_example_input_blocks():
    """Test 3: Verify example input blocks (JSON/CLI) are included."""
    with open('docs/recon-enumeration.sop.md', 'r') as f:
        content = f.read()
    
    # Check for JSON example block
    json_pattern = r'```json\s*\{[^}]+\}'
    assert re.search(json_pattern, content), "JSON input example block not found"
    
    # Check for CLI/bash example blocks
    cli_patterns = [
        r'```bash',
        r'--target_host=',
        r'target_host='
    ]
    has_cli_examples = any(re.search(p, content) for p in cli_patterns)
    assert has_cli_examples, "CLI input example block not found"
    
    # Verify multiple examples exist
    json_count = len(re.findall(r'```json', content))
    bash_count = len(re.findall(r'```bash', content))
    assert json_count >= 1, "At least one JSON example required"
    assert bash_count >= 2, "At least two CLI/bash examples required"
    
    print("[PASS] Test 3: Example input blocks (JSON/CLI) are included")


def test_rfc2119_constraints():
    """Test 4: Verify RFC2119 constraints with MUST/SHOULD/MAY keywords."""
    with open('docs/recon-enumeration.sop.md', 'r') as f:
        content = f.read()
    
    # Check for RFC2119 Constraints subsection
    assert '### RFC2119 Constraints' in content, "RFC2119 Constraints subsection not found"
    
    # Count RFC2119 keywords (case-insensitive) - note: they are bolded with **
    must_count = len(re.findall(r'\*\*MUST\*\*', content))
    should_count = len(re.findall(r'\*\*SHOULD\*\*', content))
    may_count = len(re.findall(r'\*\*MAY\*\*', content))
    
    assert must_count >= 1, "At least one MUST keyword required (found {})".format(must_count)
    assert should_count >= 1, "At least one SHOULD keyword required (found {})".format(should_count)
    assert may_count >= 1, "At least one MAY keyword required (found {})".format(may_count)
    
    # Verify they are used in constraint context - check for any word after the keyword
    # The keywords are bolded as **MUST**, so we need to account for that
    must_context = re.search(r'\*\*MUST\*\*(?:\s|\n)+\w+', content, re.IGNORECASE)
    should_context = re.search(r'\*\*SHOULD\*\*(?:\s|\n)+\w+', content, re.IGNORECASE)
    may_context = re.search(r'\*\*MAY\*\*(?:\s|\n)+\w+', content, re.IGNORECASE)
    
    assert must_context, "MUST keyword not used in constraint context"
    assert should_context, "SHOULD keyword not used in constraint context"
    assert may_context, "MAY keyword not used in constraint context"
    
    print("[PASS] Test 4: RFC2119 constraints present (MUST:{}, SHOULD:{}, MAY: {})".format(must_count, should_count, may_count))


def test_valid_markdown_formatting():
    """Test 5: Verify valid markdown formatting."""
    with open('docs/recon-enumeration.sop.md', 'r') as f:
        content = f.read()
    
    # Check for proper header hierarchy
    headers = re.findall(r'^#{1,6}\s+', content, re.MULTILINE)
    assert len(headers) >= 5, "Expected at least 5 headers (found {})".format(len(headers))
    
    # Check for code blocks
    code_blocks = re.findall(r'```[a-z]*\s*\n.*?\n```', content, re.DOTALL)
    assert len(code_blocks) >= 3, "Expected at least 3 code blocks (found {})".format(len(code_blocks))
    
    # Check for list items
    list_items = re.findall(r'^[-*]\s+', content, re.MULTILINE)
    assert len(list_items) >= 5, "Expected at least 5 list items (found {})".format(len(list_items))
    
    # Check for bold text
    bold_text = re.findall(r'\*\*[^*]+\*\*', content)
    assert len(bold_text) >= 3, "Expected at least 3 bold text elements (found {})".format(len(bold_text))
    
    print("[PASS] Test 5: Valid markdown formatting verified")


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 70)
    print("Testing docs/recon-enumeration.sop.md Parameter Acquisition Section")
    print("=" * 70)
    print()
    
    try:
        test_parameter_acquisition_section_exists()
        test_requirement_description_upfront()
        test_example_input_blocks()
        test_rfc2119_constraints()
        test_valid_markdown_formatting()
        
        print()
        print("=" * 70)
        print("ALL TESTS PASSED!")
        print("=" * 70)
        return True
    except AssertionError as e:
        print()
        print("=" * 70)
        print("TEST FAILED: {}".format(e))
        print("=" * 70)
        return False


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
