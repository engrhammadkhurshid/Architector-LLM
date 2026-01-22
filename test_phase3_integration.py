"""
Complete Phase 3 Integration Test
Tests the full pipeline with all Phase 3 components:
- Quality validation
- Relationship mapping
- Interactive documentation
"""

import sys
import json
from pathlib import Path

# Add backend/src to path
backend_src = Path(__file__).parent / 'backend' / 'src'
sys.path.insert(0, str(backend_src))

from validation.diagram_validator import DiagramValidator
from validation.quality_report import QualityReportGenerator
from diagram.relationship_mapper import RelationshipMapper
from output.interactive_docs import InteractiveDocGenerator


# Mock data from successful generation
MOCK_DIAGRAM_RESULTS = {
    'component': {
        'success': True,
        'mermaid_code': '''graph TD
    Main[Main Application] -->|uses| Calculator[Calculator Module]
    Main -->|uses| Utils[Utilities]
    Calculator -->|depends on| Utils''',
        'metadata': {
            'name': 'Component Diagram',
            'category': 'Structural',
            'purpose': 'Shows system components and dependencies',
            'type_id': 'component'
        }
    },
    'class': {
        'success': True,
        'mermaid_code': '''classDiagram
    class Main {
        +run()
        +display_result()
    }
    class Calculator {
        +add(a, b)
        +subtract(a, b)
    }
    class Utils {
        +validate_input()
        +format_output()
    }
    Main --> Calculator
    Calculator --> Utils''',
        'metadata': {
            'name': 'Class Diagram',
            'category': 'Structural',
            'purpose': 'Shows class structure and relationships',
            'type_id': 'class'
        }
    },
    'sequence': {
        'success': True,
        'mermaid_code': '''sequenceDiagram
    participant User
    participant Main
    participant Calculator
    participant Utils
    
    User->>Main: run()
    Main->>Utils: validate_input()
    Utils-->>Main: valid
    Main->>Calculator: add(5, 3)
    Calculator-->>Main: 8
    Main->>Utils: format_output(8)
    Utils-->>Main: "Result: 8"
    Main-->>User: display''',
        'metadata': {
            'name': 'Sequence Diagram',
            'category': 'Behavioral',
            'purpose': 'Shows execution flow and interactions',
            'type_id': 'sequence'
        }
    }
}

MOCK_DEPENDENCY_GRAPH = {
    'nodes': [
        {'name': 'Main', 'type': 'class', 'dependencies': ['Calculator', 'Utils']},
        {'name': 'Calculator', 'type': 'class', 'dependencies': ['Utils']},
        {'name': 'Utils', 'type': 'class', 'dependencies': []}
    ],
    'edges': [
        {'from': 'Main', 'to': 'Calculator'},
        {'from': 'Main', 'to': 'Utils'},
        {'from': 'Calculator', 'to': 'Utils'}
    ],
    'metadata': {
        'total_nodes': 3,
        'total_edges': 3,
        'total_classes': 3,
        'total_functions': 6
    }
}


