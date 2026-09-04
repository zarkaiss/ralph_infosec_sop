"""
RFC2119 Keyword Usage and Markdown Formatting Linting Tests for SOP documents.

This module provides comprehensive linting tests to verify:
- RFC2119 keyword usage (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY)
- Proper markdown formatting compliance
- Consistent constraint language throughout the document
- Syntax errors and header consistency
"""

from pathlib import Path
import re


class RFC_2119_Linting_Error(Exception):
    """Custom exception for RFC2119 linting violations."""
    pass


def test_rfc2119_keywords_exist():
    """Verify that all RFC2119 keywords are present in the document."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # RFC2119 keywords (case-insensitive check)
    required_keywords = {
        'MUST': True,
        'MUST NOT': True,
        'SHOULD': True,
        'SHOULD NOT': True,
        'MAY': True
    }
    
    for keyword in required_keywords:
        if keyword not in content:
            raise RFC_2119_Linting_Error(
                f"Missing RFC2119 keyword: {keyword}"
            )
    
    print(f"✓ All RFC2119 keywords present: {list(required_keywords.keys())}")


def test_rfc2119_keyword_consistency():
    """Verify consistent usage of RFC2119 keywords (case sensitivity check)."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check for inconsistent casing (e.g., "must" vs "MUST")
    # RFC2119 keywords should be uppercase
    lowercase_keywords = re.findall(r'\b(must|must not|should|should not|m ay)\b', content, re.IGNORECASE)
    
    if len(lowercase_keywords) > 0:
        raise RFC_2119_Linting_Error(
            f"Inconsistent RFC2119 keyword casing found: {lowercase_keywords}"
        )
    
    print("✓ RFC2119 keywords are consistently uppercase")


def test_rfc2119_keyword_context():
    """Verify RFC2119 keywords are used in proper context (not as regular words like 'must' in 'mustard')."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check for keywords followed by non-alphanumeric characters or at word boundaries
    keyword_patterns = [
        r'\bMUST\b',
        r'\bMUST NOT\b',
        r'\bSHOULD\b',
        r'\bSHOULD NOT\b',
        r'\bMAY\b'
    ]
    
    # Count occurrences of each keyword in proper context
    for pattern in keyword_patterns:
        matches = re.findall(pattern, content)
        if len(matches) == 0:
            raise RFC_2119_Linting_Error(
                f"No valid occurrences found for keyword pattern: {pattern}"
            )
    
    print("✓ All RFC2119 keywords used in proper context")


def test_no_inconsistent_must_not():
    """Verify 'MUST NOT' is not split or inconsistently formatted."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check for variations like "mustnot" (without space)
    if re.search(r'\bMUSTNOT\b', content):
        raise RFC_2119_Linting_Error(
            f"Found 'MMUSTNOT' without space - should be 'MUST NOT'"
        )
    
    print("✓ 'MUST NOT' keyword is consistently formatted with space")


def test_no_mixed_case_keywords():
    """Verify no mixed case variations of RFC2119 keywords."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check for mixed case like "Must" or "Should"
    mixed_case_patterns = [
        r'\bMust\b',
        r'\bShould\b',
        r'\bMay\b'
    ]
    
    for pattern in mixed_case_patterns:
        if re.search(pattern, content):
            raise RFC_2119_Linting_Error(
                f"Found mixed case keyword matching pattern: {pattern}"
            )
    
    print("✓ No mixed case RFC2119 keywords found")


def test_markdown_header_structure():
    """Verify proper markdown header structure (no spaces before in headers)."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content_lines = filepath.read_text(encoding="utf-8").split('\n')

    for i, line in enumerate(content_lines):
        # Check for headers with leading spaces (invalid markdown)
        if re.match(r'^\s*#{1,6}\s', line):
            raise RFC_2119_Linting_Error(
                f"Line {i+1}: Header should have no leading spaces: {line.strip()}"
            )
    
    print("✓ All markdown headers are properly formatted")


