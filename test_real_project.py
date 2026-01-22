"""
Direct pipeline test - run generation without Flask server
"""

import sys
import logging
from pathlib import Path

# Add backend/src to path
backend_src = Path(__file__).parent / 'backend' / 'src'
sys.path.insert(0, str(backend_src))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from pipeline import DocumentationPipeline


def main():
    """Run the pipeline on test Flask app."""
    codebase_path = str(Path(__file__).parent / 'test-flask-app')
    
    print('='*80)
    print('PHASE 4: REAL PROJECT TEST')
    print('='*80)
    print(f'\n📁 Project: Flask Blog Application')
    print(f'   Path: {codebase_path}')
    print()
    
    pipeline = DocumentationPipeline()
    
    result = pipeline.generate(codebase_path, semantic_version='1.0.0')
    
    if result['status'] == 'success':
        print('\n' + '='*80)
        print('✅ DOCUMENTATION GENERATED SUCCESSFULLY')
        print('='*80)
        print(f'\n📊 Metrics:')
        metrics = result['metrics']
        print(f'   - Files Analyzed: {metrics["files_analyzed"]}')
        print(f'   - Classes Found: {metrics["total_classes"]}')
        print(f'   - Functions Found: {metrics["total_functions"]}')
        print(f'   - Diagrams Generated: {metrics["diagrams_successful"]}/{metrics["diagrams_generated"]}')
        print(f'   - Average Quality: {metrics["average_quality_score"]:.1f}/100')
        print(f'   - Shared Entities: {metrics["shared_entities"]}')
        print(f'   - Diagram Connections: {metrics["diagram_connections"]}')
        print(f'   - Processing Time: {metrics["processing_time"]}s')
        print(f'\n📂 Output Directory: {result["output_dir"]}')
        print(f'\n📄 Generated Files:')
        for key, path in result['saved_files'].items():
            print(f'   - {key}: {Path(path).name}')
        print()
    else:
        print('\n❌ GENERATION FAILED')
        print(f'Error: {result.get("error")}')
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
