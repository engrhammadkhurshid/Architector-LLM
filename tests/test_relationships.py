"""
Test: Cross-Diagram Relationship Mapping & Interactive Docs
"""

import sys
import os
from pathlib import Path

# Add backend/src to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / 'backend' / 'src'))

from diagram.relationship_mapper import RelationshipMapper
from output.interactive_docs import InteractiveDocGenerator


def test_relationships_and_interactive_docs():
    """Test entity correlation and cross-diagram linking"""
    print("=" * 60)
    print("TEST: Cross-Diagram Relationships & Navigation")
    print("=" * 60)
    
    diagrams = {
        'component': """graph TD
        Main[Main Application] --> Calculator[Calculator Module]
        Calculator --> Utils[Utils Module]""",
        'class': """classDiagram
        class Calculator {
            +add()
        }
        class Utils {
            +validate()
        }
        Calculator --> Utils""",
        'sequence': """sequenceDiagram
        participant Main
        participant Calculator
        participant Utils
        Main->>Calculator: run()
        Calculator->>Utils: validate()"""
    }
    
    diagram_results = {
        dtype: {'success': True, 'mermaid_code': code, 'metadata': {'category': 'Structural', 'type_id': dtype}}
        for dtype, code in diagrams.items()
    }
    
    # 1. Relationship Mapping
    mapper = RelationshipMapper()
    relationships = mapper.map_relationships(diagram_results)
    print(f"✓ Found {len(relationships.get('shared_entities', []))} shared entities across diagrams")
    print(f"✓ Found {len(relationships.get('diagram_connections', []))} inter-diagram connections")
    
    rel_markdown = mapper.generate_relationship_report(relationships)
    assert "Cross-Diagram Relationship Analysis" in rel_markdown
    print("✓ RELATIONSHIPS.md generated successfully")
    
    # 2. Interactive Navigation Generator
    doc_gen = InteractiveDocGenerator()
    validation_results = {
        dtype: {'overall_score': 90.0, 'scores': {'syntax': 95, 'completeness': 85, 'clarity': 90, 'accuracy': 90}}
        for dtype in diagrams.keys()
    }
    index_md = doc_gen.generate_enhanced_index(
        diagram_results=diagram_results,
        validation_results=validation_results,
        relationship_map=relationships,
        metadata={'generated_at': '2026-01-24', 'semantic_version': '2.1.0', 'codebase_path': str(ROOT_DIR / 'test-repo')}
    )
    assert "Architecture Documentation Index" in index_md
    print("✓ Enhanced INDEX.md generated successfully")
    
    print("\n============================================================")
    print("✅ RELATIONSHIPS & INTERACTIVE DOCS TEST PASSED")
    print("============================================================")
    return True


if __name__ == '__main__':
    success = test_relationships_and_interactive_docs()
    sys.exit(0 if success else 1)