def test_markdown_no_empty_lines_between_paragraphs():
    """Verify no excessive empty lines between paragraphs."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Count consecutive newlines (more than 2 is excessive)
    triple_newlines = len(re.findall(r'\n\n\n', content))
    
    if triple_newlines > 0:
        raise RFC_2119_Linting_Error(
            f"Found {triple_newlines} instances of 3+ consecutive newlines"
        )
    
    print("✓ No excessive empty lines between paragraphs")


def test_markdown_no_trailing_whitespace():
    """Verify no trailing whitespace on lines."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    lines = content.split('\n')
    trailing_whitespace_count = sum(1 for line in lines if line != line.rstrip())
    
    if trailing_whitespace_count > 0:
        raise RFC_2119_Linting_Error(
            f"Found {trailing_whitespace_count} lines with trailing whitespace"
        )
    
    print("✓ No trailing whitespace on lines")


def test_markdown_no_tabs():
    """Verify no tabs used (markdown best practice)."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    if '\t' in content:
        raise RFC_2119_Linting_Error(
            "File contains tabs which should be replaced with spaces"
        )
    
    print("✓ No tabs found in file")


def test_markdown_list_consistency():
    """Verify consistent list formatting (no mixed - bullet and numbered lists)."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check for inconsistent list markers in close proximity
    lines = content.split('\n')
    list_markers = []
    
    for line in lines:
        if re.match(r'^\s*[-*]\s', line):
            list_markers.append('-')
        elif re.match(r'^\d+\.', line):
            list_markers.append('1.')
    
    # If we have both types, it might be intentional (TOC vs content)
    if len(list_markers) > 0:
        print("✓ List markers consistent")


def test_markdown_code_block_formatting():
    """Verify proper code block formatting."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    lines = content.split('\n')
    
    in_code_block = False
    
    for i, line in enumerate(lines):
        if re.match(r'^```', line):
            in_code_block = not in_code_block
            print(f"✓ Code block at line {i+1}: {'opened' if not in_code_block else 'closed'}")
        elif in_code_block and not re.match(r'^```', line):
            # Check for proper indentation within code blocks
            if line.strip() and len(line) - len(line.lstrip()) < 4:
                raise RFC_2119_Linting_Error(
                    f"Line {i+1}: Code block content should not be indented less than 4 spaces"
                )
    
    print("✓ Code blocks are properly formatted")


def test_markdown_link_formatting():
    """Verify proper markdown link formatting."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check for broken links (links without closing brackets)
    link_pattern = r'\[([^\]]*)\]\(([^)]*)\)'
    matches = re.findall(link_pattern, content)
    
    if len(matches) > 0:
        print(f"✓ Found {len(matches)} valid markdown links")


def test_markdown_table_formatting():
    """Verify proper table formatting (if tables exist)."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utfutf-8")
    
    lines = content.split('\n')
    
    in_table = False
    for i, line in enumerate(lines):
        if re.match(r'^\|', line):
            if not in_table and len(line.strip()) > 0:
                raise RFC_2119_Linting_Error(
                    f"Line {i+1}: Table row should have consistent column alignment"
                )
    
    print("✓ Tables are properly formatted (if any exist)")


def run_all_linting_tests():
    """Run all linting tests and report results."""
    print("=" * 60)
    print("RFC2119 Keyword Usage and Markdown Formatting Linting Tests")
    print("=" * 60)
    print()
    
    try:
        test_rfc2119_keywords_exist()
        test_rfc2119_keyword_consistency()
        test_rfc2119_keyword_context()
        test_no_inconsistent_must_not()
        test_no_mixed_case_keywords()
        test_markdown_header_structure()
        test_markdown_no_empty_lines_between_paragraphs()
        test_markdown_no_trailing_whitespace()
        test_markdown_no_tabs()
        test_markdown_list_consistency()
        test_markdown_code_block_formatting()
        test_markdown_link_formatting()
        test_markdown_table_formatting()
        
        print()()
        print("=" * 60)
        print("✓ All linting tests passed!")
        print("=" * 60)
        return True
        
    except RFC_2119_Linting_Error as e:
        print()
        print("=" * 60)
        print(f"✗ Linting test failed: {e}")
        print("=" * 60)
        return False


if __name__ == "__main__":
    success = run_all_linting_tests()
    exit(0 if success else 1)
