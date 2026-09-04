with open('docs/vulnerability-exploitation.sop.md', 'r') as f:
    content = f.read()

# Find the last line (non-empty)
lines = content.split('\n')
# Remove trailing empty lines to find actual last content
while lines and lines[-1] == '':
    lines.pop()

print(f"Last non-empty line: {repr(lines[-1])}")

# The YAML block we want to insert
yaml_block = """---
priority: MEDIUM
version: 1.0
last_updated: 2024-01-15
status: FINAL"""

# Insert the YAML block before the last line
new_lines = lines[:-1] + [yaml_block, '']  # Add empty string at end for proper file ending

print(f"New number of lines: {len(new_lines)}")
print("Last 5 new lines:")
for i, line in enumerate(new_lines[-5:], start=len(new_lines)-5):
    print(f"{i}: {repr(line)}")

# Write back with proper newlines
with open('docs/vulnerability-exploitation.sop.md', 'w') as f:
    f.write('\n'.join(new_lines) + '\n')

print("File updated successfully")
