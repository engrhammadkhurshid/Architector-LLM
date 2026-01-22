"""
Test Phase 1: Codebase Analyzer, Diagram Registry, and Selector
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from analyzer.codebase_analyzer import CodebaseAnalyzer
from diagram.diagram_types import diagram_registry
from diagram.diagram_selector import DiagramSelector
from parser.ast_parser import CodeParser
from parser.dependency_graph import DependencyGraphBuilder
import json

def test_phase1():
    """Test Phase 1 components"""
    
    print("="*60)
    print("PHASE 1 TEST: Multi-Diagram System Foundation")
    print("="*60)
    
    # Test on our test-repo
    codebase_path = os.path.join(os.path.dirname(__file__), 'test-repo')
    
    # Step 1: Parse codebase (existing)
    print("\n1. Parsing codebase...")
    parser = CodeParser()
    parsed_files = parser.parse_directory(codebase_path)
    print(f"   ✓ Parsed {len(parsed_files)} files")
    
    # Step 2: Build dependency graph (existing)
    print("\n2. Building dependency graph...")
    graph_builder = DependencyGraphBuilder()
    dependency_graph = graph_builder.build_graph(parsed_files)
    print(f"   ✓ Graph: {dependency_graph['metadata']['total_nodes']} nodes, {dependency_graph['metadata']['total_edges']} edges")
    
    # Step 3: Analyze codebase (NEW)
    print("\n3. Analyzing codebase characteristics...")
    analyzer = CodebaseAnalyzer()
    profile = analyzer.analyze(codebase_path, parsed_files, dependency_graph)
    
    print(f"   ✓ Primary Language: {profile['language']}")
    print(f"   ✓ Features: {', '.join(profile['features'])}")
    print(f"   ✓ Frameworks: {', '.join(profile['frameworks']) if profile['frameworks'] else 'None detected'}")
    print(f"   ✓ Project Type: {profile['project_type']}")
    print(f"   ✓ Has Database: {profile['has_database']}")
    print(f"   ✓ Has API: {profile['has_api']}")
    print(f"   ✓ Complexity: {profile['complexity']['size_category']} ({profile['complexity']['total_files']} files)")
    
    # Step 4: Calculate diagram priorities (NEW)
    print("\n4. Calculating diagram priorities...")
    priorities = diagram_registry.calculate_priorities(profile)
    print(f"   ✓ {len(priorities)} diagrams recommended")
    
    for p in priorities:
        priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[p['priority']]
        print(f"   {priority_emoji} {p['name']} ({p['category']}) - {p['priority'].upper()}")
    
    # Step 5: Select diagrams (NEW)
    print("\n5. Selecting diagrams to generate...")
    selector = DiagramSelector()
    selected_diagrams = selector.select_diagrams(profile, max_diagrams=8)
    
    print(f"   ✓ Selected {len(selected_diagrams)} diagrams for generation")
    print()
    
    for i, diagram in enumerate(selected_diagrams, 1):
        print(f"   [{i}] {diagram['name']}")
        print(f"       Category: {diagram['category']}")
        print(f"       Reason: {diagram['reason']}")
        if diagram.get('scenarios'):
            print(f"       Scenarios: {', '.join(diagram['scenarios'])}")
        print()
    
    # Step 6: Generate selection report
    print("\n6. Selection Report:")
    report = selector.generate_selection_report(selected_diagrams)
    print(f"   Total: {report['total_diagrams']} diagrams")
    print(f"   High Priority: {report['high_priority']}")
    print(f"   Medium Priority: {report['medium_priority']}")
    print(f"\n   By Category:")
    for category, diagrams in report['categories'].items():
        print(f"   - {category.upper()}: {', '.join(diagrams)}")
    
    # Save results
    print("\n7. Saving test results...")
    results = {
        'profile': profile,
        'selected_diagrams': selected_diagrams,
        'report': report
    }
    
    with open('phase1_test_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("   ✓ Results saved to phase1_test_results.json")
    
    print("\n" + "="*60)
    print("✅ PHASE 1 TEST COMPLETE")
    print("="*60)
    print(f"\nNext: Phase 2 will generate {len(selected_diagrams)} diagrams:")
    for d in selected_diagrams:
        print(f"  - {d['name']}")
    print()

if __name__ == '__main__':
    test_phase1()
