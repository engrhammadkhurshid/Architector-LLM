#!/usr/bin/env python3
"""
Quick CLI wrapper for Architector-LLM
Makes it easy to run from command line on any project.
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend' / 'src'))

from pipeline import DocumentationPipeline


def main():
    """Run Architector-LLM on a codebase."""
    if len(sys.argv) < 2:
        print('Usage: python3 architector.py <codebase-path> [version]')
        print('\nExamples:')
        print('  python3 architector.py ~/projects/my-app')
        print('  python3 architector.py ~/projects/my-app 2.0.0')
        print('  python3 architector.py ~/projects/my-app  # auto-detects version')
        print('\nOr use the test script:')
        print('  python3 test_real_project.py')
        sys.exit(1)
    
    codebase = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else None  # None means auto-detect
    
    print(f'🚀 Architector-LLM')
    print(f'   Analyzing: {codebase}')
    if version:
        print(f'   Version: {version}')
    else:
        print(f'   Version: Auto-detect from project files')
    print()
    
    pipeline = DocumentationPipeline()
    result = pipeline.generate(codebase, version)
    
    if result['status'] == 'success':
        print('\n' + '='*80)
        print('✅ DOCUMENTATION GENERATED')
        print('='*80)
        metrics = result['metrics']
        print(f"\n📊 Metrics:")
        print(f"   Files: {metrics['files_analyzed']}")
        print(f"   Classes: {metrics['total_classes']}")
        print(f"   Functions: {metrics['total_functions']}")
        print(f"   Diagrams: {metrics['diagrams_successful']}/{metrics['diagrams_generated']}")
        print(f"   Quality: {metrics['average_quality_score']:.1f}/100")
        print(f"   Time: {metrics['processing_time']:.1f}s")
        print(f"\n📂 Output: {result['output_dir']}")
        print(f"\nOpen with:")
        print(f"   open {result['output_dir']}/README.md")
    else:
        print(f'\n❌ FAILED: {result.get("error")}')
        sys.exit(1)


if __name__ == '__main__':
    main()
