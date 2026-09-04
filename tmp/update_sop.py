with open('docs/asset-inventory.sop.md', 'r') as f:
    content = f.read()

# Read all lines
lines = content.split('\n')

# Remove trailing empty lines to find the actual last line
while lines and lines[-1].strip() == '':
    lines.pop()

print(f"Lines after removing trailing empty: {len(lines)}")
print("Last 5 lines:")
for i, line in enumerate(lines[-5:], start=len(lines)-5):
    print(f"Line {i}: {repr(line)}")

# YAML block to insert
yaml_block = """---
priority: MEDIUM
version: 1.0
last_updated: 2024-01-15
status: FINAL
---"""

# Find the last non-empty line index
last_non_empty_idx = -1
for i in range(len(lines)-1, -1, -1):
    if lines[i].strip():
        last_non_empty_idx = i
        break

print(f"Last non-empty line index: {last_non_empty_idx}")
print(f"Content of that line: {repr(lines[last_non_empty_idx])}")

# Insert YAML block before the last non-empty line
if last_non_empty_idx >= 0:
    new_lines = lines[:last_non_empty_idx] + [yaml_block] + lines[last_non_empty_idx:]
else:
    new_lines = [yaml_block] + lines

new_content = '\n'.join(new_lines)

with open('docs/asset-inventory.sop.md', 'w') as f:
    f.write(new_content)

print("File updated successfully")
