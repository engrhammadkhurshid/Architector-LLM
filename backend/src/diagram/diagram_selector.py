"""
Diagram Selector
LLM-powered agent that intelligently selects which diagrams to generate
"""

import logging
from typing import Dict, Any, List
from diagram.diagram_types import diagram_registry

logger = logging.getLogger(__name__)

class DiagramSelector:
    """
    Intelligent diagram selection using LLM reasoning
    """
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client
        self.registry = diagram_registry
    
    def select_diagrams(
        self,
        profile: Dict[str, Any],
        max_diagrams: int = 8,
        use_llm: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Select diagrams to generate based on codebase profile
        
        Args:
            profile: CodebaseProfile from CodebaseAnalyzer
            max_diagrams: Maximum number of diagrams to generate
            use_llm: Whether to use LLM for selection (advanced)
            
        Returns:
            List of selected diagram specifications with priorities and reasons
        """
        logger.info(f'Selecting diagrams for {profile.get("project_type")} project')
        
        if use_llm and self.llm_client:
            return self._select_with_llm(profile, max_diagrams)
        else:
            return self._select_rule_based(profile, max_diagrams)
    
    def _select_rule_based(
        self,
        profile: Dict[str, Any],
        max_diagrams: int
    ) -> List[Dict[str, Any]]:
        """
        Rule-based diagram selection using diagram type registry
        """
        # Get recommended diagrams from registry
        recommended = self.registry.get_recommended_diagrams(
            profile,
            max_diagrams=max_diagrams,
            min_priority='medium'  # Only high and medium priority
        )
        
        # Add reasoning for each selection
        for diagram_spec in recommended:
            diagram_spec['reason'] = self._generate_reason(diagram_spec, profile)
            diagram_spec['scenarios'] = self._generate_scenarios(diagram_spec, profile)
        
        # Log selection summary
        high_priority = sum(1 for d in recommended if d['priority'] == 'high')
        medium_priority = sum(1 for d in recommended if d['priority'] == 'medium')
        
        logger.info(f'Selected {len(recommended)} diagrams: {high_priority} high, {medium_priority} medium priority')
        
        return recommended
    
    def _select_with_llm(
        self,
        profile: Dict[str, Any],
        max_diagrams: int
    ) -> List[Dict[str, Any]]:
        """
        LLM-powered diagram selection with reasoning
        Future enhancement: Use LLM to intelligently select and prioritize
        """
        # For now, fallback to rule-based
        # TODO: Implement LLM-based selection in Phase 2
        logger.warning('LLM-based selection not yet implemented, using rule-based')
        return self._select_rule_based(profile, max_diagrams)
    
    def _generate_reason(self, diagram_spec: Dict[str, Any], profile: Dict[str, Any]) -> str:
        """Generate human-readable reason for diagram selection"""
        type_id = diagram_spec['type_id']
        priority = diagram_spec['priority']
        
        reasons = {
            'component': 'Essential for understanding system architecture and module relationships',
            'class': f'OOP design with {profile["complexity"]["total_classes"]} classes requires class structure visualization',
            'package': f'Large codebase ({profile["complexity"]["total_files"]} files) benefits from module organization view',
            'sequence': 'API-driven architecture requires interaction flow documentation',
            'activity': 'Complex business logic benefits from workflow visualization',
            'state': 'Stateful components detected, state machine diagram recommended',
            'c4_context': f'{profile.get("project_type", "Application")} requires system context documentation',
            'c4_container': 'Multi-component architecture with database and API layers',
            'deployment': 'Deployment configurations found, infrastructure diagram needed',
            'data_flow': 'Data processing system benefits from data flow visualization',
            'er_diagram': 'Database models detected, schema diagram essential',
        }
        
        reason = reasons.get(type_id, f'Recommended for {profile.get("project_type")} projects')
        
        if priority == 'high':
            return f'🔴 HIGH PRIORITY: {reason}'
        elif priority == 'medium':
            return f'🟡 MEDIUM PRIORITY: {reason}'
        else:
            return f'🟢 LOW PRIORITY: {reason}'
    
    def _generate_scenarios(self, diagram_spec: Dict[str, Any], profile: Dict[str, Any]) -> List[str]:
        """Generate specific scenarios for behavioral diagrams"""
        type_id = diagram_spec['type_id']
        
        if type_id == 'sequence':
            scenarios = []
            
            # API scenarios
            if profile.get('has_api'):
                scenarios.append('API Request Flow')
                
                if 'django' in profile.get('frameworks', []) or 'flask' in profile.get('frameworks', []):
                    scenarios.append('User Authentication')
                    scenarios.append('Data Retrieval')
            
            # General scenarios
            if profile['complexity']['total_classes'] >= 5:
                scenarios.append('Main Execution Flow')
            
            return scenarios[:3]  # Max 3 scenarios
        
        elif type_id == 'activity':
            scenarios = []
            
            if profile.get('project_type') == 'cli_tool':
                scenarios.append('Command Execution Flow')
            elif profile.get('has_database'):
                scenarios.append('Data Processing Workflow')
            else:
                scenarios.append('Main Business Logic')
            
            return scenarios[:2]  # Max 2 scenarios
        
        return []
    
    def generate_selection_report(self, selected_diagrams: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a report about diagram selection
        """
        categories = {}
        for diagram in selected_diagrams:
            category = diagram['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(diagram['name'])
        
        return {
            'total_diagrams': len(selected_diagrams),
            'high_priority': sum(1 for d in selected_diagrams if d['priority'] == 'high'),
            'medium_priority': sum(1 for d in selected_diagrams if d['priority'] == 'medium'),
            'categories': categories,
            'diagrams': [
                {
                    'name': d['name'],
                    'type': d['type_id'],
                    'priority': d['priority'],
                    'reason': d.get('reason', ''),
                    'scenarios': d.get('scenarios', []),
                }
                for d in selected_diagrams
            ]
        }
