#!/usr/bin/env python3
"""Quick test script to verify backend setup and environment"""

import sys
import os
from pathlib import Path

# Add backend to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / 'backend' / 'src'))

def main():
    print("Testing backend setup...")
    print(f"Python version: {sys.version}")
    print(f"Project root: {ROOT_DIR}")

    # Test imports
    modules = [
        ("Parser", "parser.ast_parser", "CodeParser"),
        ("LLM Client", "llm.client", "LLMClient"),
        ("Diagram Renderer", "diagram.renderer", "DiagramRenderer"),
        ("Output Organizer", "output.organizer", "OutputOrganizer"),
        ("Codebase Analyzer", "analyzer.codebase_analyzer", "CodebaseAnalyzer"),
        ("Diagram Validator", "validation.diagram_validator", "DiagramValidator"),
        ("Pipeline", "pipeline", "DocumentationPipeline"),
    ]

    all_passed = True
    for name, mod_path, cls_name in modules:
        try:
            mod = __import__(mod_path, fromlist=[cls_name])
            getattr(mod, cls_name)
            print(f"✓ {name} imported successfully")
        except Exception as e:
            print(f"✗ {name} import failed: {e}")
            all_passed = False

    # Test environment variables
    print("\nEnvironment configuration:")
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / '.env')

    api_key = os.getenv('DEEPSEEK_API_KEY')
    if api_key:
        print(f"✓ DEEPSEEK_API_KEY: configured ({api_key[:6]}...{api_key[-4:]})")
    else:
        print("ℹ DEEPSEEK_API_KEY: not set (required only for DeepSeek cloud provider)")

    llm_provider = os.getenv('LLM_PROVIDER', 'ollama')
    print(f"✓ LLM_PROVIDER: {llm_provider}")

    backend_port = os.getenv('BACKEND_PORT', '8765')
    print(f"✓ BACKEND_PORT: {backend_port}")

    if all_passed:
        print("\n✅ Backend setup test complete!")
        return 0
    else:
        print("\n❌ Backend setup test failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
