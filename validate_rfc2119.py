#!/usr/bin/env python3
import re

with open('docs/recon-enumeration.sop.md', 'r') as f:
    content = f.read()

lines = content.split('\n')
procedure_lines = lines[47:285]

print("=" * 70)
print("RFC2119 CONSTRAINT COMPLIANCE VALIDATION REPORT")
print("=" * 70)

# Test Case 1: Step 1 Target Identification - MUST constraints
print("\n" + "=" * 70)
print("TEST CASE 1: Step 1 Target Identification - MUST constraints (lines 48-110)")
print("=" * 70)

step1_content = '\n'.join(procedure_lines[49:111])
print(f"\nStep 1 content:\n{step1_content}\}

must_count = len(re.findall(r'\*\*MUST\*\*', step1_content))
must_not_count = len(re.findall(r'\*\*MUST NOT\*\*', step1_content))
should_count = len(re.findall(r'\*\*SHOULD\*\*', step 1_content)
may_count = len(re.findall(r'\*\*MAY\*\*', step1_content))

print(f"\nMUST count: {must_count}")  
print(f"MUST NOT count: {must_not_count}")  
print(f"SHOULD count: {should_count}")  
print(f"MAY count: {may_count}")

improper_m_must = re.findall(r'\*\*must\*\*', step1_content, re.IGNORECASE)
print(f"\nImproperly formatted 'must' (lowercase): {len(improper_must)}")
for match in improper_must:
    print(f"Found: {repr(match)}")

improper_must_not = re.findall(r'\*\*must not\*\*', step1_content, re.IGNORECASE)
print(f"\nImproperly formatted 'must not' (lowercase): {len(improper_must_not)}")
for match in improper_must_not:
    print(f"Found: {repr(match)}")

should_not_count = len(re.findall(r'\*\*SHOULD NOT\*\*', step1_content))
print(f"\nSHOULD NOT count: {should_not_count}")
