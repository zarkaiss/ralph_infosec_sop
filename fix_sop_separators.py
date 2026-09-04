#!/usr/bin/env python3
"""
Script to fix all .sop.md files in docs/ by removing extra "---" separator lines.
Only keeps the first 2 "---" lines (frontmatter delimiters).
"""

import os
import re

# List of files to fix
FILES_TO_FIX = [
    "asset-inventory.sop.md",
    "incident-response.sop.md",
    "penetration-testing.s.sop.md",
    "recon-enumeration.s.sop.md",
    "recon-enumerationation.sop.md",
    "vulnerability-exploitation.sop.md",
    "vulnerability-exploitationitations.sop.md"
]

def fix_sop_file(filepath):
    """
    Fix a single .sop.md file by removing extra "---" separator lines.
    Only keeps the first 2 "---" lines (frontmatter delimiters).
    
    Returns: (success, message lines)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return False, [f"File not found: {filepath}"]
    
    # Split into lines
    lines = content.splitlines(keepends=True)
    
    # Find all "---" separator lines (exactly "---" on their own line)
    separator_pattern = re.compile(r'^---$')
    
    new_lines = []
    separator_count = 0
    
    for i, line in enumerate(lines):
        if separator_pattern.match(line):
            separator_count += 1
            # Keep only the first 2 separators
            if separator_count <= 2:
                new_lines.append(line)
            else:
                print(f"  Removed extra separator at line {i+1} (kept count: {separator_count})")
        else:
            new_lines.append(line)
    
    # Check if any changes were made
    if new_lines == lines:
        return True, ["No extra separators found - file unchanged"] if content.strip() else ["Empty file"]
    
    # Write back to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    return True, [f"Fixed {filepath}: removed {separator_count - 2} extra separator(s)"]


def main():
    """Main function to process all files."""
    docs_dir = "docs"
    
    print(f"Fixing SOP separator lines in {len(FILES_TO_FIX)} files...")
    print("=" * 60)
    
    success_count = 0
    error_count = 0
    
    for filename in FILES_TO_FIX:
        filepath = os.path.join(docs_dir, filename)
        print(f"\nProcessing: {filename}")
        print("-" * 40)
        
        success, messages = fix_sop_file(filepath)
        
        if success:
            success_count += 1
            for msg in messages:
                print(msg)
        else:
            error_count += 1
            for msg in messages:
                print(msg)
    
    print("\n" + "=" * 60)
    print(f"Summary: {success_count} files fixed successfully, {error_count} errors")
    print("Done!")


if __name__ == "__main__":
    main()
