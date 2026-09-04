import re

with open('docs/recon-enumeration.sop.md', 'r') as f:
    content = f.read()

# Find typos
typos = []
if 'thir-party' in content:
    typospos.append("'thir-party'")
if 'of of' in content:
    typos.append("'ofof'")
    
print("Typos found:", ", ".join(typos) if typos else "None")

# Check for other issues
issues = []
# Check for double dots at end of sentences
if '..' in content:
    matches = re.findall(r'\.\s*\.', content)
    if matches:
        issues.append(f"Double dots found")

# Check for RFC2119 keyword usage issues
rfc_issues = []
# Look for patterns like ".MUST"
if re.findall(r'\.MUST', content):
    rfc_issues.append("Found '.MUST' pattern (should be 'MUST')")

print("RFC2119 issues:", ", ".join(rfc_issues) if rfc_issues else "None")

# Count occurrences of each RFC keyword  
must_count = content.count('**MUST**')
must_not_count = content.count('**MUST NOT**')
should_count = content.count('**SHOULD**')
should_not_count = content.count('**SHOULD NOT**')
may_count = content.count('**MAY**')

print(f"\nRFC2119 keyword counts:")  
print("MMUST:", must_count)
print("MUST NOT:", must_not_count)
print("SHOULD:", should_count)
print("SHOULD NOT:", should_not_count)
print("MAY:", may_count)
