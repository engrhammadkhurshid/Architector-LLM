"""
Test: Diagram Quality Validation & Quality Report Generation (Phase 3)
"""

import sys
import os
import json
from pathlib import Path

# Add backend/src to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / 'backend' / 'src'))

from validation.diagram_validator import DiagramValidator
from validation.quality_report import QualityReportGenerator

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


def test_quality_validation():
    """Test DiagramValidator 4-dimension scoring and QualityReportGenerator"""
    print("=" * 60)
    print("TEST: Diagram Quality Validation System")
    print("=" * 60)
    
    validator = DiagramValidator()
    validation_results = {}
    
    for dtype, code in SAMPLE_DIAGRAMS.items():
        ctx = SAMPLE_CONTEXTS.get(dtype, {})
        result = validator.validate(dtype, code, ctx)
        validation_results[dtype] = result
        print(f"✓ {dtype:12s}: Overall={result['overall_score']:.1f}/100 | Syntax={result['scores']['syntax']:.1f} | Completeness={result['scores']['completeness']:.1f} | Clarity={result['scores']['clarity']:.1f}")
        assert result['overall_score'] >= 70.0, f"{dtype} score {result['overall_score']} is below minimum threshold"
        assert result['validated'] is True, f"{dtype} validation was not marked validated"
    
    # Mock diagram results for report generator
    diagram_results = {
        dtype: {'success': True, 'mermaid_code': code, 'metadata': {'category': 'Structural', 'type_id': dtype}}
        for dtype, code in SAMPLE_DIAGRAMS.items()
    }
    
    report_gen = QualityReportGenerator()
    quality_report = report_gen.generate(
        validation_results,
        diagram_results,
        {'generated_at': '2026-01-22T10:00:00', 'semantic_version': '1.0.0'}
    )
    assert "Architecture Documentation Quality Report" in quality_report
    assert "Score Breakdown" in quality_report
    print("✓ Quality report markdown generated successfully")
    
    print("\n============================================================")
    print("✅ QUALITY VALIDATION TESTS PASSED")
    print("============================================================")
    return True


if __name__ == '__main__':
    success = test_quality_validation()
    sys.exit(0 if success else 1)
