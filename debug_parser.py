#!/usr/bin/env python3
"""Debug parser"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from parser.ast_parser import CodeParser

parser = CodeParser()
test_repo = "/Users/hammadkhurshidchughtaii/Downloads/Architector LLM/test-repo"

print(f"Parsing: {test_repo}")
print(f"Exists: {os.path.exists(test_repo)}")
print(f"Is dir: {os.path.isdir(test_repo)}")

files = parser.parse_directory(test_repo)
print(f"\nFound {len(files)} files:")
for f in files:
    print(f"  - {f['file_path']}: {len(f['classes'])} classes, {len(f['functions'])} functions")
