#!/usr/bin/env python3
import sys
sys.stdout.reconfigure(encoding='utf-8')
content = open('test_validate_sop.py', encoding='utf-8').read()
lines = content.split('\n')
for i, line in enumerate(lines[150:200], start=150):
    print(f'{i}: {line}')
