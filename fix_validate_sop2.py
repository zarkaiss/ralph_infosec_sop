#!/usr/bin/env python3
"""Fix syntax errors in validate_sop.py"""

with open('validate_sop.py', 'r') as f:
    content = f.read()

# Fix the invalid escape sequence - replace '\ ' with proper newline
new_content = content.replace("return '\\ '\\n'.join(lines[start_idx:end_idx])", 
                              "return '\\n'.join(lines[start_idx:end_idx])")

with open('validate_sop.py', 'w') as f:
    f.write(new_content)

print("Fixed!")
