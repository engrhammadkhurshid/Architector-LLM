"""
Diagram Quality Validator
Validates generated diagrams for syntax, completeness, clarity, and accuracy.
"""

from typing import Dict, List, Any, Optional
import re


class DiagramValidator:
    """Validates diagram quality across multiple dimensions."""
    
    def __init__(self):
        """Initialize validator with validation rules."""
        self.validators = {
            'component': self._validate_component_diagram,
            'class': self._validate_class_diagram,
            'sequence': self._validate_sequence_diagram,
            'activity': self._validate_activity_diagram,
            'data_flow': self._validate_data_flow_diagram,
            'c4_context': self._validate_c4_diagram,
            'c4_container': self._validate_c4_diagram,
            'er_diagram': self._validate_er_diagram,
            'package': self._validate_package_diagram,
            'state': self._validate_state_diagram,
            'deployment': self._validate_deployment_diagram
        }
    
    def validate(self, diagram_type: str, mermaid_code: str, context: Dict = None) -> Dict[str, Any]:
        """
        Validate a single diagram.
        
        Args:
            diagram_type: Type of diagram (e.g., 'component', 'class')
            mermaid_code: Generated Mermaid code
            context: Optional context used for generation
            
        Returns:
            Validation result with scores and recommendations
        """
        validator = self.validators.get(diagram_type, self._validate_generic)
        return validator(mermaid_code, context or {})
    
    def validate_all(self, diagram_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate all generated diagrams.
        
        Args:
            diagram_results: Dictionary of diagram generation results
            
        Returns:
            Dictionary mapping diagram types to validation results
        """
        validation_results = {}
        
        for diagram_type, result in diagram_results.items():
            if not result.get('success'):
                validation_results[diagram_type] = {
                    'validated': False,
                    'reason': 'Generation failed',
                    'overall_score': 0,
                    'scores': {
                        'syntax': 0,
                        'completeness': 0,
                        'clarity': 0,
                        'accuracy': 0
                    },
                    'issues': ['Generation failed'],
                    'recommendations': []
                }
                continue
            
            mermaid_code = result.get('mermaid_code', '')
            context = result.get('context', {})
            
            validation = self.validate(diagram_type, mermaid_code, context)
            validation_results[diagram_type] = validation
        
        return validation_results
    
    def _validate_generic(self, mermaid_code: str, context: Dict) -> Dict[str, Any]:
        """Generic validation for any diagram type."""
        scores = {
            'syntax': self._check_syntax(mermaid_code),
            'completeness': self._check_completeness_generic(mermaid_code),
            'clarity': self._check_clarity(mermaid_code),
            'accuracy': 75  # Default for generic
        }
        
        issues = []
        recommendations = []
        
        if scores['syntax'] < 90:
            issues.append('Potential syntax issues detected')
        if scores['completeness'] < 70:
            issues.append('Diagram appears incomplete')
        if scores['clarity'] < 70:
            issues.append('Diagram may be too complex or unclear')
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'diagram_type': 'generic',
            'scores': scores,
            'overall_score': round(overall, 2),
            'issues': issues,
            'recommendations': recommendations,
            'validated': True
        }
    
    def _validate_component_diagram(self, mermaid_code: str, context: Dict) -> Dict[str, Any]:
        """Validate component diagram."""
        scores = {
            'syntax': self._check_syntax(mermaid_code),
            'completeness': 0,
            'clarity': self._check_clarity(mermaid_code),
            'accuracy': 0
        }
        
        issues = []
        recommendations = []
        
        # Completeness: Should have components and relationships
        has_components = '[' in mermaid_code or '(' in mermaid_code
        has_relationships = '-->' in mermaid_code or '---' in mermaid_code
        has_external = '{{' in mermaid_code or context.get('external_dependencies')
        
        completeness = 0
        if has_components: completeness += 40
        if has_relationships: completeness += 40
        if has_external: completeness += 20
        scores['completeness'] = completeness
        
        # Accuracy: Compare with context
        expected_components = context.get('total_components', 0)
        actual_components = len(re.findall(r'\w+\[', mermaid_code))
        
        if expected_components > 0:
            accuracy = min(100, (actual_components / expected_components) * 100)
            scores['accuracy'] = accuracy
        else:
            scores['accuracy'] = 75
        
        # Issues and recommendations
        if not has_components:
            issues.append('No components defined')
            recommendations.append('Add component nodes with clear labels')
        
        if not has_relationships:
            issues.append('No relationships between components')
            recommendations.append('Show dependencies with arrows (-->)')
        
        if not has_external:
            recommendations.append('Consider showing external dependencies')
        
        if actual_components < expected_components * 0.5:
            issues.append(f'Only {actual_components} components shown, expected ~{expected_components}')
            recommendations.append('Include all major components for completeness')
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'diagram_type': 'component',
            'scores': scores,
            'overall_score': round(overall, 2),
            'issues': issues,
            'recommendations': recommendations,
            'validated': True
        }
    
    def _validate_class_diagram(self, mermaid_code: str, context: Dict) -> Dict[str, Any]:
        """Validate class diagram."""
        scores = {
            'syntax': self._check_syntax(mermaid_code, expected_start='classDiagram'),
            'completeness': 0,
            'clarity': self._check_clarity(mermaid_code),
            'accuracy': 0
        }
        
        issues = []
        recommendations = []
        
        # Completeness: Should have classes, methods, attributes, relationships
        has_classes = 'class ' in mermaid_code
        has_methods = '()' in mermaid_code
        has_attributes = ':' in mermaid_code
        has_relationships = any(rel in mermaid_code for rel in ['<|--', '*--', 'o--', '-->'])
        
        completeness = 0
        if has_classes: completeness += 30
        if has_methods: completeness += 25
        if has_attributes: completeness += 20
        if has_relationships: completeness += 25
        scores['completeness'] = completeness
        
        # Accuracy: Compare with context
        expected_classes = context.get('total_classes', 0)
        actual_classes = mermaid_code.count('class ')
        
        if expected_classes > 0:
            accuracy = min(100, (actual_classes / expected_classes) * 100)
            scores['accuracy'] = accuracy
        else:
            scores['accuracy'] = 75
        
        # Check for visibility modifiers
        has_visibility = any(vis in mermaid_code for vis in ['+', '-', '#', '~'])
        
        # Issues and recommendations
        if not has_classes:
            issues.append('No classes defined')
            recommendations.append('Add class definitions with attributes and methods')
        
        if not has_methods and not has_attributes:
            issues.append('Classes lack methods and attributes')
            recommendations.append('Include key methods and attributes for each class')
        
        if not has_visibility:
            recommendations.append('Add visibility modifiers (+public, -private, #protected)')
        
        if not has_relationships:
            issues.append('No relationships between classes')
            recommendations.append('Show inheritance (<|--), composition (*--), and associations (-->)')
        
        if actual_classes < expected_classes * 0.6:
            issues.append(f'Only {actual_classes} classes shown, expected ~{expected_classes}')
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'diagram_type': 'class',
            'scores': scores,
            'overall_score': round(overall, 2),
            'issues': issues,
            'recommendations': recommendations,
            'validated': True
        }
    
    def _validate_sequence_diagram(self, mermaid_code: str, context: Dict) -> Dict[str, Any]:
        """Validate sequence diagram."""
        scores = {
            'syntax': self._check_syntax(mermaid_code, expected_start='sequenceDiagram'),
            'completeness': 0,
            'clarity': self._check_clarity(mermaid_code),
            'accuracy': 0
        }
        
        issues = []
        recommendations = []
        
        # Completeness: Should have participants and messages
        has_participants = 'participant ' in mermaid_code or 'actor ' in mermaid_code
        has_messages = '->>' in mermaid_code or '-->' in mermaid_code
        has_activations = 'activate' in mermaid_code or 'deactivate' in mermaid_code
        has_notes = 'Note ' in mermaid_code
        
        completeness = 0
        if has_participants: completeness += 30
        if has_messages: completeness += 50
        if has_activations: completeness += 10
        if has_notes: completeness += 10
        scores['completeness'] = completeness
        
        # Accuracy: Check for reasonable interaction count
        expected_interactions = context.get('interaction_count', 0)
        actual_interactions = mermaid_code.count('->>')
        
        if expected_interactions > 0:
            accuracy = min(100, (actual_interactions / expected_interactions) * 100)
            scores['accuracy'] = accuracy
        else:
            scores['accuracy'] = 75
        
        # Issues and recommendations
        if not has_participants:
            issues.append('No participants defined')
            recommendations.append('Define participants with "participant" or "actor"')
        
        if not has_messages:
            issues.append('No message flows')
            recommendations.append('Add message flows with ->> or -->')
        
        if not has_activations:
            recommendations.append('Consider adding activation boxes to show processing time')
        
        message_count = mermaid_code.count('->>')
        if message_count < 3:
            issues.append('Very few interactions shown')
            recommendations.append('Include more message exchanges for completeness')
        elif message_count > 20:
            recommendations.append('Consider splitting into multiple sequence diagrams')
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'diagram_type': 'sequence',
            'scores': scores,
            'overall_score': round(overall, 2),
            'issues': issues,
            'recommendations': recommendations,
            'validated': True
        }
    
    def _validate_activity_diagram(self, mermaid_code: str, context: Dict) -> Dict[str, Any]:
        """Validate activity diagram (flowchart)."""
        scores = {
            'syntax': self._check_syntax(mermaid_code, expected_start='flowchart'),
            'completeness': 0,
            'clarity': self._check_clarity(mermaid_code),
            'accuracy': 75
        }
        
        issues = []
        recommendations = []
        
        # Completeness: Should have start, end, activities, decisions
        has_start = '[Start]' in mermaid_code or '([Start])' in mermaid_code or '[*]' in mermaid_code
        has_end = '[End]' in mermaid_code or '([End])' in mermaid_code
        has_activities = '[' in mermaid_code
        has_decisions = '{' in mermaid_code or '{{' in mermaid_code
        has_flow = '-->' in mermaid_code
        
        completeness = 0
        if has_start: completeness += 15
        if has_end: completeness += 15
        if has_activities: completeness += 40
        if has_decisions: completeness += 15
        if has_flow: completeness += 15
        scores['completeness'] = completeness
        
        # Issues and recommendations
        if not has_start:
            recommendations.append('Add a start node: ([Start])')
        
        if not has_end:
            recommendations.append('Add an end node: ([End])')
        
        if not has_decisions:
            recommendations.append('Add decision points for conditionals: {Decision?}')
        
        if not has_flow:
            issues.append('No flow arrows between activities')
            recommendations.append('Connect activities with -->')
        
        activity_count = mermaid_code.count('[')
        if activity_count < 3:
            issues.append('Very few activities shown')
            recommendations.append('Include more activities to show complete workflow')
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'diagram_type': 'activity',
            'scores': scores,
            'overall_score': round(overall, 2),
            'issues': issues,
            'recommendations': recommendations,
            'validated': True
        }
    
    def _validate_data_flow_diagram(self, mermaid_code: str, context: Dict) -> Dict[str, Any]:
        """Validate data flow diagram."""
        scores = {
            'syntax': self._check_syntax(mermaid_code, expected_start='flowchart'),
            'completeness': 0,
            'clarity': self._check_clarity(mermaid_code),
            'accuracy': 75
        }
        
        issues = []
        recommendations = []
        
        # Completeness: Should have sources, processes, stores, sinks
        has_sources = '([' in mermaid_code  # External entities
        has_processes = '[' in mermaid_code  # Processes
        has_stores = '[(Database)]' in mermaid_code or '[(' in mermaid_code  # Data stores
        has_flows = '|' in mermaid_code or '-->' in mermaid_code  # Labeled flows
        
        completeness = 0
        if has_sources: completeness += 25
        if has_processes: completeness += 35
        if has_stores: completeness += 20
        if has_flows: completeness += 20
        scores['completeness'] = completeness
        
        # Issues and recommendations
        if not has_sources:
            recommendations.append('Show data sources with ([External Entity])')
        
        if not has_processes:
            issues.append('No data transformation processes')
            recommendations.append('Add processing nodes: [Transform Data]')
        
        if not has_stores:
            recommendations.append('Include data stores if applicable: [(Database)]')
        
        if not has_flows:
            issues.append('No labeled data flows')
            recommendations.append('Label arrows with data names: -->|data|')
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'diagram_type': 'data_flow',
            'scores': scores,
            'overall_score': round(overall, 2),
            'issues': issues,
            'recommendations': recommendations,
            'validated': True
        }
    
    def _validate_c4_diagram(self, mermaid_code: str, context: Dict) -> Dict[str, Any]:
        """Validate C4 context/container diagram."""
        scores = {
            'syntax': self._check_syntax(mermaid_code),
            'completeness': 0,
            'clarity': self._check_clarity(mermaid_code),
            'accuracy': 75
        }
        
        issues = []
        recommendations = []
        
        # Completeness: Should have system, users, external systems
        has_system = '[' in mermaid_code
        has_users = '([' in mermaid_code  # Actors
        has_external = '{{' in mermaid_code  # External systems
        has_relationships = '-->' in mermaid_code
        
        completeness = 0
        if has_system: completeness += 30
        if has_users: completeness += 30
        if has_external: completeness += 20
        if has_relationships: completeness += 20
        scores['completeness'] = completeness
        
        # Issues and recommendations
        if not has_system:
            issues.append('No system defined')
            recommendations.append('Add the main system: [System Name]')
        
        if not has_users:
            recommendations.append('Show users/actors: ([User])')
        
        if not has_external:
            recommendations.append('Show external systems: {{External System}}')
        
        if not has_relationships:
            issues.append('No relationships shown')
            recommendations.append('Connect entities with labeled arrows: -->|uses|')
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'diagram_type': 'c4_context',
            'scores': scores,
            'overall_score': round(overall, 2),
            'issues': issues,
            'recommendations': recommendations,
            'validated': True
        }
    
    def _validate_er_diagram(self, mermaid_code: str, context: Dict) -> Dict[str, Any]:
        """Validate ER diagram."""
        scores = {
            'syntax': self._check_syntax(mermaid_code, expected_start='erDiagram'),
            'completeness': 0,
            'clarity': self._check_clarity(mermaid_code),
            'accuracy': 0
        }
        
        issues = []
        recommendations = []
        
        # Completeness: Should have entities, attributes, relationships
        has_entities = '{' in mermaid_code
        has_attributes = 'int ' in mermaid_code or 'string ' in mermaid_code or 'PK' in mermaid_code
        has_relationships = '||' in mermaid_code or '}}' in mermaid_code or 'o{' in mermaid_code
        
        completeness = 0
        if has_entities: completeness += 40
        if has_attributes: completeness += 30
        if has_relationships: completeness += 30
        scores['completeness'] = completeness
        
        # Accuracy: Compare with context
        expected_entities = context.get('total_entities', 0)
        actual_entities = mermaid_code.count('{')
        
        if expected_entities > 0:
            accuracy = min(100, (actual_entities / expected_entities) * 100)
            scores['accuracy'] = accuracy
        else:
            scores['accuracy'] = 75
        
        # Issues and recommendations
        if not has_entities:
            issues.append('No entities defined')
            recommendations.append('Define entities with attributes')
        
        if not has_attributes:
            issues.append('Entities lack attributes')
            recommendations.append('Add attributes with types (int, string, etc.)')
        
        if not has_relationships:
            issues.append('No relationships between entities')
            recommendations.append('Show relationships with cardinality (||--o{, etc.)')
        
        if 'PK' not in mermaid_code:
            recommendations.append('Mark primary keys with PK')
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'diagram_type': 'er_diagram',
            'scores': scores,
            'overall_score': round(overall, 2),
            'issues': issues,
            'recommendations': recommendations,
            'validated': True
        }
    
    def _validate_package_diagram(self, mermaid_code: str, context: Dict) -> Dict[str, Any]:
        """Validate package diagram."""
        scores = {
            'syntax': self._check_syntax(mermaid_code),
            'completeness': 0,
            'clarity': self._check_clarity(mermaid_code),
            'accuracy': 75
        }
        
        issues = []
        recommendations = []
        
        # Completeness: Should have subgraphs (packages) and dependencies
        has_subgraphs = 'subgraph' in mermaid_code
        has_packages = '[' in mermaid_code
        has_dependencies = '-->' in mermaid_code
        
        completeness = 0
        if has_subgraphs: completeness += 40
        if has_packages: completeness += 30
        if has_dependencies: completeness += 30
        scores['completeness'] = completeness
        
        # Issues and recommendations
        if not has_subgraphs:
            recommendations.append('Use subgraphs to represent packages')
        
        if not has_packages:
            issues.append('No package modules shown')
            recommendations.append('Add package modules within subgraphs')
        
        if not has_dependencies:
            issues.append('No dependencies between packages')
            recommendations.append('Show inter-package dependencies with -->')
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'diagram_type': 'package',
            'scores': scores,
            'overall_score': round(overall, 2),
            'issues': issues,
            'recommendations': recommendations,
            'validated': True
        }
    
    def _validate_state_diagram(self, mermaid_code: str, context: Dict) -> Dict[str, Any]:
        """Validate state diagram."""
        scores = {
            'syntax': self._check_syntax(mermaid_code, expected_start='stateDiagram'),
            'completeness': 0,
            'clarity': self._check_clarity(mermaid_code),
            'accuracy': 75
        }
        
        issues = []
        recommendations = []
        
        # Completeness: Should have states, transitions, initial/final states
        has_states = 'state' in mermaid_code or ':' in mermaid_code
        has_transitions = '-->' in mermaid_code
        has_initial = '[*]' in mermaid_code
        
        completeness = 0
        if has_states: completeness += 40
        if has_transitions: completeness += 40
        if has_initial: completeness += 20
        scores['completeness'] = completeness
        
        # Issues and recommendations
        if not has_states:
            issues.append('No states defined')
            recommendations.append('Define states with clear names')
        
        if not has_transitions:
            issues.append('No transitions between states')
            recommendations.append('Add transitions with labels: State1 --> State2 : event')
        
        if not has_initial:
            recommendations.append('Add initial state: [*] --> InitialState')
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'diagram_type': 'state',
            'scores': scores,
            'overall_score': round(overall, 2),
            'issues': issues,
            'recommendations': recommendations,
            'validated': True
        }
    
    def _validate_deployment_diagram(self, mermaid_code: str, context: Dict) -> Dict[str, Any]:
        """Validate deployment diagram."""
        scores = {
            'syntax': self._check_syntax(mermaid_code),
            'completeness': 0,
            'clarity': self._check_clarity(mermaid_code),
            'accuracy': 75
        }
        
        issues = []
        recommendations = []
        
        # Completeness: Should have nodes, components, connections
        has_nodes = '[' in mermaid_code  # Deployment nodes
        has_components = '{{' in mermaid_code or has_nodes
        has_connections = '-->' in mermaid_code
        has_protocols = '|' in mermaid_code  # Labeled connections
        
        completeness = 0
        if has_nodes: completeness += 35
        if has_components: completeness += 35
        if has_connections: completeness += 20
        if has_protocols: completeness += 10
        scores['completeness'] = completeness
        
        # Issues and recommendations
        if not has_nodes:
            issues.append('No deployment nodes shown')
            recommendations.append('Add deployment nodes (servers, containers): [Server]')
        
        if not has_connections:
            issues.append('No network connections')
            recommendations.append('Show connections between nodes: -->|HTTP|')
        
        if not has_protocols:
            recommendations.append('Label connections with protocols (HTTP, TCP, etc.)')
        
        overall = sum(scores.values()) / len(scores)
        
        return {
            'diagram_type': 'deployment',
            'scores': scores,
            'overall_score': round(overall, 2),
            'issues': issues,
            'recommendations': recommendations,
            'validated': True
        }
    
    def _check_syntax(self, mermaid_code: str, expected_start: str = None) -> float:
        """Check basic Mermaid syntax validity."""
        score = 100.0
        
        # Check for valid diagram type declaration
        valid_starts = [
            'graph ', 'flowchart ', 'sequenceDiagram', 'classDiagram',
            'stateDiagram', 'erDiagram', 'journey', 'gantt', 'pie'
        ]
        
        has_valid_start = any(mermaid_code.strip().startswith(start) for start in valid_starts)
        if not has_valid_start:
            score -= 30
        
        # Check for expected start if specified
        if expected_start and not mermaid_code.strip().startswith(expected_start):
            score -= 20
        
        # Check minimum length
        if len(mermaid_code) < 50:
            score -= 25
        
        # Check for balanced brackets (simple check)
        open_brackets = mermaid_code.count('[') + mermaid_code.count('(') + mermaid_code.count('{')
        close_brackets = mermaid_code.count(']') + mermaid_code.count(')') + mermaid_code.count('}')
        if abs(open_brackets - close_brackets) > 2:
            score -= 15
        
        return max(0, score)
    
    def _check_completeness_generic(self, mermaid_code: str) -> float:
        """Check generic completeness."""
        score = 0.0
        
        # Has nodes
        if '[' in mermaid_code or '(' in mermaid_code:
            score += 40
        
        # Has relationships
        if '-->' in mermaid_code or '---' in mermaid_code:
            score += 40
        
        # Has labels
        if '|' in mermaid_code:
            score += 20
        
        return score
    
    def _check_clarity(self, mermaid_code: str) -> float:
        """Check diagram clarity (not too simple or complex)."""
        lines = mermaid_code.count('\n')
        nodes = mermaid_code.count('[') + mermaid_code.count('(')
        
        # Optimal range: 5-20 nodes, 10-50 lines
        clarity = 100.0
        
        if nodes < 2:
            clarity -= 30  # Too simple
        elif nodes < 5:
            clarity -= 10
        elif nodes > 25:
            clarity -= 20  # Too complex
        elif nodes > 15:
            clarity -= 5
        
        if lines < 5:
            clarity -= 20
        elif lines > 80:
            clarity -= 15
        
        return max(0, clarity)
