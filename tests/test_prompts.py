"""
Test: Context Extraction & Diagram Prompt Generation (Phase 2)
"""

import sys
import os
from pathlib import Path

# Add backend/src to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / 'backend' / 'src'))

from parser.ast_parser import CodeParser
from parser.dependency_graph import DependencyGraphBuilder
from analyzer.codebase_analyzer import CodebaseAnalyzer
from diagram.diagram_selector import DiagramSelector
from diagram.context_extractors import ContextExtractorFactory
from llm.prompts.diagram_prompts import get_prompt_for_diagram


def test_context_and_prompts():
    """Test context extraction and prompt generation across diagram types."""
    print("=" * 60)
    print("TEST: Context Extraction & Prompt Generation")
    print("=" * 60)
    
    test_repo = str(ROOT_DIR / 'test-repo')
    
    # 1. Parse & build graph
    parser = CodeParser()
    parsed_files = parser.parse_directory(test_repo)
    graph_builder = DependencyGraphBuilder()
    dependency_graph = graph_builder.build_graph(parsed_files)
    
    # 2. Analyze
    analyzer = CodebaseAnalyzer()
    profile = analyzer.analyze(test_repo, parsed_files, dependency_graph)
    
    # 3. Select diagrams
    selector = DiagramSelector()
    selected_diagrams = selector.select_diagrams(profile, max_diagrams=5)
    print(f"✓ Selected {len(selected_diagrams)} diagrams for evaluation")
    
    # 4. Extract contexts & generate prompts
    contexts = {}
    prompts = {}
    for diagram in selected_diagrams:
        dtype = diagram.get('type_id') or diagram.get('type')
        extractor = ContextExtractorFactory.get_extractor(dtype)
        ctx = extractor.extract(dependency_graph, profile)
        contexts[dtype] = ctx
        
        prompt = get_prompt_for_diagram(dtype, ctx)
        prompts[dtype] = prompt
        print(f"✓ {dtype:15s}: context extracted, prompt generated ({len(prompt)} chars)")
        assert len(prompt) >= 200, f"Prompt for {dtype} is too short"
        assert "REQUIREMENTS:" in prompt, f"Prompt for {dtype} missing REQUIREMENTS:"
        assert "MERMAID SYNTAX:" in prompt, f"Prompt for {dtype} missing MERMAID SYNTAX:"
    
    print("\n============================================================")
    print(f"✅ ALL {len(prompts)} PROMPTS GENERATED AND VALIDATED")
    print("============================================================")
    return True


if __name__ == '__main__':
    success = test_context_and_prompts()
    sys.exit(0 if success else 1)
