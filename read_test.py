import codecs
with codecs.open('test_validate_sop.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines[700:900], start=700):
        print(f"{i}: {repr(line)}")
