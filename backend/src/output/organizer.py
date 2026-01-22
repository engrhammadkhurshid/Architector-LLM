"""
Output Organizer
Manages versioned output directories and artifact organization
"""

import os
import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class OutputOrganizer:
    """
    Organizes generated documentation into versioned directories
    """
    
    def __init__(self, base_output_dir: str = 'docs/arch'):
        self.base_output_dir = base_output_dir
    
    def create_output_directory(
        self,
        codebase_path: str,
        semantic_version: str = '1.0.0'
    ) -> str:
        """
        Create a versioned output directory
        
        Format: docs/arch/v{semantic_version}_{timestamp}_{git_hash}
        Example: docs/arch/v1.0.0_2026-01-21-143022_abc123f
        
        Args:
            codebase_path: Path to the codebase (for git operations)
            semantic_version: Semantic version string (default: 1.0.0)
            
        Returns:
            Path to the created output directory
        """
        timestamp = datetime.now().strftime('%Y-%m-%d-%H%M%S')
        git_hash = self._get_git_hash(codebase_path)
        
        dir_name = f'v{semantic_version}_{timestamp}_{git_hash}'
        output_path = os.path.join(codebase_path, self.base_output_dir, dir_name)
        
        # Create directory structure
        os.makedirs(output_path, exist_ok=True)
        os.makedirs(os.path.join(output_path, 'diagrams'), exist_ok=True)
        os.makedirs(os.path.join(output_path, 'metadata'), exist_ok=True)
        
        logger.info(f'Created output directory: {output_path}')
        return output_path
    
    def save_documentation(
        self,
        output_dir: str,
        markdown_content: str,
        diagram_code: str,
        metadata: Dict[str, Any],
        diagram_renderer=None
    ) -> Dict[str, str]:
        """
        Save all generated artifacts to the output directory
        
        Args:
            output_dir: Path to the output directory
            markdown_content: Generated markdown documentation
            diagram_code: Mermaid diagram source code
            metadata: Generation metadata (metrics, timestamps, etc.)
            diagram_renderer: Optional DiagramRenderer instance for rendering images
            
        Returns:
            Dictionary mapping artifact types to file paths
        """
        logger.info(f'Saving artifacts to {output_dir}')
        
        saved_files = {}
        rendered_diagrams = []
        
        # Save diagram source code first
        diagram_src_path = os.path.join(output_dir, 'diagrams', 'architecture.mmd')
        with open(diagram_src_path, 'w', encoding='utf-8') as f:
            f.write(diagram_code)
        saved_files['diagram_source'] = diagram_src_path
        logger.info(f'Saved diagram source: {diagram_src_path}')
        
        # Render diagram to PNG and SVG if renderer provided
        if diagram_renderer and diagram_renderer.check_dependencies():
            logger.info('Rendering diagrams to PNG and SVG...')
            
            # Render PNG
            png_path = os.path.join(output_dir, 'diagrams', 'architecture.png')
            if diagram_renderer.render(diagram_code, png_path, 'png'):
                saved_files['diagram_png'] = png_path
                rendered_diagrams.append('PNG')
                logger.info(f'Rendered PNG diagram: {png_path}')
            
            # Render SVG
            svg_path = os.path.join(output_dir, 'diagrams', 'architecture.svg')
            if diagram_renderer.render(diagram_code, svg_path, 'svg'):
                saved_files['diagram_svg'] = svg_path
                rendered_diagrams.append('SVG')
                logger.info(f'Rendered SVG diagram: {svg_path}')
            
            # Update metadata
            metadata['diagrams_rendered'] = rendered_diagrams
        else:
            logger.warning('Diagram renderer not available - only source code saved')
            metadata['diagrams_rendered'] = []
        
        # Enhance markdown content with diagram images
        enhanced_markdown = self._enhance_markdown_with_diagrams(
            markdown_content, 
            diagram_code,
            bool(rendered_diagrams)
        )
        
        # Save main documentation
        doc_path = os.path.join(output_dir, 'README.md')
        with open(doc_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_markdown)
        saved_files['documentation'] = doc_path
        logger.info(f'Saved documentation: {doc_path}')
        
        # Save metadata
        metadata_path = os.path.join(output_dir, 'metadata', 'generation_info.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        saved_files['metadata'] = metadata_path
        logger.info(f'Saved metadata: {metadata_path}')
        
        # Create index file
        index_path = os.path.join(output_dir, 'INDEX.md')
        self._create_index_file(index_path, saved_files, metadata)
        saved_files['index'] = index_path
        
        return saved_files
    
    def _enhance_markdown_with_diagrams(
        self,
        markdown_content: str,
        diagram_code: str,
        has_rendered_images: bool
    ) -> str:
        """Enhance markdown content with diagram embeds"""
        # Add architecture diagram section
        diagram_section = "\n\n---\n\n## Architecture Diagram\n\n"
        
        if has_rendered_images:
            diagram_section += "### Visual Diagram\n\n"
            diagram_section += "![Architecture Diagram](diagrams/architecture.png)\n\n"
            diagram_section += "*Click the image to view in full size. SVG version available at [diagrams/architecture.svg](diagrams/architecture.svg)*\n\n"
        
        diagram_section += "### Mermaid Source Code\n\n"
        diagram_section += "```mermaid\n"
        # Extract clean mermaid code
        if '```mermaid' in diagram_code:
            start = diagram_code.find('```mermaid') + 10
            end = diagram_code.find('```', start)
            clean_code = diagram_code[start:end].strip()
        else:
            clean_code = diagram_code.strip()
        diagram_section += clean_code + "\n"
        diagram_section += "```\n\n"
        diagram_section += "*This diagram can be edited and viewed in VS Code, GitHub, or any Mermaid-compatible viewer.*\n\n"
        
        # Insert diagram section after the overview
        return markdown_content + diagram_section
    
    def _get_git_hash(self, codebase_path: str, short: bool = True) -> str:
        """Get the current Git commit hash"""
        try:
            cmd = ['git', 'rev-parse']
            if short:
                cmd.append('--short')
            cmd.append('HEAD')
            
            result = subprocess.run(
                cmd,
                cwd=codebase_path,
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.warning('Not a git repository or git not found')
                return 'nogit'
                
        except Exception as e:
            logger.warning(f'Could not get git hash: {e}')
            return 'nogit'
    
    def _create_index_file(
        self,
        index_path: str,
        saved_files: Dict[str, str],
        metadata: Dict[str, Any]
    ) -> None:
        """Create an index file listing all artifacts"""
        
        # Build diagrams list
        diagram_list = []
        if 'diagram_png' in saved_files:
            diagram_list.append('- 🖼️ [Architecture Diagram (PNG)](diagrams/architecture.png)')
        if 'diagram_svg' in saved_files:
            diagram_list.append('- 🎨 [Architecture Diagram (SVG)](diagrams/architecture.svg)')
        diagram_list.append('- 📝 [Mermaid Source Code](diagrams/architecture.mmd)')
        
        diagrams_section = '\n'.join(diagram_list) if diagram_list else 'No diagrams generated'
        
        content = f"""# Architecture Documentation Index

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Generated Artifacts

### Documentation
- 📄 [Main Documentation](README.md) - Complete architecture overview

### Diagrams
{diagrams_section}

### Metadata
- 📊 [Generation Info](metadata/generation_info.json) - Processing metrics and timestamps

## Generation Statistics

- **Files Analyzed:** {metadata.get('files_analyzed', 'N/A')}
- **Classes Found:** {metadata.get('total_classes', 'N/A')}
- **Functions Found:** {metadata.get('total_functions', 'N/A')}
- **Processing Time:** {metadata.get('processing_time', 'N/A')} seconds
- **LLM Model:** {metadata.get('llm_model', 'N/A')}
- **Git Commit:** {metadata.get('git_hash', 'N/A')}
- **Diagrams Rendered:** {', '.join(metadata.get('diagrams_rendered', [])) or 'Source code only'}

## Quick Start

1. **View Documentation:** Open [README.md](README.md) to see the complete architecture overview
2. **View Diagram:** {'Open [diagrams/architecture.png](diagrams/architecture.png) for the visual diagram' if 'diagram_png' in saved_files else 'View the Mermaid code in [diagrams/architecture.mmd](diagrams/architecture.mmd)'}
3. **Edit Diagram:** Modify [diagrams/architecture.mmd](diagrams/architecture.mmd) in VS Code with Mermaid preview

---

*Generated by Architector-LLM v1.0.0*
"""
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f'Created index file: {index_path}')
    
    def save_multi_diagram_documentation(
        self,
        output_dir: str,
        readme_content: str,
        diagram_results: Dict[str, Any],
        metadata: Dict[str, Any],
        diagram_renderer=None,
        quality_report: str = None,
        relationship_report: str = None,
        enhanced_index: str = None,
        comparison_view: str = None
    ) -> Dict[str, str]:
        """
        Save documentation with multiple diagrams and Phase 3 enhancements.
        
        Args:
            output_dir: Path to output directory
            readme_content: Generated README content
            diagram_results: Dictionary of diagram generation results
            metadata: Generation metadata
            diagram_renderer: Optional DiagramRenderer for rendering images
            quality_report: Quality assessment report (Phase 3.2)
            relationship_report: Cross-diagram relationships report (Phase 3.3)
            enhanced_index: Interactive navigation index (Phase 3.4)
            comparison_view: Side-by-side diagram comparisons (Phase 3.4)
            
        Returns:
            Dictionary mapping artifact types to file paths
        """
        logger.info(f'Saving multi-diagram documentation with Phase 3 enhancements to {output_dir}')
        
        saved_files = {}
        diagrams_dir = os.path.join(output_dir, 'diagrams')
        os.makedirs(diagrams_dir, exist_ok=True)
        
        # Save each diagram
        for diagram_type, result in diagram_results.items():
            if not result.get('success'):
                logger.warning(f'Skipping failed diagram: {diagram_type}')
                continue
            
            mermaid_code = result.get('mermaid_code', '')
            
            # Save Mermaid source
            mmd_path = os.path.join(diagrams_dir, f'{diagram_type}.mmd')
            with open(mmd_path, 'w', encoding='utf-8') as f:
                f.write(mermaid_code)
            saved_files[f'diagram_{diagram_type}_source'] = mmd_path
            logger.info(f'Saved {diagram_type} source: {mmd_path}')
            
            # Render PNG and SVG if renderer available
            if diagram_renderer and diagram_renderer.check_dependencies():
                # Render PNG
                png_path = os.path.join(diagrams_dir, f'{diagram_type}.png')
                if diagram_renderer.render(mermaid_code, png_path, 'png'):
                    saved_files[f'diagram_{diagram_type}_png'] = png_path
                    logger.info(f'Rendered {diagram_type} PNG')
                
                # Render SVG
                svg_path = os.path.join(diagrams_dir, f'{diagram_type}.svg')
                if diagram_renderer.render(mermaid_code, svg_path, 'svg'):
                    saved_files[f'diagram_{diagram_type}_svg'] = svg_path
                    logger.info(f'Rendered {diagram_type} SVG')
        
        # Save README
        readme_path = os.path.join(output_dir, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        saved_files['readme'] = readme_path
        logger.info(f'Saved README: {readme_path}')
        
        # Save quality report if provided
        if quality_report:
            quality_path = os.path.join(output_dir, 'QUALITY_REPORT.md')
            with open(quality_path, 'w', encoding='utf-8') as f:
                f.write(quality_report)
            saved_files['quality_report'] = quality_path
            logger.info(f'Saved quality report: {quality_path}')
        
        # Save relationship report if provided (Phase 3.3)
        if relationship_report:
            relationship_path = os.path.join(output_dir, 'RELATIONSHIPS.md')
            with open(relationship_path, 'w', encoding='utf-8') as f:
                f.write(relationship_report)
            saved_files['relationship_report'] = relationship_path
            logger.info(f'Saved relationship report: {relationship_path}')
        
        # Save comparison view if provided (Phase 3.4)
        if comparison_view:
            comparison_path = os.path.join(output_dir, 'COMPARISONS.md')
            with open(comparison_path, 'w', encoding='utf-8') as f:
                f.write(comparison_view)
            saved_files['comparison_view'] = comparison_path
            logger.info(f'Saved comparison view: {comparison_path}')
        
        # Save metadata
        metadata_path = os.path.join(output_dir, 'metadata', 'generation_info.json')
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        saved_files['metadata'] = metadata_path
        
        # Create category documentation
        self._create_category_docs(output_dir, diagram_results, saved_files)
        
        # Create comprehensive index (use enhanced_index if provided, otherwise create default)
        index_path = os.path.join(output_dir, 'INDEX.md')
        if enhanced_index:
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(enhanced_index)
            logger.info(f'Saved enhanced index: {index_path}')
        else:
            self._create_multi_diagram_index(index_path, diagram_results, metadata)
        saved_files['index'] = index_path
        
        logger.info(f'Saved {len(saved_files)} files')
        return saved_files
    
    def _create_category_docs(
        self,
        output_dir: str,
        diagram_results: Dict[str, Any],
        saved_files: Dict[str, str]
    ):
        """Create category-specific documentation files."""
        docs_dir = os.path.join(output_dir, 'docs')
        os.makedirs(docs_dir, exist_ok=True)
        
        # Group by category
        categories = {
            'STRUCTURAL': [],
            'BEHAVIORAL': [],
            'ARCHITECTURAL': [],
            'DATA': []
        }
        
        for diagram_type, result in diagram_results.items():
            if result.get('success'):
                category = result.get('metadata', {}).get('category', 'OTHER')
                if category in categories:
                    categories[category].append({
                        'type': diagram_type,
                        'result': result
                    })
        
        # Create structural diagrams doc
        if categories['STRUCTURAL']:
            struct_path = os.path.join(docs_dir, 'structural-diagrams.md')
            self._write_category_doc(struct_path, 'Structural', categories['STRUCTURAL'])
            saved_files['structural_docs'] = struct_path
        
        # Create behavioral diagrams doc
        if categories['BEHAVIORAL']:
            behav_path = os.path.join(docs_dir, 'behavioral-diagrams.md')
            self._write_category_doc(behav_path, 'Behavioral', categories['BEHAVIORAL'])
            saved_files['behavioral_docs'] = behav_path
        
        # Create data diagrams doc
        if categories['DATA']:
            data_path = os.path.join(docs_dir, 'data-diagrams.md')
            self._write_category_doc(data_path, 'Data', categories['DATA'])
            saved_files['data_docs'] = data_path
    
    def _write_category_doc(self, path: str, category: str, diagrams: list):
        """Write category-specific documentation."""
        content = f"""# {category} Diagrams

This document contains all {category.lower()} architecture diagrams for the system.

"""
        for item in diagrams:
            dtype = item['type']
            result = item['result']
            
            content += f"## {dtype.replace('_', ' ').title()}\n\n"
            content += f"![{dtype}](../diagrams/{dtype}.png)\n\n"
            content += f"**Priority:** {result.get('priority', 'N/A').upper()}  \n"
            content += f"**Quality Score:** {result.get('quality_score', 0):.1f}/100  \n\n"
            content += f"[View Source](../diagrams/{dtype}.mmd) | [View SVG](../diagrams/{dtype}.svg)\n\n"
            content += "---\n\n"
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _create_multi_diagram_index(
        self,
        index_path: str,
        diagram_results: Dict[str, Any],
        metadata: Dict[str, Any]
    ):
        """Create comprehensive index for multi-diagram documentation."""
        content = f"""# Architecture Documentation Index

**Generated:** {metadata.get('generated_at', 'Unknown')}  
**Version:** {metadata.get('semantic_version', '1.0.0')}  
**Processing Time:** {metadata.get('processing_time', 0)}s  
**Diagrams Generated:** {metadata.get('diagrams_successful', 0)}/{metadata.get('diagrams_generated', 0)}  
**Average Quality:** {metadata.get('average_quality_score', 0):.1f}/100

## Quick Links

- [Main Documentation](README.md)
- [Generation Metadata](metadata/generation_info.json)

## Diagrams by Category

"""
        # Group by category
        by_category = {}
        for dtype, result in diagram_results.items():
            if result.get('success'):
                category = result.get('metadata', {}).get('category', 'OTHER')
                if category not in by_category:
                    by_category[category] = []
                by_category[category].append((dtype, result))
        
        for category, items in sorted(by_category.items()):
            content += f"### {category}\n\n"
            for dtype, result in items:
                priority = result.get('priority', 'medium')
                quality = result.get('quality_score', 0)
                emoji = '🔴' if priority == 'high' else '🟡' if priority == 'medium' else '🟢'
                content += f"- {emoji} [{dtype.replace('_', ' ').title()}](diagrams/{dtype}.mmd) "
                content += f"(Quality: {quality:.0f}/100)\n"
            content += "\n"
        
        content += """
## Category Documentation

- [Structural Diagrams](docs/structural-diagrams.md) - System components and architecture
- [Behavioral Diagrams](docs/behavioral-diagrams.md) - Interactions and workflows
- [Data Diagrams](docs/data-diagrams.md) - Data models and flows

---

*Generated by Architector-LLM Multi-Diagram System*
"""
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(content)

