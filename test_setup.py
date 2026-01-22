#!/usr/bin/env python3
"""Quick test script to verify backend setup"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

print("Testing backend setup...")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")

# Test imports
try:
    from parser.ast_parser import CodeParser
    print("✓ Parser module imported successfully")
except ImportError as e:
    print(f"✗ Parser import failed: {e}")

try:
    from llm.client import LLMClient
    print("✓ LLM client module imported successfully")
except ImportError as e:
    print(f"✗ LLM client import failed: {e}")

try:
    from diagram.renderer import DiagramRenderer
    print("✓ Diagram renderer module imported successfully")
except ImportError as e:
    print(f"✗ Diagram renderer import failed: {e}")

try:
    from output.organizer import OutputOrganizer
    print("✓ Output organizer module imported successfully")
except ImportError as e:
    print(f"✗ Output organizer import failed: {e}")

# Test environment variables
print("\nEnvironment variables:")
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('DEEPSEEK_API_KEY')
if api_key:
    print(f"✓ DEEPSEEK_API_KEY: {api_key[:10]}...{api_key[-4:]}")
else:
    print("✗ DEEPSEEK_API_KEY not found")

backend_port = os.getenv('BACKEND_PORT', '8765')
print(f"✓ BACKEND_PORT: {backend_port}")

print("\n✅ Backend setup test complete!")
