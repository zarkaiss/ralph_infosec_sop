#!/usr/bin/env python3
import os

def check_sop_metadata(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    
    priority = None
    version = None
    last_updated = None
    status = None
    
    in_yaml_block = False
    
    for line in lines:
        if line.strip() == '---':
            in_yaml_block = True
            continue
        
        if in_yaml_block:
            stripped = line.strip()
            # Exit YAML block on non-empty, non-comment, non-key-value line
            if stripped and not stripped.startswith('#') and ':' not in stripped:
                break
            
            if 'priority:' in line:
                priority = line.split('priority:')[1].strip().split()[0]
            elif 'version:' in line:
                version = line.split('version:')[1].strip().split()[0]
            elif 'last_updated:' in line:
                last_updated = line.split('last_updated:')[1].strip().split()[0]
            elif 'status:' in line:
                status = line.split('status:')[1].strip().split()[0]
    
    # Check if we found all required fields
    has_priority = priority is not None and priority == 'MEDIUM'
    has_version = version is not None and version == '1.0'
    has_last_updated = last_updated is not None and last_updated == '2024-01-15'
    has_status = status is not None and status == 'FINAL'
    
    return {
        'filepath': filepath,
        'has_priority': has_priority,
        'priority': priority,
        'has_version': has_version,
        'version': version,
        'has_last_updated': has_last_updated,
        'last_updated': last_updated,
        'has_status': has_status,
        'status': status
    }

sops = [f for f in os.listdir('docs') if f.endswith('.sop.md')]
results = []

for sop in sorted(sops):
    filepath = f'docs/{sop}'
    result = check_sop_metadata(filepath)
    results.append(result)
    print(f"{sop}: {result}")
