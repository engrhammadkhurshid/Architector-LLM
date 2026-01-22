#!/usr/bin/env python3
"""
Test the documentation pipeline directly without HTTP
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from pipeline import DocumentationPipeline

# Test with our test-repo
test_repo_path = os.path.join(os.path.dirname(__file__), 'test-repo')

print(f"Testing documentation generation for: {test_repo_path}")
print("=" * 60)

# Create pipeline
pipeline = DocumentationPipeline()

# Generate documentation
print("\nGenerating documentation...")
result = pipeline.generate(test_repo_path, semantic_version='0.1.0')

print("\n" + "=" * 60)
print("RESULT:")
print("=" * 60)

if result['status'] == 'success':
    print(f"✅ Success!")
    print(f"\nOutput Directory: {result['output_dir']}")
    print(f"\nMetrics:")
    for key, value in result['metrics'].items():
        print(f"  - {key}: {value}")
    
    print(f"\nSaved Files:")
    for key, path in result['saved_files'].items():
        print(f"  - {key}: {path}")
else:
    print(f"❌ Failed: {result.get('message', 'Unknown error')}")
    if 'processing_time' in result:
        print(f"Processing time: {result['processing_time']:.2f}s")
