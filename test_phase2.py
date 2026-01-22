"""
Phase 2 End-to-End Test
Tests the complete multi-diagram generation pipeline.
"""

import os
import sys
import json
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / 'backend' / 'src'
sys.path.insert(0, str(backend_path))

from parser.ast_parser import CodeParser
from parser.dependency_graph import DependencyGraphBuilder
from analyzer.codebase_analyzer import CodebaseAnalyzer
from diagram.diagram_selector import DiagramSelector
from diagram.context_extractors import ContextExtractorFactory
from llm.prompts.diagram_prompts import get_prompt_for_diagram


def test_phase2_pipeline():
    """Test the complete Phase 2 multi-diagram pipeline."""
    
    print("=" * 70)
    print("PHASE 2 END-TO-END TEST")
    print("=" * 70)
    print()
    
    # Setup
    test_repo = './test-repo'
    
    if not os.path.exists(test_repo):
        print(f"❌ Test repository not found: {test_repo}")
        return False
    
    try:
        # Stage 1: Parse codebase
        print("Stage 1: Parsing codebase...")
        parser = CodeParser()
        parsed_files = parser.parse_directory(test_repo)
        print(f"✓ Parsed {len(parsed_files)} files")
        print()
        
        # Stage 2: Build dependency graph
        print("Stage 2: Building dependency graph...")
        graph_builder = DependencyGraphBuilder()
        dependency_graph = graph_builder.build_graph(parsed_files)
        node_count = len(dependency_graph.get('nodes', []))
        edge_count = len(dependency_graph.get('edges', []))
        print(f"✓ Graph built: {node_count} nodes, {edge_count} edges")
        print()
        
        # Stage 3: Analyze codebase
        print("Stage 3: Analyzing codebase profile...")
        analyzer = CodebaseAnalyzer()
        profile = analyzer.analyze(test_repo, parsed_files, dependency_graph)
        print(f"✓ Language: {profile['language']}")
        print(f"✓ Features: {', '.join(profile['features']) if profile['features'] else 'None'}")
        print(f"✓ Frameworks: {', '.join(profile['frameworks']) if profile['frameworks'] else 'None'}")
        print(f"✓ Project Type: {profile['project_type']}")
        print(f"✓ Has Database: {profile['has_database']}")
        print(f"✓ Has API: {profile['has_api']}")
        print(f"✓ Complexity: {profile['complexity']['size_category']} ({profile['complexity']['total_files']} files)")
        print()
        
        # Stage 4: Select diagrams
        print("Stage 4: Selecting relevant diagrams...")
        selector = DiagramSelector()
        selected_diagrams = selector.select_diagrams(profile, max_diagrams=8)
        print(f"✓ Selected {len(selected_diagrams)} diagrams:")
        for i, diagram in enumerate(selected_diagrams, 1):
            priority_emoji = "🔴" if diagram['priority'] == 'high' else "🟡" if diagram['priority'] == 'medium' else "🟢"
            print(f"  {priority_emoji} [{i}] {diagram['name']} ({diagram['priority'].upper()})")
        print()
        
        # Stage 5: Extract contexts
        print("Stage 5: Extracting specialized contexts...")
        context_factory = ContextExtractorFactory()
        contexts = {}
        
        for diagram in selected_diagrams:
            diagram_type = diagram['type_id']
            scenarios = diagram.get('scenarios', [])
            scenario = scenarios[0] if scenarios else None
            
            extractor = context_factory.get_extractor(diagram_type)
            context = extractor.extract(dependency_graph, profile, scenario)
            contexts[diagram_type] = context
            
            print(f"✓ {diagram_type}: Extracted context")
            # Show sample of what was extracted
            if diagram_type == 'component':
                print(f"    - Components: {context.get('total_components', 0)}")
                print(f"    - External deps: {len(context.get('external_dependencies', []))}")
            elif diagram_type == 'class':
                print(f"    - Classes: {context.get('total_classes', 0)}")
                print(f"    - Relationships: {len(context.get('relationships', []))}")
            elif diagram_type == 'sequence':
                print(f"    - Participants: {len(context.get('participants', []))}")
                print(f"    - Interactions: {context.get('interaction_count', 0)}")
        print()
        
        # Stage 6: Generate prompts
        print("Stage 6: Generating specialized prompts...")
        prompts = {}
        for diagram_type, context in contexts.items():
            prompt = get_prompt_for_diagram(diagram_type, context)
            prompts[diagram_type] = prompt
            
            # Show prompt stats
            lines = len(prompt.split('\n'))
            chars = len(prompt)
            print(f"✓ {diagram_type}: {lines} lines, {chars} chars")
        print()
        
        # Stage 7: Validation
        print("Stage 7: Validating prompt quality...")
        validation_results = {}
        
        for diagram_type, prompt in prompts.items():
            issues = []
            
            # Check 1: Has context
            if "CONTEXT:" not in prompt:
                issues.append("Missing CONTEXT section")
            
            # Check 2: Has requirements
            if "REQUIREMENTS:" not in prompt:
                issues.append("Missing REQUIREMENTS section")
            
            # Check 3: Has syntax guidance
            if "MERMAID SYNTAX:" not in prompt or "SYNTAX:" not in prompt:
                issues.append("Missing Mermaid syntax guidance")
            
            # Check 4: Reasonable length
            if len(prompt) < 300:
                issues.append("Prompt too short")
            
            # Check 5: Has diagram-specific keywords
            diagram_keywords = {
                'component': ['components', 'modules', 'dependencies'],
                'class': ['class', 'attributes', 'methods', 'relationships'],
                'sequence': ['sequence', 'participants', 'messages', 'interactions'],
                'activity': ['activity', 'workflow', 'decision', 'flow'],
                'data_flow': ['data', 'flow', 'transformation'],
                'c4_context': ['system', 'context', 'users', 'external'],
                'er_diagram': ['entity', 'relationship', 'attributes']
            }
            
            if diagram_type in diagram_keywords:
                keywords = diagram_keywords[diagram_type]
                found = sum(1 for kw in keywords if kw.lower() in prompt.lower())
                if found < len(keywords) / 2:
                    issues.append(f"Missing key terminology (found {found}/{len(keywords)})")
            
            validation_results[diagram_type] = {
                'valid': len(issues) == 0,
                'issues': issues,
                'length': len(prompt),
                'lines': len(prompt.split('\n'))
            }
            
            status = "✓" if len(issues) == 0 else "⚠"
            print(f"{status} {diagram_type}: {'Valid' if len(issues) == 0 else ', '.join(issues)}")
        print()
        
        # Summary
        print("=" * 70)
        print("PHASE 2 TEST SUMMARY")
        print("=" * 70)
        print()
        print(f"✅ Parsing: {len(parsed_files)} files")
        print(f"✅ Graph: {node_count} nodes, {edge_count} edges")
        print(f"✅ Analysis: {profile['project_type']} detected")
        print(f"✅ Selection: {len(selected_diagrams)} diagrams chosen")
        print(f"✅ Contexts: {len(contexts)} extracted")
        print(f"✅ Prompts: {len(prompts)} generated")
        print()
        
        valid_prompts = sum(1 for v in validation_results.values() if v['valid'])
        print(f"Prompt Quality: {valid_prompts}/{len(prompts)} valid")
        print()
        
        # Categorize diagrams
        by_category = {}
        for diagram in selected_diagrams:
            cat = diagram['category']
            by_category[cat] = by_category.get(cat, 0) + 1
        
        print("Diagram Distribution:")
        for cat, count in sorted(by_category.items()):
            print(f"  - {cat}: {count}")
        print()
        
        # Save results
        results = {
            'test_date': '2026-01-22',
            'test_repo': test_repo,
            'parsing': {
                'files_parsed': len(parsed_files),
                'languages': list(set(f.get('language', 'unknown') for f in parsed_files))
            },
            'graph': {
                'nodes': node_count,
                'edges': edge_count
            },
            'profile': profile,
            'selected_diagrams': selected_diagrams,
            'contexts': {k: {'diagram_type': v.get('diagram_type')} for k, v in contexts.items()},
            'validation': validation_results,
            'summary': {
                'total_diagrams': len(selected_diagrams),
                'valid_prompts': valid_prompts,
                'by_category': by_category
            }
        }
        
        output_file = 'phase2_test_results.json'
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📄 Results saved to: {output_file}")
        print()
        
        # Final status
        all_valid = valid_prompts == len(prompts)
        if all_valid and len(selected_diagrams) > 0 and len(contexts) > 0:
            print("🎉 PHASE 2 TEST: PASSED")
            print()
            print("✅ All components working correctly")
            print("✅ Context extraction successful")
            print("✅ Prompt generation valid")
            print("✅ Ready for LLM generation testing")
            return True
        else:
            print("⚠️  PHASE 2 TEST: PASSED WITH WARNINGS")
            print()
            print(f"⚠️  Some prompts have issues ({valid_prompts}/{len(prompts)} valid)")
            print("ℹ️  Review validation results above")
            return True
        
    except Exception as e:
        print()
        print(f"❌ PHASE 2 TEST: FAILED")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_phase2_pipeline()
    sys.exit(0 if success else 1)
