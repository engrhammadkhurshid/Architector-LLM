#!/usr/bin/env python3
from tree_sitter import Parser
import tree_sitter_python as tspython

# Test new API
parser = Parser()
parser.set_language(tspython.language())
print("✅ New API works with parser.set_language()")
