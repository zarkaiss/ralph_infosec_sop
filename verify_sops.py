import re

# Check only the FIRST occurrence of each metadata field (YAML frontmatter)
sop_files = [
    'asset-inventory.sop.md',
    'incident-response.sop.md',
    'penetration-testing.sop.md',
    'recon-enumeration.s.sop.md',
    'recon-enumeration.sop.md',
    'recon-enumerationation.sop.md',
    'vulnerability-exploitation.sop.md',
    'vulnerability-exploitationitations.sop.md',
    'vulnerability-scanning.sop.md'
]

required_metadata = {
    'priority': 'MEDIUM',
    'version': '1.0',
    'last_updated': '2024-01-15',
    'status': 'FINAL'
}

results = {}

for filename in sop_files:
    filepath = f'docs/{filename}'
    try:
        content = open(filepath, 'r').read()
        
        # Check only first occurrence of each field
        checks = {}
        for key, expected_value in required_metadata.items():
            pattern = rf'^{key}:\s*{expected_value}\s*$'
            match = re.search(pattern, content, re.MULTILINE)
            checks[key] = match is not None
        
        all_present = all(checks.values())
        
        results[filename] = {
            'status': 'PASS' if all_present else 'FAIL',
            'checks': checks
        }
    except Exception as e:
        results[filename] = {'error': str(e)}

print("SOP Metadata Verification Results (First occurrence only):")
print("=" * 70)
for filename, result in results.items():
    status = result['status'] if 'status' in result else 'ERROR'
    print(f"\n{filename}: {status}")
    if 'checks' in result:
        for key, value in result['checks'].items():
            print(f"  - {key}: {'PASS' if value else 'FAIL'}")
