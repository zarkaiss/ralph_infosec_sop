import re
from pathlib import Path

RFC2119_KEYWORDS = {'MUST', 'SHALL', 'SHOULD', 'COULD', 'MAY', 'MIGHT'}

def validate_sop(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Check for markdown headers (## or ###)
    has_headers = bool(re.search(r'#{2,3}\s', content))
    
    # Just check if headers exist
    return bool(has_headers)

if __name__ == '__main__':
    docs_dir = Path('docs')
    sop_files = list(docs_dir.glob('*.sop.md'))
    
    for filepath in sop_files:
        result = validate_sop(filepath)
        print(f"{filepath.name}: {result}")