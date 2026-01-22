"""
Cross-Diagram Relationship Mapper
Analyzes relationships and dependencies between different diagrams.
"""

from typing import Dict, List, Any, Set, Tuple
import re


class RelationshipMapper:
    """Maps relationships and shared entities across multiple diagrams."""
    
    def __init__(self):
        self.entity_pattern = re.compile(r'[A-Z][a-zA-Z0-9_]*')
    
    def map_relationships(
        self,
        diagram_results: Dict[str, Any],
        dependency_graph: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Analyze and map cross-diagram relationships.
        
        Args:
            diagram_results: Generated diagram results from MultiDiagramGenerator
            dependency_graph: Optional dependency graph for enhanced analysis
            
        Returns:
            Dictionary containing:
            - shared_entities: Entities appearing in multiple diagrams
            - diagram_connections: How diagrams relate to each other
            - entity_locations: Where each entity appears
            - coverage_analysis: What aspects are covered by multiple views
        """
        # Extract entities from each diagram
        diagram_entities = {}
        for diagram_type, result in diagram_results.items():
            if result.get('success'):
                mermaid_code = result.get('mermaid_code', '')
                entities = self._extract_entities(diagram_type, mermaid_code)
                diagram_entities[diagram_type] = entities
        
        # Find shared entities
        shared_entities = self._find_shared_entities(diagram_entities)
        
        # Map diagram connections
        connections = self._map_diagram_connections(diagram_entities, shared_entities)
        
        # Create entity location map
        entity_locations = self._create_entity_locations(diagram_entities)
        
        # Analyze coverage
        coverage = self._analyze_coverage(diagram_results, diagram_entities, dependency_graph)
        
        return {
            'shared_entities': shared_entities,
            'diagram_connections': connections,
            'entity_locations': entity_locations,
            'coverage_analysis': coverage,
            'diagrams_analyzed': list(diagram_entities.keys())
        }
    
    def _extract_entities(self, diagram_type: str, mermaid_code: str) -> Set[str]:
        """Extract entities from Mermaid diagram code."""
        entities = set()
        
        # Diagram-specific extraction
        if diagram_type == 'component':
            # Extract component names: A[Component Name]
            entities.update(re.findall(r'([A-Z][a-zA-Z0-9_]*)\[', mermaid_code))
            # Extract from subgraphs
            entities.update(re.findall(r'subgraph\s+([A-Z][a-zA-Z0-9_\s]+)', mermaid_code))
        
        elif diagram_type == 'class':
            # Extract class names: class ClassName
            entities.update(re.findall(r'class\s+([A-Z][a-zA-Z0-9_]+)', mermaid_code))
        
        elif diagram_type == 'sequence':
            # Extract participants
            entities.update(re.findall(r'participant\s+([A-Z][a-zA-Z0-9_]+)', mermaid_code))
            # Extract from interactions
            interactions = re.findall(r'([A-Z][a-zA-Z0-9_]+)->>([A-Z][a-zA-Z0-9_]+)', mermaid_code)
            for from_entity, to_entity in interactions:
                entities.add(from_entity)
                entities.add(to_entity)
        
        elif diagram_type == 'c4_context' or diagram_type == 'c4_container':
            # Extract systems and containers
            entities.update(re.findall(r'System\s*\(\s*([A-Za-z0-9_]+)', mermaid_code))
            entities.update(re.findall(r'Person\s*\(\s*([A-Za-z0-9_]+)', mermaid_code))
            entities.update(re.findall(r'Container\s*\(\s*([A-Za-z0-9_]+)', mermaid_code))
        
        elif diagram_type == 'er':
            # Extract entity names
            entities.update(re.findall(r'([A-Z][A-Z0-9_]+)\s*\{', mermaid_code))
        
        elif diagram_type == 'package':
            # Extract package names from subgraphs
            entities.update(re.findall(r'subgraph\s+([a-zA-Z][a-zA-Z0-9_\.]+)', mermaid_code))
        
        elif diagram_type == 'state':
            # Extract state names
            entities.update(re.findall(r'state\s+"([^"]+)"', mermaid_code))
            entities.update(re.findall(r'state\s+([A-Z][a-zA-Z0-9_]+)', mermaid_code))
        
        elif diagram_type == 'deployment':
            # Extract nodes and components
            entities.update(re.findall(r'node\s+([A-Z][a-zA-Z0-9_]+)', mermaid_code))
        
        elif diagram_type in ['activity', 'data_flow']:
            # Extract nodes
            entities.update(re.findall(r'([A-Z][a-zA-Z0-9_]+)\[', mermaid_code))
            entities.update(re.findall(r'([A-Z][a-zA-Z0-9_]+)\{', mermaid_code))
            entities.update(re.findall(r'([A-Z][a-zA-Z0-9_]+)\(', mermaid_code))
        
        # Clean up entities
        entities = {e.strip() for e in entities if e and len(e) > 1}
        
        return entities
    
    def _find_shared_entities(self, diagram_entities: Dict[str, Set[str]]) -> Dict[str, List[str]]:
        """Find entities that appear in multiple diagrams."""
        entity_diagrams = {}
        
        for diagram_type, entities in diagram_entities.items():
            for entity in entities:
                if entity not in entity_diagrams:
                    entity_diagrams[entity] = []
                entity_diagrams[entity].append(diagram_type)
        
        # Filter to only shared entities (appears in 2+ diagrams)
        shared = {
            entity: diagrams
            for entity, diagrams in entity_diagrams.items()
            if len(diagrams) > 1
        }
        
        return shared
    
    def _map_diagram_connections(
        self,
        diagram_entities: Dict[str, Set[str]],
        shared_entities: Dict[str, List[str]]
    ) -> List[Dict[str, Any]]:
        """Map connections between diagrams based on shared entities."""
        connections = []
        
        diagram_types = list(diagram_entities.keys())
        
        for i, diagram1 in enumerate(diagram_types):
            for diagram2 in diagram_types[i+1:]:
                # Find entities shared between these two diagrams
                shared = diagram_entities[diagram1] & diagram_entities[diagram2]
                
                if shared:
                    connections.append({
                        'from': diagram1,
                        'to': diagram2,
                        'shared_entities': list(shared),
                        'connection_strength': len(shared),
                        'relationship_type': self._classify_relationship(diagram1, diagram2)
                    })
        
        # Sort by connection strength
        connections.sort(key=lambda x: x['connection_strength'], reverse=True)
        
        return connections
    
    def _classify_relationship(self, diagram1: str, diagram2: str) -> str:
        """Classify the relationship type between two diagrams."""
        structural = {'component', 'class', 'package', 'deployment'}
        behavioral = {'sequence', 'activity', 'state'}
        data_related = {'data_flow', 'er'}
        architectural = {'c4_context', 'c4_container'}
        
        d1_cat = (
            'structural' if diagram1 in structural else
            'behavioral' if diagram1 in behavioral else
            'data' if diagram1 in data_related else
            'architectural'
        )
        
        d2_cat = (
            'structural' if diagram2 in structural else
            'behavioral' if diagram2 in behavioral else
            'data' if diagram2 in data_related else
            'architectural'
        )
        
        if d1_cat == d2_cat:
            return f'complementary_{d1_cat}'
        else:
            return f'{d1_cat}_to_{d2_cat}'
    
    def _create_entity_locations(self, diagram_entities: Dict[str, Set[str]]) -> Dict[str, List[str]]:
        """Create a map of where each entity appears."""
        entity_locations = {}
        
        for diagram_type, entities in diagram_entities.items():
            for entity in entities:
                if entity not in entity_locations:
                    entity_locations[entity] = []
                entity_locations[entity].append(diagram_type)
        
        return entity_locations
    
    def _analyze_coverage(
        self,
        diagram_results: Dict[str, Any],
        diagram_entities: Dict[str, Set[str]],
        dependency_graph: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Analyze what aspects of the system are covered by multiple views."""
        coverage = {
            'structural_views': 0,
            'behavioral_views': 0,
            'data_views': 0,
            'architectural_views': 0,
            'multi_view_entities': [],
            'coverage_gaps': []
        }
        
        # Count views by category
        for diagram_type in diagram_results.keys():
            if diagram_type in {'component', 'class', 'package', 'deployment'}:
                coverage['structural_views'] += 1
            elif diagram_type in {'sequence', 'activity', 'state'}:
                coverage['behavioral_views'] += 1
            elif diagram_type in {'data_flow', 'er'}:
                coverage['data_views'] += 1
            elif diagram_type in {'c4_context', 'c4_container'}:
                coverage['architectural_views'] += 1
        
        # Find entities with multiple views
        for entity, diagrams in self._find_shared_entities(diagram_entities).items():
            if len(diagrams) >= 3:
                coverage['multi_view_entities'].append({
                    'entity': entity,
                    'views': diagrams,
                    'coverage_score': len(diagrams)
                })
        
        # Identify coverage gaps
        if coverage['structural_views'] == 0:
            coverage['coverage_gaps'].append('No structural views (component/class diagrams)')
        if coverage['behavioral_views'] == 0:
            coverage['coverage_gaps'].append('No behavioral views (sequence/activity diagrams)')
        if coverage['data_views'] == 0:
            coverage['coverage_gaps'].append('No data views (ER/data flow diagrams)')
        
        # Check if major entities are well-covered
        if dependency_graph:
            major_entities = self._get_major_entities(dependency_graph)
            uncovered = [
                entity for entity in major_entities
                if entity not in diagram_entities or len(diagram_entities.get(entity, [])) < 2
            ]
            if uncovered:
                coverage['coverage_gaps'].append(f'Major entities with limited coverage: {", ".join(uncovered[:5])}')
        
        return coverage
    
    def _get_major_entities(self, dependency_graph: Dict[str, Any]) -> List[str]:
        """Extract major entities from dependency graph (high-degree nodes)."""
        nodes = dependency_graph.get('nodes', [])
        
        # Sort by out-degree (number of dependencies)
        major_nodes = sorted(
            [n for n in nodes if n.get('type') in ['class', 'module']],
            key=lambda n: len(n.get('dependencies', [])),
            reverse=True
        )
        
        return [n['name'] for n in major_nodes[:10]]
    
    def generate_relationship_report(self, relationship_map: Dict[str, Any]) -> str:
        """Generate a markdown report of cross-diagram relationships."""
        report = """# Cross-Diagram Relationship Analysis

## Overview

This report analyzes the relationships and connections between different architecture diagrams.

---

"""
        
        # Shared entities section
        shared = relationship_map['shared_entities']
        report += f"## Shared Entities ({len(shared)} found)\n\n"
        
        if shared:
            report += "Entities appearing in multiple diagrams:\n\n"
            report += "| Entity | Appears In | Views |\n"
            report += "|--------|------------|-------|\n"
            
            for entity, diagrams in sorted(shared.items(), key=lambda x: len(x[1]), reverse=True):
                diagram_list = ", ".join([d.replace('_', ' ').title() for d in diagrams])
                report += f"| {entity} | {diagram_list} | {len(diagrams)} |\n"
        else:
            report += "*No shared entities found across diagrams.*\n"
        
        report += "\n---\n\n"
        
        # Diagram connections
        connections = relationship_map['diagram_connections']
        report += f"## Diagram Connections ({len(connections)} found)\n\n"
        
        if connections:
            report += "Strong connections between diagrams:\n\n"
            for conn in connections[:10]:  # Top 10
                from_name = conn['from'].replace('_', ' ').title()
                to_name = conn['to'].replace('_', ' ').title()
                strength = conn['connection_strength']
                rel_type = conn['relationship_type'].replace('_', ' ').title()
                
                report += f"### {from_name} ↔ {to_name}\n\n"
                report += f"- **Connection Strength:** {strength} shared entities\n"
                report += f"- **Relationship Type:** {rel_type}\n"
                report += f"- **Shared Entities:** {', '.join(conn['shared_entities'][:5])}\n\n"
        else:
            report += "*No strong connections found.*\n"
        
        report += "\n---\n\n"
        
        # Coverage analysis
        coverage = relationship_map['coverage_analysis']
        report += "## Coverage Analysis\n\n"
        
        report += f"### Diagram Distribution\n\n"
        report += f"- **Structural Views:** {coverage['structural_views']}\n"
        report += f"- **Behavioral Views:** {coverage['behavioral_views']}\n"
        report += f"- **Data Views:** {coverage['data_views']}\n"
        report += f"- **Architectural Views:** {coverage['architectural_views']}\n\n"
        
        # Multi-view entities
        multi_view = coverage.get('multi_view_entities', [])
        if multi_view:
            report += f"### Well-Covered Entities ({len(multi_view)})\n\n"
            report += "Entities with comprehensive coverage across multiple views:\n\n"
            for item in multi_view[:10]:
                report += f"- **{item['entity']}** ({item['coverage_score']} views): {', '.join(item['views'])}\n"
            report += "\n"
        
        # Coverage gaps
        gaps = coverage.get('coverage_gaps', [])
        if gaps:
            report += "### Coverage Gaps\n\n"
            for gap in gaps:
                report += f"- ⚠️ {gap}\n"
            report += "\n"
        
        report += "---\n\n"
        report += "*Generated by Architector-LLM Relationship Mapper*\n"
        
        return report
