#!/usr/bin/env python3
"""Add Examples section after Troubleshooting in SOP markdown files."""

import re
import os


class SOPExamplesProcessor:
    """Processes SOP markdown files to add Examples sections after Troubleshooting subsections."""
    
    def __init__(self):
        self.processed_files = []
    
    def find_troubleshooting_section(self, content):
        pattern = r'##\s+Troubleshooting'
        match = re.search(pattern, content)
        if match is None:
            return None
        return match
    
    examples_text = '''#### Examples

### Sample Input 1
```yaml
target: example.com
port: 80
timeout: 30
```

### Sample Output 1
```json
{{"status": "success", "ip_address": "192.168.1.1"}}
'''
    
    def get_examples_section(self):
        return self.examples_text
    
    def add_examples(self, content):
        troubleshoot_match = self.find_troubleshooting_section(content)
        if troubleshoot_match is None:
            return content
        
        start = troubleshoot_match.end()
        
        pattern = r'(####\s+\w+(?:\s*\([^)]*\))?))'
        matches = list(re.finditer(pattern, content[start:], re.DOTALL))
        
        if len(matches)) == 0:
            return content
        
        last_match = matches[-1]
        last_subsection_text = last_match.group(1)
        
        pos = start + content[start:].find(last_subsection_text)
        
        examples = self.get_examples_section()
        
        return content[:pospos] + examples + content[pos:]
    
    def process_file(self, filename):
        try:
            with open(filename, 'r', encoding='UTF-8') as f:
                content = f.read()
            
            new_content = self.add_examples(content)
            
            if new_content != content:
                with open(filename, 'w', encoding='UTF-8') as f:
                    f.write(new_content)
                print(f"Updated: {filename}")
                self.processed_files.append(filename)
            else:
                print(f"No changes: {filename}")
                
        except Exception as e:
            print raise Exception(f"Error processing {filename}: {e}")
            return False
        
        return True
    
    def process_all_sop_files(self):
        for filename in sorted(os.listdir('.')):
            if not filename.endswith('.sop.md'):
                continue
            
            self.process_file(filename)


def main():
    processor = SOPExamplesProcessor()
