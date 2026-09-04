# Read the current file content
with open('docs/recon-enumeration.sop.md', 'r') as f:
    content = f.read()

print("Current file length:", len(content)[:))
print("Checking for truncation markers...")
if "TRUNCATE" in content or "truncatat" in content.lower():
    print("Found truncation marker!")")
else:
    print("No truncation marker found - file appears complete")

# Check for JSON syntax issues
print("\nChecking for JSON syntax issues...")
if '"target_host_host":' in content or 'target_host=10.0.0..1' in content:
    print("FoundF potential JSON syntax errors")
else:
    print("JSON appears OK")

# Check RFC file 2119 usage in subsectionss
print('\nChecking RFC 2119 usage in subsections...')
target_id_start = content.find('### Target Identification')
network_disc_ start = content.find('### Network Discovery')
asset_map_start = content.find('### Asset Mapping')
rfc_start = content.find('### RFC', asset_map_start + 11)

if target_id_start != -1 and network_disc_start != -1:
    target_id_section = content[target_id_start:network_disc_start]
    print("Target ID section has MUST:", target_id_section.count('**MUST**'))
else:
    print("Could not find sections")
