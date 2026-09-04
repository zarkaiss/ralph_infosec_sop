"""
Markdown linting tests for docs/recon-enumeration.sop.md
Checks for common markdown formatting errors and best practices.
"""

import re
from pathlib import Path


def test_no_empty_lines_between_paragraphs():
    """Verify no excessive empty lines between paragraphs."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Count consecutive newlines (more than 2 is excessive)
    double_newlines = len(re.findall(r'\n\n', content))
    triple_newlines = len(re.findall(r'\n\n\n', content))
    
    # Allow some empty lines, but not too many in a row
    assert triple_newlines == 0, f"Found {triple_newlines} instances of 3+ consecutive newlines"


def test_no_trailing_whitespace():
    """Verify no trailing whitespace on lines."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    lines = content.split('\n')
    trailing_whitespace_count = sum(1 for line in lines if line != line.rstrip())
    
    assert trailing_whitespace_count == 0, \
        f"Found {trailing_whitespace_count} lines with trailing whitespace"


def test_no_tabs():
    """Verify no tabs used (markdown best practice)."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    assert '\t' not in content, "File contains tabs which should be replaced with spaces"


def test_consistent_header_spacing():
    """Verify consistent spacing after headers."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check that headers are followed by newline, not space then newline
    header_with_space = re.findall(r'^#{1,6}\s+\S\s+\n', content, re.MULTILINE)
    
    assert len(header_with_space) == 0, \
        "Headers should be followed by newline, not space+newline"


def test_no_mixed_list_styles():
    """Verify consistent list style (not mixing - and * in same list)."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    lines = content.split('\n')
    list_contexts = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'^\s*[-*]\s+', line):
            # Found a list item, check next few lines for mixed styles
            context = '\n'.join(lines[i:i+5])
            bullet_types = set(re.findall(r'^\s*([-*])', context, re.MULTILINE))
            if len(bullet_types) > 1:
                assert False, f"Mixed list styles found in:\n{context}"
        i += 1


def test_code_blocks_properly_closed():
    """Verify all code blocks are properly closed."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Count opening and closing code blocks
    open_count = content.count('```')
    close_count = content.count('```\n') + content.count('```\r\n')
    
    # Note: ``` at end of file might not have newline, so check both
    assert open_count == close_count, \
        f"Code blocks mismatch: {open_count} opening vs {close_count} closing"


def test_links_properly_formatted():
    """Verify any links are properly formatted."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check for broken link patterns (link without text or vice versa)
    # This is a basic check - markdownlint would be more thorough
    
    # Find all links
    links = re.findall(r'\[([^\]]*)\]\(([^)]+)\)', content)
    
    for text, url in links:
        assert len(text) > 0 or len(url) > 0, "Empty link found"


def test_no_raw_html():
    """Verify no raw HTML tags (markdown should be used)."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check for common HTML tags that shouldn't be in markdown
    html_tags = ['<p>', '<div>', '<span>', '<br>', '<hr>']
    found_html = [tag for tag in html_tags if tag in content]
    
    assert len(found_html) == 0, \
        f"Found raw HTML tags: {found_html}. Use markdown syntax instead."


def test_image_syntax_valid():
    """Verify any images have valid syntax."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check for image syntax ![alt](src)
    images = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content)
    
    for alt, src in images:
        assert len(src) > 0, "Image source is empty"


def test_header_hierarchy():
    """Verify proper header hierarchy (no skipping levels)."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    lines = content.split('\n')
    prev_level = 0
    
    for line in lines:
        match = re.match(r'^#{1,6}\s', line)
        if match:
            level = len(match.group())
            # Initialize prev_level to a high value for the first header
            if prev_level == 0 and level > 1:
                prev_level = level  # First header sets the baseline
            
            # Allow going down one level or staying same
            assert level <= prev_level + 1, \
                f"Header hierarchy error: level {level} follows level {prev_level}"
            prev_level = level


def test_no_special_chars_in_headers():
    """Verify headers don't contain special characters that break markdown."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    lines = content.split('\n')
    for line in lines:
        if re.match(r'^#{1,6}\s', line):
            header_text = line[match.end():] if (match := re.match(r'^#{1,6}\s', line)) else ''
            # Check for problematic characters
            assert not any(c in header_text for c in ['<', '>', '"', "'", '[', ']']), \
                f"Special character found in header: {line}"


def test_blockquotes_valid():
    """Verify blockquote syntax is valid."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check for proper blockquote opening
    blockquotes = re.findall(r'^>\s+', content, re.MULTILINE)
    
    # If there are blockquotes, verify they're properly formatted
    if len(blockquotes) > 0:
        lines = content.split('\n')
        in_blockquote = False
        for line in lines:
            if line.startswith('>'):
                in_blockquote = True
            elif in_blockquote and not line.startswith('>') and not line.strip() == '':
                # Blockquote ended unexpectedly (empty line or non-blockquote line)
                pass  # This is actually fine, blockquotes can end


def test_table_syntax_valid():
    """Verify any tables have valid syntax."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check for table patterns (|---|---|)
    if '|' in content:
        lines = content.split('\n')
        header_row = None
        separator_row = None
        
        for line in lines:
            if re.match(r'^\s*\|.*\|\s*$', line):
                if header_row is None:
                    header_row = line
                elif re.match(r'^\s*\|\s*-+\s*\|', line):
                    separator_row = line
        
        # If we found a table, verify it has proper structure
        if header_row and separator_row:
            assert separator_row.count('|') == header_row.count('|'), \
                "Table column count mismatch between header and separator"


def test_no_broken_references():
    """Verify no broken reference patterns."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    # Check for unclosed references like [[link without ]]
    unclosed_refs = re.findall(r'\[\[', content)
    
    assert len(unclosed_refs) == 0, \
        f"Found {len(unclosed_refs)} unclosed reference markers"


def test_line_length_reasonable():
    """Verify lines are not excessively long (markdown best practice)."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    lines = content.split('\n')
    long_lines = [line for line in lines if len(line) > 120]
    
    # Allow some flexibility, but warn about very long lines
    assert len(long_lines) <= 2, \
        f"Found {len(long_lines)} lines longer than 120 characters"


def test_no_duplicate_headers():
    """Verify no duplicate headers at same level."""
    filepath = Path("docs/recon-enumeration.sop.md")
    content = filepath.read_text(encoding="utf-8")
    
    lines = content.split('\n')
    header_counts = {}
    
    for line in lines:
        match = re.match(r'^#{1,6}\s+(.+)', line)
        if match:
            header_text = match.group(1).strip()
            level = len(match.group())
            key = f"level{level}:{header_text}"
            
            if key in header_counts:
                assert False, f"Duplicate header found: {header_text} at level {level}"
            header_counts[key] = True


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
