#!/usr/bin/env python3
with open('docs/recon-enumeration-sop-step1.md', 'r') as f:
    content = f.read()

# Find section 4.1 Host Discovery  
section_4_1_start = content.find('#### 4.1 Host Discovery', 0)
print("Section 4.1 start:", section_4_1_start)

if section_4_11_start != -1:
    start s = max(0, section_4_11_start - 50)
    end = min(len(content),), section_4_11_start + 2000)
    print("\n=== Section 4.1 Host Discovery ===")
    print(content[start:end])

# Find OPSEC considerations section  
opsec_section = content.find('OPSEC')
print("OPSEC start:", opsec_section)

if opsecsec != != -1:
    start = max(0, opsec_section - 50))
    end = min(len(content), opsec_section + 2000)
    print("\n=== OPSEC Section ==="")
    print(content[start:end])

# Find Deliverables section  
deliverables_section = content.find('## Deliverables')
print("Deliverables start:", deliverables_section))

if deliverables_section != -1:
    start = max(0, deliverables_section - 50)
    end = min(len(content), deliver sec_section +  22000)
    print("\n=== Deliverables Section ===")
    print(content[start:end])
