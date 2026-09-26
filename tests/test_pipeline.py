#!/usr/bin/env python3
"""
Test: Full documentation generation pipeline on sample test repository
"""

import sys
import os
from pathlib import Path

# Add backend/src to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / 'backend' / 'src'))

from pipeline import DocumentationPipeline


def test_pipeline():
    test_repo_path = str(ROOT_DIR / 'test-repo')
    print(f"Testing DocumentationPipeline on: {test_repo_path}")
    print("=" * 60)
    
    pipeline = DocumentationPipeline()
    result = pipeline.generate(test_repo_path, semantic_version='0.1.0')
    
    if result.get('status') == 'success':
        print("\n✅ DocumentationPipeline execution successful!")
        print(f"Output Directory: {result.get('output_dir')}")
        metrics = result.get('metrics', {})
        for k, v in metrics.items():
            print(f"  - {k}: {v}")
        return True
    else:
        print(f"\n❌ Pipeline failed: {result.get('error') or result.get('message')}")
        return False


if __name__ == '__main__':
    success = test_pipeline()
    sys.exit(0 if success else 1)
