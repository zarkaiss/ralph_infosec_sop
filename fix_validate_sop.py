#!/usr/bin/env python3
"""Fix the syntax error in validate_sop.py"""

with open('validate_sop.py', 'r') as f:
    content = f.read()

# Fix the double parenthesis issue
new_content = content.replace('Path(filepath).).name', 'Path(filepath).name')

with open('validate_sop.py', 'w') as f:
    f.write(new_content)

print("Fixed!")
