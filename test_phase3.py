"""
Phase 3 Test: Quality Validation System
Tests DiagramValidator and QualityReportGenerator
"""

import sys
import os
import json
from pathlib import Path

# Add backend/src to path
backend_src = Path(__file__).parent / 'backend' / 'src'
sys.path.insert(0, str(backend_src))

from validation.diagram_validator import DiagramValidator
from validation.quality_report import QualityReportGenerator


# Sample Mermaid diagrams for testing
SAMPLE_DIAGRAMS = {
    'component': """graph TD
    A[Main Application] -->|Uses| B[Calculator Module]
    A -->|Uses| C[Utilities]
    B -->|Depends on| C
    
    subgraph External
        D[Python Standard Lib]
    end
    
    C -->|Uses| D""",
    
    'class': """classDiagram
    class Calculator {
        +int result
        +add(a, b) int
        +subtract(a, b) int
        +multiply(a, b) int
        +divide(a, b) float
    }
    
    class ScientificCalculator {
        +power(base, exp) float
        +sqrt(num) float
    }
    
    class Utils {
        +validate_input(value) bool
        +format_result(value) str
    }
    
    Calculator <|-- ScientificCalculator
    Calculator --> Utils : uses""",
    
    'sequence': """sequenceDiagram
    participant User
    participant Main
    participant Calculator
    participant Utils
    
    User->>Main: run()
    activate Main
    Main->>Calculator: add(5, 3)
    activate Calculator
    Calculator->>Utils: validate_input(5)
    activate Utils
    Utils-->>Calculator: True
    deactivate Utils
    Calculator-->>Main: 8
    deactivate Calculator
    Main-->>User: Display result
    deactivate Main""",
    
    'activity': """graph TD
    Start([Start]) --> GetInput[Get User Input]
    GetInput --> Validate{Valid Input?}
    Validate -->|No| Error[Show Error]
    Error --> GetInput
    Validate -->|Yes| Calculate[Perform Calculation]
    Calculate --> Format[Format Result]
    Format --> Display[Display to User]
    Display --> Continue{Continue?}
    Continue -->|Yes| GetInput
    Continue -->|No| End([End])""",
    
    'data_flow': """graph LR
    Input[(User Input)] --> Validate[Input Validator]
    Validate --> Process[Calculation Engine]
    Process --> Format[Result Formatter]
    Format --> Output[(Display)]
    
    Process --> Log[("Log File")]
    Process --> Cache[("Result Cache")]""",
}

# Sample contexts
SAMPLE_CONTEXTS = {
    'component': {
        'components': ['main', 'calculator', 'utils'],
        'external_dependencies': ['sys', 'os']
    },
    'class': {
        'classes': [
            {'name': 'Calculator', 'methods': ['add', 'subtract', 'multiply', 'divide'], 'attributes': ['result']},
            {'name': 'ScientificCalculator', 'methods': ['power', 'sqrt'], 'attributes': []},
            {'name': 'Utils', 'methods': ['validate_input', 'format_result'], 'attributes': []}
        ],
        'relationships': [
            {'from': 'Calculator', 'to': 'ScientificCalculator', 'type': 'inheritance'},
            {'from': 'Calculator', 'to': 'Utils', 'type': 'dependency'}
        ]
    },
    'sequence': {
        'participants': ['User', 'Main', 'Calculator', 'Utils'],
        'key_interactions': ['run', 'add', 'validate_input']
    },
    'activity': {
        'start_points': ['Start'],
        'end_points': ['End'],
        'key_functions': ['GetInput', 'Validate', 'Calculate', 'Format', 'Display']
    },
    'data_flow': {
        'data_sources': ['User Input'],
        'data_sinks': ['Display', 'Log File', 'Result Cache'],
        'transformations': ['Input Validator', 'Calculation Engine', 'Result Formatter']
    }
}


