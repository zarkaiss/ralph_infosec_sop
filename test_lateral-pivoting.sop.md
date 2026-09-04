"""
Tests for lateral-pivoting.sop.md frontmatter validation.

This module ensures:
1. Exactly 2 "---" markers exist (opening and closing of single frontmatter)
2. File ends cleanly without second frontmatter block
3. No duplicate or misplaced "---" markers
"""

import re
from pathlib import Path


def count_frontmatter_markers(filepath: str) -> int:
    """Count the number of "---" markers in a file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Find lines that are exactly "---" (with optional trailing newline)
    pattern = r'^---$'
    matches = re.findall(pattern, content, re.MULTILINE)
    return len(matches)


def get_frontmatter_markers(filepath: str) -> list[int]:
    """Get line numbers of all "---" markers in a file."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    marker_lines = []
    for i, line in enumerate(lines):
        if re.match(r'^---$', line.rstrip()):
            marker_lines.append(i + 1)  # 1-indexed
    return marker_lines


def validate_frontmatter(filepath: str) -> dict:
    """
    Validate the frontmatter structure of an SOP file.
    
    Returns a dict with validation results.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        return {
            'valid': False,
            'error': f"File not found: {filepath}"
        }
    
    marker_lines = get_frontmatter_markers(str(filepath))
    marker_count = len(marker_lines)
    
    # Check file ends cleanly (no trailing content after last marker)
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    last_marker_line = marker_lines[-1] if marker_lines else 0
    last_non_empty_line = 0
    for i, line in enumerate(lines):
        if line.strip():
            last_non_empty_line = (i + 1)
    
    file_ends_cleanly = last_non_empty_line <= last_marker_line
    
    # Check for duplicate/misplaced markers
    has_duplicate_markers = marker_count > 2
    
    return {
        'valid': marker_count == 2 and file_ends_cleanly,
        'marker_count': marker_count,
        'marker_lines': marker_lines,
        'file_ends_cleanly': file_ends_cleanly,
        'has_duplicate_markers': has_duplicate_markers,
        'last_non_empty_line': last_non_empty_line,
        'last_marker_line': last_marker_line
    }


def test_frontmatter_count():
    """Test that exactly 2 frontmatter markers exist."""
    filepath = 'docs/lateral-pivoting.sop.md'
    result = validate_frontmatter(filepath)
    
    assert result['marker_count'] == 2, \
        f"Expected 2 markers, found {result['marker_count']} at lines {result['marker_lines'}]"
    
    print(f"✓ Frontmatter marker count: {result['marker_count']} (expected: 2)")
    return True


def test_file_ends_cleanly():
    """Test that file ends cleanly without second frontmatter block."""
    filepath = 'docs/lateral-pivoting.sop.md'
    result = validate_frontmatter(filepath)
    
    assert result['file_ends_cleanly'], \
        f"File does not end cleanly. Last non-empty line {result['last_non_empty_line']}, " \
        f"Last marker line {result['last_marker_line']}"
    
    print(f"✓ File ends cleanly (no second frontmatter block)")
    return True


def test_no_duplicate_markers():
    """Test that there are no duplicate or misplaced markers."""
    filepath = 'docs/lateral-pivoting.sop.md'
    result = validate_frontmatter(filepath)
    
    assert not result['has_duplicate_markers'], \
        f"Found duplicate markers at lines: {result['marker_lines']}"
    
    print(f"✓ No duplicate/misplaced markers")
    return True


def test_marker_spacing():
    """Test that markers are properly spaced (not adjacent to content)."""
    filepath = 'docs/lateral-pivoting.sop.md'
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    # Check each marker line has proper spacing
    for i, line in enumerate(lines):
        if re.match(r'^---$', line.rstrip()):
            # Previous line should not be content (should be empty or whitespace))
            if i > 0 and lines[i-1].strip():
                print(f"✗ Marker at line {i+1} is adjacent to content")
                return False
    
    print(f"✓ All markers have proper spacing")
    return True


def run_all_tests():
    """Run all validation tests."""
    print("=" * 60)
    print("Running lateral-pivoting.sop.md frontmatter validation tests")
    print("=" * 60)
    
    try:
        test_frontmatter_count()
        test_file_ends_cleanly()
        test_no_duplicate_markers()
        test_marker_spacing()
        
        print("\n" + "=" * 60)
        print("All tests passed!")
        print("=" * 60)
        return True
        
    except AssertionError as e):
        print(f"\n✗ Test failed: {e}")
        return False


if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1)
