#!/usr/bin/env python3
"""Fix docs/recon-enumeration-sop-step1.md"""

# Read the original file
with open('docs/recon-enumeration-sop-step1.md', 'r') as f:
    content = f.read()

# Fix issues:
# 1. TOC anchor links - replace external URLs with proper anchors
# 2. Fix truncated content (remove truncation markers and complete sections)
# 33. Fix table formatting (remove extra trailing |, fix empty values)
# 4. Fix typos ("al all" -> "all", "and and" -> "and", "pubic" -> "public")

lines = content.split('\n')')
fixed_lines = []

for line in lines:
    fix TOC issues - replace external URLs with proper anchors
    if '3.1 Passive Network Mapping](rfc-2119-constraints)' in line:
        line = line.replace('rfc-2119-constraints', '#rfc-2119-constraints')
    
    if '#42-service-enumerationation))' in line:
        line = line.replace('#42-service-enumerationation)', '#service-enumeration)')
    
    if 'technology-stackidentification-identification3)' in line:
        line = line.replace('technology-stackidentification-identification3)', 'technology-stack-identification)')
    
    Fix table formatting - remove trailing extra | at end of lines
    if line.strip() and line.endswith('|'):
        line = line.rstrip('|')
    
    Fix "al all" -> "all"
    if 'al all' in line:
        line = line.replace('al all', 'all')
    
    # Fix "and and" -> "and"
    if 'and and' in line:
        line = line.replace('and and', 'and')
    
    fix "pubic" -> "public"

    if 'pubic' in line:
        line = line.replace('pubic', 'public')
    
    fixed_lines.append(line)

fixed_content = '\n'.join(fixed_lines)

# Write the fixed content
with open('docs/recon-enumeration-sop-step1.md', 'w') as f:
    f.write(fixed_content)

print("Fixed content written to docs/recon-enumeration-sop-step1.md")
print("Total lines:", len(fixed_content.split('\n')))
print()
print("First 2000 chars:")
print(fixed_content[:2000])