def test_diagram_validator():
    """Test DiagramValidator with sample diagrams."""
    print('='*80)
    print('PHASE 3 TEST: Diagram Quality Validation')
    print('='*80)
    print()
    
    validator = DiagramValidator()
    results = {}
    
    print('Stage 1: Validating Individual Diagrams')
    print('-'*80)
    
    for diagram_type, mermaid_code in SAMPLE_DIAGRAMS.items():
        print(f'\n🔍 Validating {diagram_type} diagram...')
        
        context = SAMPLE_CONTEXTS.get(diagram_type, {})
        result = validator.validate(diagram_type, mermaid_code, context)
        results[diagram_type] = result
        
        # Display results
        print(f'   Overall Score: {result["overall_score"]:.1f}/100')
        print(f'   Scores:')
        for dimension, score in result['scores'].items():
            emoji = '✅' if score >= 85 else '⚠️' if score >= 70 else '❌'
            print(f'     - {dimension.title()}: {score:.1f}/100 {emoji}')
        
        if result['issues']:
            print(f'   Issues ({len(result["issues"])}):')
            for issue in result['issues'][:3]:  # First 3 issues
                print(f'     - {issue}')
        
        if result['recommendations']:
            print(f'   Recommendations ({len(result["recommendations"])}):')
            for rec in result['recommendations'][:2]:  # First 2 recommendations
                print(f'     - {rec}')
    
    print('\n' + '='*80)
    print('Stage 2: Quality Report Generation')
    print('-'*80)
    
    # Create mock diagram_results
    diagram_results = {}
    for diagram_type, mermaid_code in SAMPLE_DIAGRAMS.items():
        diagram_results[diagram_type] = {
            'success': True,
            'mermaid_code': mermaid_code,
            'metadata': {
                'category': {
                    'component': 'Structural',
                    'class': 'Structural',
                    'sequence': 'Behavioral',
                    'activity': 'Behavioral',
                    'data_flow': 'Data'
                }.get(diagram_type, 'Other'),
                'type_id': diagram_type
            }
        }
    
    # Generate quality report
    report_gen = QualityReportGenerator()
    quality_report = report_gen.generate(
        results,
        diagram_results,
        {'generated_at': '2026-01-22T10:00:00', 'semantic_version': '1.0.0'}
    )
    
    print('\n✅ Quality Report Generated')
    print(f'   Length: {len(quality_report)} characters')
    print(f'   Lines: {len(quality_report.splitlines())}')
    
    # Save report to file
    output_dir = Path(__file__).parent / 'test_output'
    output_dir.mkdir(exist_ok=True)
    
    report_path = output_dir / 'QUALITY_REPORT.md'
    with open(report_path, 'w') as f:
        f.write(quality_report)
    print(f'   Saved to: {report_path}')
    
    # Display report preview (first 50 lines)
    print('\n📄 Quality Report Preview (first 50 lines):')
    print('-'*80)
    for i, line in enumerate(quality_report.splitlines()[:50], 1):
        print(line)
    print('   ...')
    
    print('\n' + '='*80)
    print('Stage 3: Validation Results Summary')
    print('-'*80)
    
    total_diagrams = len(results)
    avg_overall = sum(r['overall_score'] for r in results.values()) / total_diagrams
    
    # Score breakdown
    avg_syntax = sum(r['scores']['syntax'] for r in results.values()) / total_diagrams
    avg_completeness = sum(r['scores']['completeness'] for r in results.values()) / total_diagrams
    avg_clarity = sum(r['scores']['clarity'] for r in results.values()) / total_diagrams
    avg_accuracy = sum(r['scores']['accuracy'] for r in results.values()) / total_diagrams
    
    print(f'\n✅ Validated {total_diagrams} diagrams')
    print(f'   Average Overall Score: {avg_overall:.1f}/100')
    print(f'   Score Breakdown:')
    print(f'     - Syntax:       {avg_syntax:.1f}/100')
    print(f'     - Completeness: {avg_completeness:.1f}/100')
    print(f'     - Clarity:      {avg_clarity:.1f}/100')
    print(f'     - Accuracy:     {avg_accuracy:.1f}/100')
    
    # Quality rating
    if avg_overall >= 90:
        rating = '🟢 Excellent'
    elif avg_overall >= 80:
        rating = '🟡 Good'
    elif avg_overall >= 70:
        rating = '🟠 Fair'
    else:
        rating = '🔴 Needs Improvement'
    
    print(f'\n   Overall Quality: {rating}')
    
    # Save test results
    results_path = output_dir / 'phase3_test_results.json'
    with open(results_path, 'w') as f:
        json.dump({
            'test_type': 'phase3_validation',
            'diagrams_tested': list(SAMPLE_DIAGRAMS.keys()),
            'validation_results': results,
            'summary': {
                'total_diagrams': total_diagrams,
                'average_overall_score': avg_overall,
                'average_syntax': avg_syntax,
                'average_completeness': avg_completeness,
                'average_clarity': avg_clarity,
                'average_accuracy': avg_accuracy,
                'quality_rating': rating
            }
        }, f, indent=2)
    print(f'\n💾 Test results saved to: {results_path}')
    
    print('\n' + '='*80)
    print('✅ PHASE 3 TEST COMPLETED')
    print('='*80)
    
    return results, quality_report


if __name__ == '__main__':
    try:
        results, report = test_diagram_validator()
        print('\n✅ All tests passed!')
        sys.exit(0)
    except Exception as e:
        print(f'\n❌ Test failed: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
