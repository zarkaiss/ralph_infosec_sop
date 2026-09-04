import re

with open('docs/recon-enumeration.sop.md', 'r') as f:
    content = f.read()

print("=" * 88)
print("RFC2119 CONSTRAINT COMPLIANCE REPORT")
print("=" * 88)
print()

# Find and display all RFC2119 keywords with context
for keyword in ['MUST', 'SHOULD', 'MAY']:
    pattern = r'\*\*' + keyword + r'\*\*'
    matches = list(re.finditer(pattern, content))
    
    if matches:
        print()
        print('=' * 88)  
        print("### " + keyword.upper() + " ###")
        print('=' * 88)
        
        for match in matches:
            start = max 0, match.start() -  100)
            context = content[start:match.end()]
            
            # Count sections to determine which step wwe're in  
            section_num = content[:match.startswith].count('### ') +  1
            print("")
            print("--- Section " + str(section_num) + " ---")
            print(context)