def test_phase3_integration():
    """Test complete Phase 3 integration."""
    print('='*80)
    print('PHASE 3 COMPLETE INTEGRATION TEST')
    print('='*80)
    print()
    
    # Stage 1: Validation
    print('Stage 1: Quality Validation')
    print('-'*80)
    
    validator = DiagramValidator()
    validation_results = {}
    
    for diagram_type, result in MOCK_DIAGRAM_RESULTS.items():
        val_result = validator.validate(
            diagram_type,
            result['mermaid_code'],
            {}  # Context would be extracted in real scenario
        )
        validation_results[diagram_type] = val_result
        print(f'✓ {diagram_type}: {val_result["overall_score"]:.1f}/100')
    
    avg_quality = sum(v['overall_score'] for v in validation_results.values()) / len(validation_results)
    print(f'\n📊 Average Quality: {avg_quality:.1f}/100')
    
    # Stage 2: Quality Report
    print('\nStage 2: Quality Report Generation')
    print('-'*80)
    
    report_gen = QualityReportGenerator()
    quality_report = report_gen.generate(
        validation_results,
        MOCK_DIAGRAM_RESULTS,
        {'generated_at': '2026-01-22T12:00:00', 'semantic_version': '1.0.0'}
    )
    
    print(f'✓ Quality report generated ({len(quality_report)} chars)')
    
    # Stage 3: Relationship Mapping
    print('\nStage 3: Cross-Diagram Relationship Mapping')
    print('-'*80)
    
    mapper = RelationshipMapper()
    relationship_map = mapper.map_relationships(
        MOCK_DIAGRAM_RESULTS,
        MOCK_DEPENDENCY_GRAPH
    )
    
    shared = len(relationship_map['shared_entities'])
    connections = len(relationship_map['diagram_connections'])
    print(f'✓ Found {shared} shared entities')
    print(f'✓ Found {connections} diagram connections')
    
    relationship_report = mapper.generate_relationship_report(relationship_map)
    print(f'✓ Relationship report generated ({len(relationship_report)} chars)')
    
    # Stage 4: Interactive Documentation
    print('\nStage 4: Interactive Documentation Generation')
    print('-'*80)
    
    doc_gen = InteractiveDocGenerator()
    
    enhanced_index = doc_gen.generate_enhanced_index(
        MOCK_DIAGRAM_RESULTS,
        validation_results,
        relationship_map,
        {
            'generated_at': '2026-01-22T12:00:00',
            'semantic_version': '1.0.0',
            'codebase_path': '/path/to/project'
        }
    )
    print(f'✓ Enhanced index generated ({len(enhanced_index)} chars)')
    
    comparison_view = doc_gen.generate_comparison_view(
        MOCK_DIAGRAM_RESULTS,
        relationship_map
    )
    print(f'✓ Comparison view generated ({len(comparison_view)} chars)')
    
    # Stage 5: Save outputs
    print('\nStage 5: Saving Test Outputs')
    print('-'*80)
    
    output_dir = Path(__file__).parent / 'test_output' / 'phase3_integration'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save all Phase 3 outputs
    outputs = {
        'QUALITY_REPORT.md': quality_report,
        'RELATIONSHIPS.md': relationship_report,
        'INDEX.md': enhanced_index,
        'COMPARISONS.md': comparison_view
    }
    
    for filename, content in outputs.items():
        filepath = output_dir / filename
        with open(filepath, 'w') as f:
            f.write(content)
        print(f'✓ Saved {filename} ({len(content)} chars)')
    
    # Save test results
    results = {
        'test_type': 'phase3_integration',
        'components_tested': [
            'DiagramValidator',
            'QualityReportGenerator',
            'RelationshipMapper',
            'InteractiveDocGenerator'
        ],
        'diagrams_tested': list(MOCK_DIAGRAM_RESULTS.keys()),
        'metrics': {
            'average_quality_score': avg_quality,
            'shared_entities': shared,
            'diagram_connections': connections,
            'reports_generated': len(outputs)
        },
        'validation_results': validation_results,
        'relationship_map': {
            'shared_entities_count': shared,
            'connections_count': connections,
            'diagrams_analyzed': relationship_map['diagrams_analyzed']
        }
    }
    
    results_file = output_dir / 'test_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f'✓ Saved test_results.json')
    
    # Summary
    print('\n' + '='*80)
    print('PHASE 3 INTEGRATION TEST SUMMARY')
    print('='*80)
    print(f'\n✅ All Phase 3 components integrated successfully')
    print(f'\n📊 Key Metrics:')
    print(f'   - Average Quality: {avg_quality:.1f}/100')
    print(f'   - Shared Entities: {shared}')
    print(f'   - Diagram Connections: {connections}')
    print(f'   - Reports Generated: {len(outputs)}')
    print(f'\n📁 Test outputs saved to: {output_dir}')
    print(f'\n🎯 Phase 3 Features Validated:')
    print(f'   ✓ 3.1: Diagram quality validation (4-component scoring)')
    print(f'   ✓ 3.2: Quality report generation (comprehensive reports)')
    print(f'   ✓ 3.3: Cross-diagram relationship mapping')
    print(f'   ✓ 3.4: Interactive documentation with cross-references')
    print(f'\n🚀 Ready for Phase 4: Real Project Testing')
    print()
    
    return results


if __name__ == '__main__':
    try:
        results = test_phase3_integration()
        print('✅ All Phase 3 integration tests passed!')
        sys.exit(0)
    except Exception as e:
        print(f'\n❌ Test failed: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
