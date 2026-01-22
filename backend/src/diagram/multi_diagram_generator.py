"""
Multi-diagram generator orchestrator.
Coordinates the generation of multiple specialized diagrams.
"""

from typing import Dict, List, Any
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

from diagram.context_extractors import ContextExtractorFactory
from llm.prompts.diagram_prompts import get_prompt_for_diagram


class MultiDiagramGenerator:
    """Orchestrates generation of multiple specialized diagrams."""
    
    def __init__(self, llm_service, max_parallel: int = 3):
        """
        Initialize multi-diagram generator.
        
        Args:
            llm_service: LLM service for generating diagrams
            max_parallel: Maximum parallel diagram generations
        """
        self.llm_service = llm_service
        self.max_parallel = max_parallel
        self.context_factory = ContextExtractorFactory()
    
    def generate_all_diagrams(
        self,
        selected_diagrams: List[Dict],
        graph: Dict,
        profile: Dict,
        output_callback=None
    ) -> Dict[str, Any]:
        """
        Generate all selected diagrams.
        
        Args:
            selected_diagrams: List of diagrams from DiagramSelector
            graph: Dependency graph from GraphBuilder
            profile: CodebaseProfile from CodebaseAnalyzer
            output_callback: Optional callback for progress updates
            
        Returns:
            Dictionary mapping diagram_type to generation result
        """
        results = {}
        total = len(selected_diagrams)
        
        if output_callback:
            output_callback(f"🎨 Generating {total} specialized diagrams...")
        
        # Step 1: Extract context for all diagrams
        if output_callback:
            output_callback("📊 Step 1/3: Extracting specialized context...")
        
        contexts = self._extract_all_contexts(selected_diagrams, graph, profile)
        
        # Step 2: Generate diagrams (can be parallelized)
        if output_callback:
            output_callback("🤖 Step 2/3: Generating Mermaid diagrams with LLM...")
        
        results = self._generate_diagrams_parallel(
            selected_diagrams,
            contexts,
            output_callback
        )
        
        # Step 3: Validate results
        if output_callback:
            output_callback("✅ Step 3/3: Validating diagram quality...")
        
        validated_results = self._validate_results(results)
        
        if output_callback:
            success_count = sum(1 for r in validated_results.values() if r.get('success'))
            output_callback(f"✨ Successfully generated {success_count}/{total} diagrams")
        
        return validated_results
    
    def _extract_all_contexts(
        self,
        selected_diagrams: List[Dict],
        graph: Dict,
        profile: Dict
    ) -> Dict[str, Dict]:
        """Extract context for all selected diagrams."""
        contexts = {}
        
        for diagram in selected_diagrams:
            diagram_type = diagram.get('type_id', '')
            scenarios = diagram.get('scenarios', [])
            scenario = scenarios[0] if scenarios else None
            
            try:
                extractor = self.context_factory.get_extractor(diagram_type)
                context = extractor.extract(graph, profile, scenario)
                contexts[diagram_type] = context
            except Exception as e:
                print(f"Warning: Failed to extract context for {diagram_type}: {e}")
                contexts[diagram_type] = self._get_fallback_context(diagram_type, profile)
        
        return contexts
    
    def _generate_diagrams_parallel(
        self,
        selected_diagrams: List[Dict],
        contexts: Dict[str, Dict],
        output_callback=None
    ) -> Dict[str, Any]:
        """Generate diagrams in parallel (respecting max_parallel limit)."""
        results = {}
        
        # Group diagrams into batches
        batches = self._create_batches(selected_diagrams, self.max_parallel)
        
        for batch_idx, batch in enumerate(batches):
            if output_callback:
                output_callback(f"   Batch {batch_idx + 1}/{len(batches)}: Generating {len(batch)} diagrams...")
            
            # Generate batch in parallel using ThreadPoolExecutor
            with ThreadPoolExecutor(max_workers=len(batch)) as executor:
                futures = {}
                
                for diagram in batch:
                    diagram_type = diagram.get('type_id', '')
                    context = contexts.get(diagram_type, {})
                    
                    future = executor.submit(
                        self._generate_single_diagram,
                        diagram_type,
                        context,
                        diagram
                    )
                    futures[future] = diagram_type
                
                # Collect results
                for future in futures:
                    diagram_type = futures[future]
                    try:
                        result = future.result(timeout=120)  # 2 minute timeout per diagram
                        results[diagram_type] = result
                        
                        if output_callback:
                            status = "✓" if result.get('success') else "✗"
                            output_callback(f"   {status} {diagram_type.replace('_', ' ').title()}")
                    except Exception as e:
                        print(f"Error generating {diagram_type}: {e}")
                        results[diagram_type] = {
                            'success': False,
                            'error': str(e),
                            'diagram_type': diagram_type
                        }
        
        return results
    
    def _generate_single_diagram(
        self,
        diagram_type: str,
        context: Dict,
        diagram_info: Dict
    ) -> Dict[str, Any]:
        """Generate a single diagram using LLM."""
        try:
            # Get specialized prompt
            prompt = get_prompt_for_diagram(diagram_type, context)
            
            # Generate with LLM
            mermaid_code = self.llm_service.generate_diagram(
                prompt=prompt,
                diagram_type=diagram_type
            )
            
            # Basic validation
            if not mermaid_code or len(mermaid_code) < 20:
                raise ValueError("Generated diagram is too short or empty")
            
            return {
                'success': True,
                'diagram_type': diagram_type,
                'mermaid_code': mermaid_code,
                'context': context,
                'priority': diagram_info.get('priority', 'medium'),
                'reason': diagram_info.get('reason', ''),
                'metadata': {
                    'type_id': diagram_type,
                    'category': diagram_info.get('category', 'unknown'),
                    'complexity': self._estimate_complexity(mermaid_code),
                    'node_count': self._count_nodes(mermaid_code)
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'diagram_type': diagram_type,
                'error': str(e),
                'context': context
            }
    
    def _create_batches(self, items: List, batch_size: int) -> List[List]:
        """Split items into batches."""
        batches = []
        for i in range(0, len(items), batch_size):
            batches.append(items[i:i + batch_size])
        return batches
    
    def _validate_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Validate generated diagrams."""
        validated = {}
        
        for diagram_type, result in results.items():
            if not result.get('success'):
                validated[diagram_type] = result
                continue
            
            mermaid_code = result.get('mermaid_code', '')
            
            # Validation checks
            validation_errors = []
            
            # Check 1: Has valid Mermaid syntax start
            valid_starts = [
                'graph ', 'flowchart ', 'sequenceDiagram', 'classDiagram',
                'stateDiagram', 'erDiagram', 'journey', 'gantt'
            ]
            if not any(mermaid_code.strip().startswith(start) for start in valid_starts):
                validation_errors.append("Missing valid Mermaid diagram type declaration")
            
            # Check 2: Has reasonable length
            if len(mermaid_code) < 50:
                validation_errors.append("Diagram content too short")
            
            # Check 3: Has at least some nodes/elements
            if '-->' not in mermaid_code and ':' not in mermaid_code:
                validation_errors.append("No relationships or elements detected")
            
            # Add validation info
            result['validation'] = {
                'is_valid': len(validation_errors) == 0,
                'errors': validation_errors,
                'warnings': []
            }
            
            # Add quality score
            result['quality_score'] = self._calculate_quality_score(result)
            
            validated[diagram_type] = result
        
        return validated
    
    def _calculate_quality_score(self, result: Dict) -> float:
        """Calculate quality score for generated diagram (0-100)."""
        if not result.get('success'):
            return 0.0
        
        score = 100.0
        
        # Deduct for validation errors
        errors = result.get('validation', {}).get('errors', [])
        score -= len(errors) * 20
        
        # Check metadata
        metadata = result.get('metadata', {})
        node_count = metadata.get('node_count', 0)
        
        # Optimal node count: 5-15
        if node_count < 3:
            score -= 20  # Too simple
        elif node_count > 20:
            score -= 10  # Too complex
        
        # Check for empty or trivial content
        mermaid_code = result.get('mermaid_code', '')
        if len(mermaid_code) < 100:
            score -= 15
        
        return max(0.0, min(100.0, score))
    
    def _estimate_complexity(self, mermaid_code: str) -> str:
        """Estimate diagram complexity."""
        lines = len(mermaid_code.split('\n'))
        
        if lines < 10:
            return 'simple'
        elif lines < 25:
            return 'moderate'
        else:
            return 'complex'
    
    def _count_nodes(self, mermaid_code: str) -> int:
        """Count approximate number of nodes in diagram."""
        # Simple heuristic: count lines with node definitions
        node_indicators = ['[', '(', '{', '[[', '((', '{{', '[(', '[/', '>']
        count = 0
        
        for line in mermaid_code.split('\n'):
            line = line.strip()
            if any(indicator in line for indicator in node_indicators):
                count += 1
        
        return count
    
    def _get_fallback_context(self, diagram_type: str, profile: Dict) -> Dict:
        """Get fallback context if extraction fails."""
        return {
            'diagram_type': diagram_type,
            'project_type': profile.get('project_type', 'unknown'),
            'language': profile.get('language', 'unknown'),
            'fallback': True
        }
    
    def generate_summary_report(self, results: Dict[str, Any]) -> Dict:
        """Generate summary report of generation process."""
        total = len(results)
        successful = sum(1 for r in results.values() if r.get('success'))
        failed = total - successful
        
        # Group by priority
        by_priority = {'high': 0, 'medium': 0, 'low': 0}
        for result in results.values():
            priority = result.get('priority', 'medium')
            by_priority[priority] = by_priority.get(priority, 0) + 1
        
        # Group by category
        by_category = {}
        for result in results.values():
            category = result.get('metadata', {}).get('category', 'unknown')
            by_category[category] = by_category.get(category, 0) + 1
        
        # Calculate average quality
        quality_scores = [r.get('quality_score', 0) for r in results.values() if r.get('success')]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        return {
            'total_diagrams': total,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0,
            'by_priority': by_priority,
            'by_category': by_category,
            'average_quality_score': round(avg_quality, 2),
            'diagram_types': list(results.keys())
        }


class LLMServiceAdapter:
    """Adapter for existing LLM service to work with multi-diagram generator."""
    
    def __init__(self, ollama_service):
        """Initialize with existing Ollama service."""
        self.ollama_service = ollama_service
    
    def generate_diagram(self, prompt: str, diagram_type: str) -> str:
        """
        Generate diagram using LLM.
        
        Args:
            prompt: Formatted prompt with context
            diagram_type: Type of diagram being generated
            
        Returns:
            Mermaid code string
        """
        try:
            # Call Ollama service with the correct method name
            response = self.ollama_service.generate(
                prompt=prompt,
                system_prompt="You are an expert at generating Mermaid diagrams. Return ONLY the Mermaid code, no explanation, no markdown code blocks."
            )
            
            # Check if generation was successful
            if response.get('status') != 'success':
                raise Exception(f"LLM generation failed: {response.get('message', 'Unknown error')}")
            
            # Extract content from response
            content = response.get('content', '')
            if not content:
                raise Exception("LLM returned empty content")
            
            # Extract Mermaid code (remove markdown code blocks if present)
            mermaid_code = self._extract_mermaid_code(content)
            
            return mermaid_code
            
        except Exception as e:
            raise Exception(f"LLM generation failed: {e}")
    
    def _extract_mermaid_code(self, response: str) -> str:
        """Extract Mermaid code from LLM response."""
        # Remove markdown code blocks
        if '```mermaid' in response:
            start = response.find('```mermaid') + len('```mermaid')
            end = response.find('```', start)
            if end > start:
                return response[start:end].strip()
        
        if '```' in response:
            start = response.find('```') + 3
            end = response.find('```', start)
            if end > start:
                return response[start:end].strip()
        
        # Return as-is if no code blocks
        return response.strip()
