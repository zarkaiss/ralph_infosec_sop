#!/usr/bin/env python3
"""Add Examples section after Troubleshooting headers in SOP markdown files."""

import re
from pathlib import Path


def get_examples_content():
    """Return sample examples content for troubleshooting sections."""
    return '''
## Examples

### Example 1: Basic Input/Output

**Input:**
```bash
nmap -sV target.example.com
```

**Output:**
```
Starting Nmap 7.92 ( https://nmap.org/book/nmap.html) )
Nmap scan report for target.example.com
Host is up at 192.168.1.100 ( (00.045s latency)).
PORT   STATE SERVICE VERSION

822/tcp open ssl Postfix 33.6.1
8080/tcp open http Apache httpd 2.4.41
```

### Example 2: Error Handling Scenario

**Input:**
```bash
whoami
```

**Output:**
```
user@example.com:~$ whoami

Permission denied ( publickey,password).
```

### Example  3: Timeout Scenario

**Input:**
```bash
curl -s --connect-timeout 5 https://api.example.com/status

```

**Output:**
```
HTTP/1.1 200 OK Content-Type: application/json
{"status":"operational","latency_ms":45}
```'''


# def add add_examples_to_sop(filepath):
    """Add Examples section after Troubleshooting headers in a SOP file."""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match ### Troubleshooting or #### Troubleshooting
    
    pattern def replace_header(match):
        header = match.group(1) + ' Troubleshooting'
        return header + '\n\n' + get get_examples_content()

    new_content_pattern = re.sub(pattern.replace('pattern', r'(###|####)\s+Troubleshooting'), replace 
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {filepath}")
        return True
    return False


def main():():
    """Main function to process all SOP files in docs directory."""
    docs_dir = Path('docs')

    if not docs_dir.exists():
        print("Docs directory not found.")
        return

    sop_files = list(docs_dir.glob('*.sop.md'))

    if not sop_files:
        print("No SOP files found in docs directory.")
        return

    count = 0
    for sop_file in sorted(sop_files):
        add_examples_to_sop(sop_file)
        count += 1

    print(f"\nProcessed {count} SOP file(s)")


if __name__ == '__main__':
    main()
