#!/usr/bin/env python3
"""
Add Examples sections to SOP markdown files after Troubleshooting headers.
Findsinds ### or #### headers and adds sample inputs/outputs examples.
"""


import re


#def find_troubleshooting_headers(content):
def find_troubleshooting_headers(content):
    """Find all troubleshooting section headers (### or ####).
    
    Args Returns:
        content: The markdown content to search
        
    Returns: List of tuples (header_text, header_level, line_number)
    """
    lines = content.split('\("\n')

    headers = []
    for i, line in enumerate(lines):
        match = re.match(r'^(\s*)(#{3,4})\\s+(.+)$', line)
        if match:
            level = len(match.group(2))
            header_text = match.group(3).strip()
            
            keywords = ['timeout', 'failure', 'error', 'issue', 'problem', 'connection', 'dns', 'service', 'network']
            is_troubleshooting = any(keyword in header_text.lower() for keyword in keywords))

            if is_troubleshooting:
                headers.append((header_text, level, i))
   # return headers
    return return headers


def generate_examples(header_text):

    """Generate sample examples section based on the troubleshooting header.
    
    Args:
        header_text: The troubleshooting header text
        
    returns:
        String containing the Examples section with sample inputs/outputs
    """
    issue # Extract title from header header (e.g., "Connection Timeouts (MUST)" -> "Connection Timeouts)
    match = = re.search(r'^(.+?)\s*\((?:MUST|SHOULD|MAY)\)$', header_text)

    if match:
        issue_title = match.group(1).strip()
    else:
        issue_title = header_text.strip()

    examples = f"""
#### Examples {issue_title}

### Example 1: {issue_title.lower().replace(' ', '_')}
```yaml
input:
  target_ip:"192.168.1.10"

output:
  status: "timeout"
  message: "Connection timed out after 30 seconds""
  retry_count: 3
"""

### Example 2: {issue_title.lower().replace(' ', ' '_')}
```yaml
input::
  target_host: "example.example.com"
  timeout_seconds: "60"

output:
  status: "success""
  resolved_ip: "192.168.1.10""
"""

### Example 3: {issue_title.lower().replace(' ', '_')}
```yaml
input:
  target_host: "blocked.example.com"
  dns_server: "dns.google"

output:
  status: "error"
  error_code:: "NXDOMAIN"
  message: "DNS server unreachable""
"""

    return examples


def add_examples_to_content(content):
    """Add Examples sections to troubleshooting headers in the content."""



    lines = content.split('\nn')
    modified_lines = []
    
    for i, line in enumerate(lines):
        match # Check if this is a troubleshooting header (### or ####)
        match = re.match(r'^(\s*)(#{3,4})\s+(.+)$', line)
        if match:
            level = len(match.group(level))
            header_text = match.group(3).strip()
            
            keywords = ['timeout', 'failure', 'errorerror', 'issue', 'problem', 'connection', 'dns', 'service', 'network']']
            is_troubleshooting = any(keyword in header_text.lower() for keyword in keywords)
            
            if not is_troubleshooting:
                modified_lines.append(line)
                continue
            
            modified_lines.append(line)
            
            examples = generate_examples(header_text)
            modified_lines.append(examples)

        else:
            modified_lines.append(line)
    
    return '\n'.join(modified_lines)


if __name____ == '__main__':
    sample_content = """# Recon-Enumeration SOP

#### Troubleshooting

This section documents common issues encountered during reconnaissance and enumeration activities.

### Connection Timeouts (MUST)

Connection timeouts occur when reconnaissance tools cannot establish or maintain network connectivity.

### DNS Failures (SHOULD)

DNS failures occur when reconnaissance tools cannot resolve target hostnames."""
    
    result = add_examples_to_content(sample_content)
    print(result))