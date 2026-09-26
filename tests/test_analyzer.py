"""
Test: Codebase Analyzer, Diagram Registry, and Selector (Phase 1)
"""

import sys
import os
from pathlib import Path
import json

# Add backend/src to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / 'backend' / 'src'))

from analyzer.codebase_analyzer import CodebaseAnalyzer
from diagram.diagram_types import diagram_registry
from diagram.diagram_selector import DiagramSelector
from parser.ast_parser import CodeParser
from parser.dependency_graph import DependencyGraphBuilder


def test_analyzer():
    """Test Codebase Analyzer and Diagram Selector on test-repo"""
    print("=" * 60)
    print("TEST: Codebase Analyzer & Diagram Selector")
    print("=" * 60)
    
    codebase_path = str(ROOT_DIR / 'test-repo')
    
    # Step 1: Parse codebase
    print("\n1. Parsing codebase...")
    parser = CodeParser()
    parsed_files = parser.parse_directory(codebase_path)
    print(f"   ✓ Parsed {len(parsed_files)} files")
    assert len(parsed_files) > 0, "No files parsed from test-repo"
    
    # Step 2: Build dependency graph
    print("\n2. Building dependency graph...")
    graph_builder = DependencyGraphBuilder()
    dependency_graph = graph_builder.build_graph(parsed_files)
    print(f"   ✓ Graph: {dependency_graph['metadata']['total_nodes']} nodes, {dependency_graph['metadata']['total_edges']} edges")
    assert dependency_graph['metadata']['total_nodes'] > 0
    
    # Step 3: Analyze codebase
    print("\n3. Analyzing codebase characteristics...")
    analyzer = CodebaseAnalyzer()
    profile = analyzer.analyze(codebase_path, parsed_files, dependency_graph)
    print(f"   ✓ Primary Language: {profile['language']}")
    print(f"   ✓ Features: {', '.join(profile['features'])}")
    print(f"   ✓ Project Type: {profile['project_type']}")
    print(f"   ✓ Complexity: {profile['complexity']['size_category']} ({profile['complexity']['total_files']} files)")
    
    # Step 4: Diagram registry & selection
    print("\n4. Calculating diagram recommendations...")
    recommendations = diagram_registry.get_recommended_diagrams(profile, max_diagrams=6)
    print(f"   ✓ {len(recommendations)} diagrams recommended")
    
    selector = DiagramSelector()
    selected_diagrams = selector.select_diagrams(profile, max_diagrams=5)
    print(f"   ✓ Selected {len(selected_diagrams)} diagrams for generation")
    assert len(selected_diagrams) > 0
    
    print("\n============================================================")
    print("✅ ANALYZER & SELECTOR TEST COMPLETE")
    print("============================================================")
    return True


if __name__ == '__main__':
    success = test_analyzer()
    sys.exit(0 if success else 1)
