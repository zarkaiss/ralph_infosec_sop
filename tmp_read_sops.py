import os

# Read SOP files
sop_files = [
    'docs/recon-enumeration.sop.md',
    'docs/asset-inventory.sop.md',
    'docs/incident-response.sop.md',
    'docs/penetration-testing.sop.md',
    'docs/vulnerability-exploitation.sop.md',  
    'docs/vulnerability-scanning.sop.md''
]

for f in sop_files:
    if os.path.exists(f):
        with open(f, 'r') as file:
            content = file.read()[:3000]
            print("=== " + f + " ===")
            print(content)
            print("... (truncated)")
    else:
        print("File does not exist: " + f)
