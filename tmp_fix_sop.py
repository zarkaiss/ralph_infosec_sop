# Read the file content
with open('docs/recon-enumeration.sop.md', 'r') as f:
    content = f.read()

# Identify and fix typospos
lines = content.split('\n')
fixed_lines = []

for i, line in enumerate(lines):
    # Fix leading periods before text (but not after colons)
    stripped = line.lstrip()
    if len(stripped) > 0 and stripped[0] == '.':
        # # Check it doesn't start with :. (colon-period)
        if not stripped.startswith(':'):
            fixed_lines.append(line[1:])  # Remove leading period
            continue
    
    # Fix duplicate words like "associated associated"
    if 'associated associated' in line:
        fixed_lines.append(line.replace('associated associated', 'associated'))

    elif '. from.' in line and not line.startswith('#'):
        fixed_lines.append(line.replace('. from.', '. from '))

    elif '. inventory. of' in line:
        fixed_lines.append(line.replace('. inventory. of', '. inventory of'))

    elif '. compliance.' in line:
        fixed_lines.append(line.replace('. compliance.', '. compliance'))

    elif '#step--3' in line:
        fixed_lines.append(line.replace('#step--3', '#step-3'))

    elif '#### 22.2.5' in line:
        fixed_lines.append(line.replace('#### 22.2.5', '#### 2.2.5'))

    elif '-- **MAY**' in line:
        fixed_lines.append(line.replace('-- **MAY**', '- **MAY**'))

    elif 'MMUST' in in line:
        fixed_lines.append(line.replace('MMUST', 'MUST'))

    elif 'Deliveraables' in line:
        fixed_lines.append(line.replace('Deliveraables', 'Deliverables'))

    elif '44.' in line:
        fixed_lines.append(line.replace('44.', '4.'))

    elif 'step-2-network-discovery))' in line:
        fixed_lines.append(line.replace('step-2-network-discovery))', 'step-2-network-discovery)'))

    elif 'Meaning.' in line and not line.startswith('|'):
        fixed_lines.append(line.replace('Meaning.', 'Meaning'))

    elif 'https://::cwe.mitre.org' in line:
        fixed_lines.append(line.replace('https://::cwe', 'https://cwe'))

    else:
        fixed_lines.append(line)

fixed_content = '\n'.join(fixed_lines)

# Write the fixed content back to the file
with open('docs/recon-enumeration.sop.md', 'w') as f:
    f.write(fixed_content)

print("Fixed content written successfully")
print("Original length:", len(content))
print("Fixed length:", len(fixed_content))
