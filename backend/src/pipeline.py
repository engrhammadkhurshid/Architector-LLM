"""
Complete pipeline orchestrator for documentation generation with quality validation
Coordinates: Parsing -> Analysis -> Selection -> Multi-Diagram Generation -> Validation -> Output
"""

import os
import time
import logging
from typing import Dict, Any
from parser.ast_parser import CodeParser
from parser.dependency_graph import DependencyGraphBuilder
from llm.client import LLMClient, OllamaClient
from llm.prompt_curator import PromptCurator
from diagram.renderer import DiagramRenderer
from output.organizer import OutputOrganizer
from analyzer.codebase_analyzer import CodebaseAnalyzer
from analyzer.version_detector import VersionDetector
from diagram.diagram_selector import DiagramSelector
from diagram.multi_diagram_generator import MultiDiagramGenerator, LLMServiceAdapter
from diagram.relationship_mapper import RelationshipMapper
from validation.diagram_validator import DiagramValidator
from validation.quality_report import QualityReportGenerator
from output.interactive_docs import InteractiveDocGenerator

logger = logging.getLogger(__name__)

class DocumentationPipeline:
    """
    Complete pipeline for generating architecture documentation with quality validation
    """
    
    def __init__(self):
        self.parser = CodeParser()
        self.graph_builder = DependencyGraphBuilder()
        self.version_detector = VersionDetector()
        
        # Select LLM client based on environment variable
        llm_provider = os.getenv('LLM_PROVIDER', 'ollama').lower()
        if llm_provider == 'ollama':
            self.llm_client = OllamaClient()
            logger.info('Using Ollama local LLM')
        else:
            self.llm_client = LLMClient()
            logger.info('Using DeepSeek API')
        
        self.prompt_curator = PromptCurator()
        self.diagram_renderer = DiagramRenderer()
        self.output_organizer = OutputOrganizer()
        
        # Multi-diagram system components
        self.codebase_analyzer = CodebaseAnalyzer()
        self.diagram_selector = DiagramSelector()
        llm_adapter = LLMServiceAdapter(self.llm_client)
        self.multi_diagram_generator = MultiDiagramGenerator(llm_adapter, max_parallel=3)
        
        # Quality validation components
        self.diagram_validator = DiagramValidator()
        self.quality_report_generator = QualityReportGenerator()
        
        # Phase 3 components
        self.relationship_mapper = RelationshipMapper()
        self.interactive_doc_generator = InteractiveDocGenerator()
        
        logger.info('Documentation pipeline initialized with Phase 3: Quality validation, relationships, and interactive docs')
    
    def generate(self, codebase_path: str, semantic_version: str = None) -> Dict[str, Any]:
        """
        Execute the complete documentation generation pipeline
        
        Args:
            codebase_path: Path to the codebase to analyze
            semantic_version: Semantic version for output directory (optional, auto-detected if None)
            
        Returns:
            Results dictionary with output paths and metrics
        """
        start_time = time.time()
        logger.info(f'Starting documentation generation for: {codebase_path}')
        
        try:
            # Auto-detect version if not provided
            if not semantic_version:
                logger.info('Auto-detecting project version...')
                version_info = self.version_detector.detect(codebase_path)
                if version_info['version']:
                    semantic_version = version_info['version']
                    logger.info(f'Detected version {semantic_version} from {version_info["source"]} ({version_info["language"]})')
                else:
                    semantic_version = '1.0.0'
                    logger.warning('No version detected, using default: 1.0.0')
            else:
                logger.info(f'Using provided version: {semantic_version}')
            
            # Stage 1: Parse codebase
            logger.info('Stage 1: Parsing codebase...')
            parsed_files = self.parser.parse_directory(codebase_path)
            
            if not parsed_files:
                raise ValueError('No source files found in codebase')
            
            logger.info(f'Parsed {len(parsed_files)} files')
            
            # Stage 2: Build dependency graph
            logger.info('Stage 2: Building dependency graph...')
            dependency_graph = self.graph_builder.build_graph(parsed_files)
            logger.info(f'Graph: {dependency_graph["metadata"]["total_nodes"]} nodes, {dependency_graph["metadata"]["total_edges"]} edges')
            
            # Stage 3: Analyze codebase profile
            logger.info('Stage 3: Analyzing codebase characteristics...')
            codebase_profile = self.codebase_analyzer.analyze(
                codebase_path,
                parsed_files,
                dependency_graph
            )
            logger.info(f'Codebase: {codebase_profile["project_type"]} with {codebase_profile["language"]}')
            
            # Stage 4: Select relevant diagrams
            logger.info('Stage 4: Selecting relevant diagram types...')
            selected_diagrams = self.diagram_selector.select_diagrams(
                codebase_profile,
                max_diagrams=8
            )
            logger.info(f'Selected {len(selected_diagrams)} diagrams: {[d["type_id"] for d in selected_diagrams]}')
            
            # Stage 5: Generate multiple specialized diagrams
            logger.info('Stage 5: Generating specialized diagrams...')
            diagram_results = self.multi_diagram_generator.generate_all_diagrams(
                selected_diagrams,
                dependency_graph,
                codebase_profile,
                output_callback=logger.info
            )
            
            generation_summary = self.multi_diagram_generator.generate_summary_report(diagram_results)
            logger.info(f'Generated {generation_summary["successful"]}/{generation_summary["total_diagrams"]} diagrams')
            
            # Stage 6: Validate diagram quality
            logger.info('Stage 6: Validating diagram quality...')
            validation_results = self.diagram_validator.validate_all(diagram_results)
            
            avg_quality = sum(v.get('overall_score', 0) for v in validation_results.values()) / len(validation_results) if validation_results else 0
            logger.info(f'Average quality score: {avg_quality:.1f}/100')
            
            # Stage 7: Generate quality report
            logger.info('Stage 7: Generating quality report...')
            quality_report = self.quality_report_generator.generate(
                validation_results,
                diagram_results,
                {'generated_at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'semantic_version': semantic_version}
            )
            
            # Stage 7.5: Map cross-diagram relationships
            logger.info('Stage 7.5: Mapping cross-diagram relationships...')
            relationship_map = self.relationship_mapper.map_relationships(
                diagram_results,
                dependency_graph
            )
            relationship_report = self.relationship_mapper.generate_relationship_report(relationship_map)
            logger.info(f'Found {len(relationship_map["shared_entities"])} shared entities across diagrams')
            
            # Stage 8: Generate README documentation
            logger.info('Stage 8: Generating README documentation...')
            readme_content = self._generate_readme_with_diagrams(
                codebase_profile,
                selected_diagrams,
                diagram_results,
                validation_results
            )
            
            # Stage 8.5: Generate interactive documentation
            logger.info('Stage 8.5: Generating interactive documentation...')
            enhanced_index = self.interactive_doc_generator.generate_enhanced_index(
                diagram_results,
                validation_results,
                relationship_map,
                {'generated_at': time.strftime('%Y-%m-%dT%H:%M:%S'), 'semantic_version': semantic_version, 'codebase_path': codebase_path}
            )
            comparison_view = self.interactive_doc_generator.generate_comparison_view(
                diagram_results,
                relationship_map
            )
            
            # Stage 9: Create output directory
            logger.info('Stage 9: Creating output directory...')
            output_dir = self.output_organizer.create_output_directory(
                codebase_path,
                semantic_version
            )
            
            # Stage 10: Save all outputs (multiple diagrams with rendering + quality report)
            logger.info('Stage 10: Saving outputs and rendering diagrams...')
            processing_time = time.time() - start_time
            
            metadata = {
                'generated_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'processing_time': round(processing_time, 2),
                'files_analyzed': len(parsed_files),
                'total_classes': dependency_graph['metadata']['total_classes'],
                'total_functions': dependency_graph['metadata']['total_functions'],
                'llm_model': 'deepseek-coder',
                'semantic_version': semantic_version,
                'codebase_path': codebase_path,
                'git_hash': self.output_organizer._get_git_hash(codebase_path),
                'codebase_profile': codebase_profile,
                'diagrams_generated': generation_summary['total_diagrams'],
                'diagrams_successful': generation_summary['successful'],
                'diagram_types': generation_summary['diagram_types'],
                'average_quality_score': avg_quality,
                'validation_results': validation_results,
                'shared_entities': len(relationship_map['shared_entities']),
                'diagram_connections': len(relationship_map['diagram_connections'])
            }
            
            saved_files = self.output_organizer.save_multi_diagram_documentation(
                output_dir,
                readme_content,
                diagram_results,
                metadata,
                diagram_renderer=self.diagram_renderer,
                quality_report=quality_report,
                relationship_report=relationship_report,
                enhanced_index=enhanced_index,
                comparison_view=comparison_view
            )
            
            logger.info(f'Documentation generation complete in {processing_time:.2f}s')
            
            return {
                'status': 'success',
                'output_dir': output_dir,
                'saved_files': saved_files,
                'metrics': metadata
            }
            
        except Exception as e:
            logger.error(f'Pipeline failed: {str(e)}', exc_info=True)
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def _generate_readme_with_diagrams(
        self,
        profile: Dict,
        selected_diagrams: list,
        diagram_results: Dict,
        validation_results: Dict = None
    ) -> str:
        """
        Generate comprehensive README with multi-diagram gallery and quality scores.
        
        Args:
            profile: Codebase profile
            selected_diagrams: List of selected diagram metadata
            diagram_results: Generated diagram results
            validation_results: Quality validation results (optional)
            
        Returns:
            README markdown content
        """
        readme = f"""# Architecture Documentation

## Project Overview

**Type:** {profile['project_type'].replace('_', ' ').title()}  
**Primary Language:** {profile['language'].title()}  
**Complexity:** {profile['complexity']['size_category'].title()} ({profile['complexity']['total_files']} files)

### Detected Features
{self._format_features(profile)}

### Frameworks & Technologies
{self._format_frameworks(profile)}

---

## Architecture Diagrams

This documentation includes {len([r for r in diagram_results.values() if r.get('success')])} specialized architecture diagrams to provide comprehensive system understanding.

"""
        
        # Group diagrams by category
        by_category = {}
        for diagram in selected_diagrams:
            category = diagram.get('category', 'Other')
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(diagram)
        
        # Add diagrams by category
        for category, diagrams in by_category.items():
            readme += f"\n### {category} Diagrams\n\n"
            
            for diagram in diagrams:
                type_id = diagram['type_id']
                result = diagram_results.get(type_id, {})
                
                if result.get('success'):
                    readme += f"#### {diagram['name']}\n\n"
                    readme += f"**Priority:** {diagram['priority'].upper()}  \n"
                    readme += f"**Purpose:** {diagram.get('reason', 'N/A')}  \n"
                    
                    # Add quality score if available
                    if validation_results and type_id in validation_results:
                        val = validation_results[type_id]
                        quality = val.get('overall_score', 0)
                        emoji = "✅" if quality >= 85 else "⚠️" if quality >= 70 else "❌"
                        readme += f"**Quality:** {quality:.0f}/100 {emoji}  \n"
                    
                    readme += f"\n![{diagram['name']}](diagrams/{type_id}.png)\n\n"
                    readme += f"[View Source](diagrams/{type_id}.mmd) | [View SVG](diagrams/{type_id}.svg)\n\n"
                    readme += "---\n\n"
        
        readme += """
## Documentation Index

- [Component Diagrams](docs/structural-diagrams.md) - System structure and modules
- [Behavioral Diagrams](docs/behavioral-diagrams.md) - Interactions and workflows  
- [Data Architecture](docs/data-diagrams.md) - Data flow and storage
- [Quality Report](QUALITY_REPORT.md) - Diagram quality assessment
- [Full Index](INDEX.md) - Complete navigation guide

---

*Generated by Architector-LLM - Multi-Diagram Architecture Documentation System*
"""
        
        return readme
    
    def _format_features(self, profile: Dict) -> str:
        """Format detected features as markdown list."""
        features = profile.get('features', [])
        if not features:
            return "- None detected\n"
        
        feature_labels = {
            'oop': 'Object-Oriented Programming',
            'async': 'Asynchronous Programming',
            'type_hints': 'Type Annotations',
            'decorators': 'Decorators',
            'context_managers': 'Context Managers'
        }
        
        return '\n'.join([f"- {feature_labels.get(f, f.title())}" for f in features])
    
    def _format_frameworks(self, profile: Dict) -> str:
        """Format detected frameworks as markdown list."""
        frameworks = profile.get('frameworks', [])
        if not frameworks:
            return "- None detected\n"
        
        return '\n'.join([f"- {fw}" for fw in frameworks])
