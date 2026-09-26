#!/usr/bin/env python3
"""
Test: Documentation generation on test Flask application codebase
"""

import sys
import os
import logging
from pathlib import Path

# Add backend/src to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / 'backend' / 'src'))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
from pipeline import DocumentationPipeline


def test_flask_app():
    codebase_path = str(ROOT_DIR / 'test-flask-app')
    print("=" * 60)
    print(f"Testing DocumentationPipeline on Flask App: {codebase_path}")
    print("=" * 60)
    
    pipeline = DocumentationPipeline()
    result = pipeline.generate(codebase_path, semantic_version='1.0.0')
    
    if result.get('status') == 'success':
        print("\n✅ Documentation generated successfully!")
        metrics = result.get('metrics', {})
        print(f"Files analyzed: {metrics.get('files_analyzed')}")
        print(f"Classes: {metrics.get('total_classes')}, Functions: {metrics.get('total_functions')}")
        print(f"Diagrams: {metrics.get('diagrams_successful')}/{metrics.get('diagrams_generated')}")
        print(f"Output: {result.get('output_dir')}")
        return True
    else:
        print(f"\n❌ Generation failed: {result.get('error')}")
        return False


if __name__ == '__main__':
    success = test_flask_app()
    sys.exit(0 if success else 1)
