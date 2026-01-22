"""
Diagram Type Registry
Defines all supported diagram types and their generation rules
"""

from typing import Dict, Any, List, Callable
import logging

logger = logging.getLogger(__name__)

class DiagramType:
    """Represents a single diagram type with its configuration"""
    
    def __init__(
        self,
        type_id: str,
        name: str,
        category: str,
        mermaid_type: str,
        description: str,
        priority_calculator: Callable,
        required_context: List[str],
        min_complexity: str = 'tiny',
    ):
        self.type_id = type_id
        self.name = name
        self.category = category
        self.mermaid_type = mermaid_type
        self.description = description
        self.priority_calculator = priority_calculator
        self.required_context = required_context
        self.min_complexity = min_complexity
    
    def calculate_priority(self, profile: Dict[str, Any]) -> str:
        """Calculate priority (high/medium/low/skip) based on codebase profile"""
        return self.priority_calculator(profile)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            'type_id': self.type_id,
            'name': self.name,
            'category': self.category,
            'mermaid_type': self.mermaid_type,
            'description': self.description,
            'required_context': self.required_context,
            'min_complexity': self.min_complexity,
        }


class DiagramTypeRegistry:
    """Registry of all supported diagram types"""
    
    def __init__(self):
        self.diagram_types = self._initialize_diagram_types()
    
    def _initialize_diagram_types(self) -> Dict[str, DiagramType]:
        """Initialize all diagram types with their rules"""
        
        return {
            # ===== STRUCTURAL DIAGRAMS =====
            'component': DiagramType(
                type_id='component',
                name='Component Diagram',
                category='structural',
                mermaid_type='graph TD',
                description='High-level system decomposition showing major components and dependencies',
                priority_calculator=lambda p: 'high',  # Always generate
                required_context=['modules', 'dependencies', 'external_systems'],
                min_complexity='tiny',
            ),
            
            'class': DiagramType(
                type_id='class',
                name='Class Diagram',
                category='structural',
                mermaid_type='classDiagram',
                description='Object-oriented structure showing classes, inheritance, and relationships',
                priority_calculator=lambda p: (
                    'high' if 'oop' in p.get('features', []) and p['complexity']['total_classes'] >= 3 else
                    'medium' if 'oop' in p.get('features', []) else
                    'skip'
                ),
                required_context=['classes', 'inheritance', 'relationships'],
                min_complexity='small',
            ),
            
            'package': DiagramType(
                type_id='package',
                name='Package/Module Diagram',
                category='structural',
                mermaid_type='graph LR',
                description='Code organization showing package/module structure and dependencies',
                priority_calculator=lambda p: (
                    'medium' if p['complexity']['total_files'] >= 10 else 'skip'
                ),
                required_context=['packages', 'module_dependencies'],
                min_complexity='medium',
            ),
            
            # ===== BEHAVIORAL DIAGRAMS =====
            'sequence': DiagramType(
                type_id='sequence',
                name='Sequence Diagram',
                category='behavioral',
                mermaid_type='sequenceDiagram',
                description='Key interaction flows showing communication between components',
                priority_calculator=lambda p: (
                    'high' if p.get('has_api', False) or p.get('project_type') in ['web_api', 'web_application'] else
                    'medium' if p['complexity']['total_classes'] >= 5 else
                    'skip'
                ),
                required_context=['interactions', 'function_calls', 'data_flow'],
                min_complexity='small',
            ),
            
            'activity': DiagramType(
                type_id='activity',
                name='Activity Diagram',
                category='behavioral',
                mermaid_type='flowchart TD',
                description='Workflow and business logic visualization',
                priority_calculator=lambda p: (
                    'medium' if p['complexity']['total_functions'] >= 10 else 'low'
                ),
                required_context=['workflows', 'algorithms', 'decision_points'],
                min_complexity='small',
            ),
            
            'state': DiagramType(
                type_id='state',
                name='State Machine Diagram',
                category='behavioral',
                mermaid_type='stateDiagram-v2',
                description='State transitions and stateful component behavior',
                priority_calculator=lambda p: (
                    'medium' if any(fw in p.get('frameworks', []) for fw in ['react', 'vue']) else
                    'low'
                ),
                required_context=['states', 'transitions', 'events'],
                min_complexity='medium',
            ),
            
            # ===== ARCHITECTURAL DIAGRAMS =====
            'c4_context': DiagramType(
                type_id='c4_context',
                name='C4 System Context Diagram',
                category='architectural',
                mermaid_type='C4Context',
                description='System boundaries, users, and external dependencies',
                priority_calculator=lambda p: (
                    'high' if p.get('project_type') in ['web_api', 'web_application', 'microservice'] else
                    'medium'
                ),
                required_context=['system_boundary', 'actors', 'external_systems'],
                min_complexity='small',
            ),
            
            'c4_container': DiagramType(
                type_id='c4_container',
                name='C4 Container Diagram',
                category='architectural',
                mermaid_type='C4Container',
                description='High-level technology architecture (web apps, APIs, databases)',
                priority_calculator=lambda p: (
                    'high' if p.get('has_database', False) and p.get('has_api', False) else
                    'medium' if p.get('has_api', False) else
                    'skip'
                ),
                required_context=['containers', 'technology_stack', 'protocols'],
                min_complexity='medium',
            ),
            
            'deployment': DiagramType(
                type_id='deployment',
                name='Deployment Diagram',
                category='architectural',
                mermaid_type='graph TB',
                description='Infrastructure and deployment configuration',
                priority_calculator=lambda p: (
                    'high' if p.get('has_deployment_configs', False) else 'skip'
                ),
                required_context=['deployment_configs', 'infrastructure', 'networks'],
                min_complexity='medium',
            ),
            
            # ===== DATA DIAGRAMS =====
            'data_flow': DiagramType(
                type_id='data_flow',
                name='Data Flow Diagram',
                category='data',
                mermaid_type='flowchart LR',
                description='Data movement and transformation through the system',
                priority_calculator=lambda p: (
                    'medium' if p.get('has_database', False) or p['complexity']['total_functions'] >= 15 else
                    'low'
                ),
                required_context=['data_sources', 'transformations', 'data_stores'],
                min_complexity='medium',
            ),
            
            'er_diagram': DiagramType(
                type_id='er_diagram',
                name='Entity Relationship Diagram',
                category='data',
                mermaid_type='erDiagram',
                description='Database schema and entity relationships',
                priority_calculator=lambda p: (
                    'high' if p.get('has_database', False) else 'skip'
                ),
                required_context=['entities', 'relationships', 'attributes'],
                min_complexity='small',
            ),
        }
    
    def get_diagram_type(self, type_id: str) -> DiagramType:
        """Get a specific diagram type"""
        return self.diagram_types.get(type_id)
    
    def get_all_types(self) -> List[DiagramType]:
        """Get all diagram types"""
        return list(self.diagram_types.values())
    
    def get_types_by_category(self, category: str) -> List[DiagramType]:
        """Get all diagram types in a category"""
        return [dt for dt in self.diagram_types.values() if dt.category == category]
    
    def calculate_priorities(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Calculate priorities for all diagram types based on codebase profile
        
        Returns:
            List of diagram specs with calculated priorities
        """
        results = []
        
        for type_id, diagram_type in self.diagram_types.items():
            priority = diagram_type.calculate_priority(profile)
            
            if priority != 'skip':
                results.append({
                    'type_id': type_id,
                    'name': diagram_type.name,
                    'category': diagram_type.category,
                    'priority': priority,
                    'mermaid_type': diagram_type.mermaid_type,
                    'description': diagram_type.description,
                    'required_context': diagram_type.required_context,
                })
        
        # Sort by priority (high -> medium -> low) and then by category
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        results.sort(key=lambda x: (priority_order[x['priority']], x['category']))
        
        logger.info(f"Calculated priorities for {len(results)} diagrams")
        return results
    
    def get_recommended_diagrams(
        self,
        profile: Dict[str, Any],
        max_diagrams: int = 8,
        min_priority: str = 'low'
    ) -> List[Dict[str, Any]]:
        """
        Get recommended diagrams for a codebase profile
        
        Args:
            profile: Codebase profile from CodebaseAnalyzer
            max_diagrams: Maximum number of diagrams to recommend
            min_priority: Minimum priority level (high/medium/low)
            
        Returns:
            List of recommended diagram specifications
        """
        all_priorities = self.calculate_priorities(profile)
        
        # Filter by minimum priority
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        min_level = priority_order[min_priority]
        
        filtered = [
            d for d in all_priorities
            if priority_order[d['priority']] <= min_level
        ]
        
        # Limit to max_diagrams
        recommended = filtered[:max_diagrams]
        
        logger.info(f"Recommended {len(recommended)}/{len(all_priorities)} diagrams (max: {max_diagrams})")
        
        return recommended


# Global registry instance
diagram_registry = DiagramTypeRegistry()
