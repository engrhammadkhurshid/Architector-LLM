"""
Prompt Curator for RAG-based Documentation Generation
Constructs structured prompts by injecting code metadata
"""

import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PromptCurator:
    """
    Curates prompts for LLM by combining system instructions with RAG context
    """
    
    SYSTEM_PROMPT = """You are an expert software architect analyzing a codebase to generate professional architecture documentation.

Your task is to:
1. Analyze the provided codebase structure and dependency graph
2. Generate comprehensive architecture documentation in Markdown format
3. Create Mermaid diagram code for visualizing the architecture (C4 Model or UML)

The documentation should include:
- System Overview
- Architecture Patterns Used
- Component Descriptions
- Key Design Decisions
- Dependency Analysis
- Deployment Considerations

The Mermaid diagrams should show:
- High-level system architecture
- Component relationships
- Data flow
- Key interactions

Be precise, professional, and focus on architectural insights rather than implementation details."""
    
    def __init__(self):
        self.system_prompt = self.SYSTEM_PROMPT
    
    def curate_prompt(self, dependency_graph: Dict[str, Any], codebase_path: str) -> str:
        """
        Construct the final prompt by injecting RAG context
        
        Args:
            dependency_graph: The structured dependency graph from DependencyGraphBuilder
            codebase_path: Path to the codebase being analyzed
            
        Returns:
            The complete prompt ready for LLM
        """
        logger.info('Curating prompt with RAG context')
        
        # Extract metadata
        metadata = dependency_graph.get('metadata', {})
        nodes = dependency_graph.get('nodes', [])
        edges = dependency_graph.get('edges', [])
        
        # Build the context section
        context = f"""
## Codebase Context

**Project Path:** `{codebase_path}`

**Statistics:**
- Total Files: {metadata.get('total_files', 0)}
- Total Classes: {metadata.get('total_classes', 0)}
- Total Functions: {metadata.get('total_functions', 0)}

**Dependency Graph:**

### Nodes (Components)
{self._format_nodes(nodes[:50])}  
{f"... and {len(nodes) - 50} more nodes" if len(nodes) > 50 else ""}

### Edges (Dependencies)
{self._format_edges(edges[:50])}
{f"... and {len(edges) - 50} more edges" if len(edges) > 50 else ""}

---

Based on the above codebase context, generate:

1. **Architecture Documentation (Markdown)**
   - Use proper heading structure (##, ###)
   - Include all sections mentioned in the system prompt
   - Be comprehensive but concise

2. **Mermaid Diagram Code**
   - Wrap in ```mermaid code blocks
   - Use appropriate diagram type (graph, flowchart, C4, etc.)
   - Show key components and their relationships
   - Keep it clean and readable

Please provide both outputs in a single response, separated clearly.
"""
        
        return context
    
    def _format_nodes(self, nodes: list) -> str:
        """Format nodes for the prompt"""
        if not nodes:
            return "No nodes found"
        
        formatted = []
        for node in nodes:
            formatted.append(
                f"  - [{node['type']}] {node['name']} (in {node['file']})"
            )
        return '\n'.join(formatted)
    
    def _format_edges(self, edges: list) -> str:
        """Format edges for the prompt"""
        if not edges:
            return "No edges found"
        
        formatted = []
        for edge in edges:
            formatted.append(
                f"  - {edge['from']} --[{edge['type']}]--> {edge['to']}"
            )
        return '\n'.join(formatted)
    
    def get_system_prompt(self) -> str:
        """Get the system prompt"""
        return self.system_prompt
