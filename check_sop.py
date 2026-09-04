#!/usr/bin/env python3
"""Check SOP files for issues."""

import os

# Check vulnerability-exploitation.sop.md for MUSTUST
print("=== Checking vulnerability-exploitation.sop.md ===")
with open('docs/vulnerability-exploitation.sop.md', 'r') as f:
    content = f.read()
    lines = content.split('\n')
    for i, line in enumerate(lines[:20], 1):
        print(f"{i}: {line}")

# Check vulnerability-scanning.sop.md around line 244
print("\n=== Checking vulnerability-scanning.sop.md around line 244 ===")
with open('docs/vulnerability-scanning.sop.md', 'r') as f:
    content = f.read()
    lines = content.split('\n')
    for i in range(240, min(250, len(lines))):
        print(f"{i+1}: {lines[i]}")

# Check recon-enumeration.sop.md for NegativeParameter Constraints
print("\n=== Checking recon-enumeration.sop.md for NegativeParameter ===")
with open('docs/recon-enumeration.sop.md', 'r') as f:
    content = f.read()
    if 'NegativeParameter' in content:
        idx = content.find('NegativeParameter')
        lines = content[:idx].split('\n')
        print(f"Found NegativeParameter at line {len(lines)}")
        print(f"Context: {content[max(0,idx-200):idx+200]}")
    else:
        print("No NegativeParameter found")

# Search for all files with issues
print("\n=== Searching for MUSTUST in all sop.md files ===")
for root, dirs, files in os.walk('.'):
    for f in files:
        if 'sop' in f.lower() and f.endswith('.md'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
                if 'MMUSTUST' in content:
                    idx = content.find('MUSTUST')
                    lines = content[:idx].split('\n')
                    print(f"Found MUSTUST in {path}, line {len(lines)}")

print("\n=== Searching for extra ) patterns ===")
for root, dirs, files in os.walk('.'):
    for f in files:
        if 'sop' in f.lower() and f.endswith('.md'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
                lines = content.split('\n')
                for idx, line in enumerate(lines, 1):
                    if line.count(')') > line.count('('):
                        print(f"{path}:{idx}: {line}")

print("\n=== Searching for NegativeParameter ===")
for root, dirs, files in os.walk('.'):
    for f in files:
        if 'sop' in f.lower() and f.endswith('.md'):
            path = os.path.join(root, f)
            with open(path, 'r') as file:
                content = file.read()
                if 'NegativeParameter' in content:
                    idx = content.find('NegativeParameter')
                    lines = content[:idx].split('\n')
                    print(f"Found NegativeParameter in {path}, line {len(lines)}")
