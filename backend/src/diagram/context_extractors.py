"""
Context extractors for specialized diagram generation.
Each extractor tailors information from the dependency graph for specific diagram types.
"""

from typing import Dict, List, Any, Set
import json


class BaseContextExtractor:
    """Base class for all context extractors."""
    
    def extract(self, graph: Dict, profile: Dict, scenario: str = None) -> Dict[str, Any]:
        """
        Extract context from dependency graph for specific diagram type.
        
        Args:
            graph: Dependency graph from GraphBuilder
            profile: CodebaseProfile from CodebaseAnalyzer
            scenario: Optional scenario description (for behavioral diagrams)
            
        Returns:
            Dictionary with diagram-specific context
        """
        raise NotImplementedError("Subclasses must implement extract()")
    
    def _get_nodes_by_type(self, graph: Dict, node_types: List[str]) -> List[Dict]:
        """Get all nodes of specific types."""
        nodes = []
        for node in graph.get('nodes', []):
            if node.get('type') in node_types:
                nodes.append(node)
        return nodes
    
    def _get_edges_for_node(self, graph: Dict, node_id: str) -> List[Dict]:
        """Get all edges connected to a specific node."""
        edges = []
        for edge in graph.get('edges', []):
            if edge.get('source') == node_id or edge.get('target') == node_id:
                edges.append(edge)
        return edges
    
    def _find_external_dependencies(self, graph: Dict) -> List[str]:
        """Find external packages/modules used."""
        external = set()
        for node in graph.get('nodes', []):
            if node.get('type') == 'import':
                module = node.get('name', '')
                # Extract top-level package
                top_level = module.split('.')[0]
                if top_level and not self._is_internal(top_level, graph):
                    external.add(top_level)
        return sorted(list(external))
    
    def _is_internal(self, module_name: str, graph: Dict) -> bool:
        """Check if module is internal to the project."""
        for node in graph.get('nodes', []):
            if node.get('type') == 'file':
                file_path = node.get('name', '')
                # Check if module name matches any internal file
                if module_name.replace('.', '/') in file_path or \
                   file_path.replace('/', '.').startswith(module_name):
                    return True
        return False
    
    def _find_node_by_id(self, graph: Dict, node_id: str) -> Dict:
        """Find node by ID."""
        for node in graph.get('nodes', []):
            if node.get('id') == node_id:
                return node
        return None


class ComponentContextExtractor(BaseContextExtractor):
    """Extract context for Component Diagrams."""
    
    def extract(self, graph: Dict, profile: Dict, scenario: str = None) -> Dict[str, Any]:
        """Extract modules, components, and their dependencies."""
        
        # Get all modules/files
        files = self._get_nodes_by_type(graph, ['file', 'module'])
        
        # Group by logical components
        components = self._identify_components(files, graph)
        
        # Extract external dependencies
        external_deps = self._find_external_dependencies(graph)
        
        # Extract inter-component dependencies
        component_deps = self._extract_component_dependencies(components, graph)
        
        return {
            'diagram_type': 'component',
            'components': components,
            'external_dependencies': external_deps,
            'component_relationships': component_deps,
            'project_type': profile.get('project_type'),
            'frameworks': profile.get('frameworks', []),
            'total_components': len(components)
        }
    
    def _identify_components(self, files: List[Dict], graph: Dict) -> List[Dict]:
        """Identify logical components from files."""
        components = []
        
        # Group files by directory
        dir_groups = {}
        for file_node in files:
            file_path = file_node.get('name', '')
            # Extract directory
            parts = file_path.split('/')
            if len(parts) > 1:
                directory = parts[-2] if len(parts) > 2 else parts[0]
            else:
                directory = 'root'
            
            if directory not in dir_groups:
                dir_groups[directory] = []
            dir_groups[directory].append(file_node)
        
        # Create component for each directory
        for dir_name, file_nodes in dir_groups.items():
            components.append({
                'name': dir_name,
                'files': [f.get('name') for f in file_nodes],
                'file_count': len(file_nodes)
            })
        
        return components
    
    def _extract_component_dependencies(self, components: List[Dict], graph: Dict) -> List[Dict]:
        """Extract dependencies between components."""
        deps = []
        
        for i, comp1 in enumerate(components):
            for comp2 in components[i+1:]:
                # Check if any files in comp1 import files in comp2
                if self._components_connected(comp1, comp2, graph):
                    deps.append({
                        'from': comp1['name'],
                        'to': comp2['name'],
                        'type': 'depends_on'
                    })
        
        return deps
    
    def _components_connected(self, comp1: Dict, comp2: Dict, graph: Dict) -> bool:
        """Check if two components have dependencies."""
        for edge in graph.get('edges', []):
            source = edge.get('source', '')
            target = edge.get('target', '')
            
            # Check if edge connects files from different components
            if any(f in source for f in comp1.get('files', [])) and \
               any(f in target for f in comp2.get('files', [])):
                return True
        
        return False


class ClassContextExtractor(BaseContextExtractor):
    """Extract context for Class Diagrams."""
    
    def extract(self, graph: Dict, profile: Dict, scenario: str = None) -> Dict[str, Any]:
        """Extract classes, attributes, methods, and relationships."""
        
        # Get all classes
        classes = self._get_nodes_by_type(graph, ['class'])
        
        # Extract class details
        class_details = []
        for cls in classes:
            details = self._extract_class_details(cls, graph)
            class_details.append(details)
        
        # Extract relationships (inheritance, composition, etc.)
        relationships = self._extract_class_relationships(graph)
        
        return {
            'diagram_type': 'class',
            'classes': class_details,
            'relationships': relationships,
            'total_classes': len(class_details),
            'has_inheritance': any(r['type'] == 'inherits' for r in relationships),
            'has_composition': any(r['type'] in ['has_a', 'uses'] for r in relationships)
        }
    
    def _extract_class_details(self, class_node: Dict, graph: Dict) -> Dict:
        """Extract detailed information about a class."""
        class_name = class_node.get('name', '')
        
        # Find methods and attributes
        methods = []
        attributes = []
        
        for edge in graph.get('edges', []):
            if edge.get('source') == class_node.get('id'):
                target_id = edge.get('target')
                target_node = self._find_node_by_id(graph, target_id)
                
                if target_node:
                    if target_node.get('type') == 'function':
                        methods.append({
                            'name': target_node.get('name', ''),
                            'visibility': self._infer_visibility(target_node.get('name', ''))
                        })
                    elif target_node.get('type') == 'variable':
                        attributes.append({
                            'name': target_node.get('name', ''),
                            'visibility': self._infer_visibility(target_node.get('name', ''))
                        })
        
        return {
            'name': class_name,
            'methods': methods[:10],  # Limit to 10 most important
            'attributes': attributes[:10],  # Limit to 10
            'method_count': len(methods),
            'attribute_count': len(attributes)
        }
    
    def _find_node_by_id(self, graph: Dict, node_id: str) -> Dict:
        """Find node by ID."""
        for node in graph.get('nodes', []):
            if node.get('id') == node_id:
                return node
        return None
    
    def _infer_visibility(self, name: str) -> str:
        """Infer visibility from naming convention."""
        if name.startswith('__'):
            return 'private'
        elif name.startswith('_'):
            return 'protected'
        else:
            return 'public'
    
    def _extract_class_relationships(self, graph: Dict) -> List[Dict]:
        """Extract relationships between classes."""
        relationships = []
        
        for edge in graph.get('edges', []):
            edge_type = edge.get('type', '')
            
            if edge_type in ['inherits', 'extends', 'implements']:
                relationships.append({
                    'from': edge.get('source', ''),
                    'to': edge.get('target', ''),
                    'type': 'inherits'
                })
            elif edge_type in ['uses', 'calls', 'depends_on']:
                relationships.append({
                    'from': edge.get('source', ''),
                    'to': edge.get('target', ''),
                    'type': 'uses'
                })
            elif edge_type in ['has_a', 'contains']:
                relationships.append({
                    'from': edge.get('source', ''),
                    'to': edge.get('target', ''),
                    'type': 'has_a'
                })
        
        return relationships


class SequenceContextExtractor(BaseContextExtractor):
    """Extract context for Sequence Diagrams."""
    
    def extract(self, graph: Dict, profile: Dict, scenario: str = None) -> Dict[str, Any]:
        """Extract interaction flow for specific scenario."""
        
        if not scenario:
            scenario = "Main workflow execution"
        
        # Find entry point
        entry_point = self._find_entry_point(graph, profile)
        
        # Trace execution flow
        execution_flow = self._trace_execution(entry_point, graph, max_depth=8)
        
        # Extract actors/participants
        participants = self._extract_participants(execution_flow, graph)
        
        return {
            'diagram_type': 'sequence',
            'scenario': scenario,
            'entry_point': entry_point,
            'participants': participants,
            'execution_flow': execution_flow,
            'interaction_count': len(execution_flow)
        }
    
    def _find_entry_point(self, graph: Dict, profile: Dict) -> str:
        """Find the entry point for the scenario."""
        # Look for main functions, API endpoints, or event handlers
        for node in graph.get('nodes', []):
            name = node.get('name', '').lower()
            if name in ['main', '__main__', 'app', 'index', 'handler']:
                return node.get('id', '')
        
        # Fallback: return first function
        functions = self._get_nodes_by_type(graph, ['function'])
        return functions[0].get('id', '') if functions else ''
    
    def _trace_execution(self, start_node_id: str, graph: Dict, max_depth: int = 8) -> List[Dict]:
        """Trace execution flow from entry point."""
        flow = []
        visited = set()
        
        def trace_recursive(node_id: str, depth: int = 0):
            if depth >= max_depth or node_id in visited:
                return
            
            visited.add(node_id)
            node = self._find_node_by_id(graph, node_id)
            
            if not node:
                return
            
            # Find outgoing calls
            for edge in graph.get('edges', []):
                if edge.get('source') == node_id and edge.get('type') == 'calls':
                    target_id = edge.get('target')
                    target_node = self._find_node_by_id(graph, target_id)
                    
                    if target_node:
                        flow.append({
                            'from': node.get('name', ''),
                            'to': target_node.get('name', ''),
                            'action': edge.get('label', 'calls'),
                            'depth': depth
                        })
                        
                        trace_recursive(target_id, depth + 1)
        
        trace_recursive(start_node_id)
        return flow
    
    def _extract_participants(self, flow: List[Dict], graph: Dict) -> List[str]:
        """Extract unique participants from flow."""
        participants = set()
        for step in flow:
            participants.add(step.get('from', ''))
            participants.add(step.get('to', ''))
        return sorted(list(participants))


class ActivityContextExtractor(BaseContextExtractor):
    """Extract context for Activity Diagrams."""
    
    def extract(self, graph: Dict, profile: Dict, scenario: str = None) -> Dict[str, Any]:
        """Extract workflow and control flow."""
        
        if not scenario:
            scenario = "Primary business logic flow"
        
        # Find key functions
        key_functions = self._identify_key_functions(graph)
        
        # Extract control flow
        control_flow = self._extract_control_flow(key_functions, graph)
        
        # Identify decision points
        decisions = self._identify_decisions(graph)
        
        return {
            'diagram_type': 'activity',
            'scenario': scenario,
            'activities': key_functions[:15],  # Limit to 15
            'control_flow': control_flow,
            'decision_points': decisions,
            'total_activities': len(key_functions)
        }
    
    def _identify_key_functions(self, graph: Dict) -> List[Dict]:
        """Identify important functions for the workflow."""
        functions = self._get_nodes_by_type(graph, ['function'])
        
        # Sort by number of connections (centrality)
        scored_functions = []
        for func in functions:
            edges = self._get_edges_for_node(graph, func.get('id', ''))
            score = len(edges)
            scored_functions.append({
                'id': func.get('id', ''),
                'name': func.get('name', ''),
                'score': score
            })
        
        # Sort by score
        scored_functions.sort(key=lambda x: x['score'], reverse=True)
        
        return scored_functions
    
    def _extract_control_flow(self, functions: List[Dict], graph: Dict) -> List[Dict]:
        """Extract control flow between functions."""
        flow = []
        
        for func in functions[:15]:  # Limit
            for edge in graph.get('edges', []):
                if edge.get('source') == func.get('id') and edge.get('type') == 'calls':
                    target_node = self._find_node_by_id(graph, edge.get('target'))
                    if target_node:
                        flow.append({
                            'from': func.get('name', ''),
                            'to': target_node.get('name', ''),
                            'type': 'sequential'
                        })
        
        return flow
    
    def _identify_decisions(self, graph: Dict) -> List[Dict]:
        """Identify decision/branching points."""
        # In a real implementation, this would analyze AST for if/switch statements
        # For now, we infer from function names
        decisions = []
        
        for node in graph.get('nodes', []):
            name = node.get('name', '').lower()
            if any(keyword in name for keyword in ['validate', 'check', 'verify', 'is', 'has']):
                decisions.append({
                    'function': node.get('name', ''),
                    'type': 'decision'
                })
        
        return decisions[:10]  # Limit


class DataFlowContextExtractor(BaseContextExtractor):
    """Extract context for Data Flow Diagrams."""
    
    def extract(self, graph: Dict, profile: Dict, scenario: str = None) -> Dict[str, Any]:
        """Extract data flow and transformations."""
        
        # Identify data sources
        data_sources = self._identify_data_sources(graph, profile)
        
        # Identify data transformations (functions that process data)
        transformations = self._identify_transformations(graph)
        
        # Identify data sinks (outputs, storage)
        data_sinks = self._identify_data_sinks(graph, profile)
        
        # Extract data flow paths
        data_flows = self._extract_data_flows(graph)
        
        return {
            'diagram_type': 'data_flow',
            'data_sources': data_sources,
            'transformations': transformations[:15],  # Limit
            'data_sinks': data_sinks,
            'data_flows': data_flows,
            'has_database': profile.get('has_database', False),
            'has_api': profile.get('has_api', False)
        }
    
    def _identify_data_sources(self, graph: Dict, profile: Dict) -> List[str]:
        """Identify where data enters the system."""
        sources = []
        
        if profile.get('has_api'):
            sources.append('API Requests')
        if profile.get('has_database'):
            sources.append('Database')
        
        # Check for file I/O
        for node in graph.get('nodes', []):
            name = node.get('name', '').lower()
            if 'read' in name or 'load' in name or 'input' in name:
                sources.append('File System')
                break
        
        return sources if sources else ['User Input']
    
    def _identify_transformations(self, graph: Dict) -> List[Dict]:
        """Identify data transformation functions."""
        transformations = []
        
        functions = self._get_nodes_by_type(graph, ['function'])
        for func in functions:
            name = func.get('name', '').lower()
            # Look for processing keywords
            if any(kw in name for kw in ['process', 'transform', 'convert', 'parse', 'format', 'calculate']):
                transformations.append({
                    'name': func.get('name', ''),
                    'type': 'transformation'
                })
        
        return transformations
    
    def _identify_data_sinks(self, graph: Dict, profile: Dict) -> List[str]:
        """Identify where data exits the system."""
        sinks = []
        
        if profile.get('has_api'):
            sinks.append('API Response')
        if profile.get('has_database'):
            sinks.append('Database Storage')
        
        # Check for output operations
        for node in graph.get('nodes', []):
            name = node.get('name', '').lower()
            if 'write' in name or 'save' in name or 'output' in name:
                sinks.append('File System')
                break
        
        return sinks if sinks else ['Console Output']
    
    def _extract_data_flows(self, graph: Dict) -> List[Dict]:
        """Extract data flow between components."""
        flows = []
        
        for edge in graph.get('edges', []):
            if edge.get('type') in ['calls', 'uses', 'depends_on']:
                source_node = self._find_node_by_id(graph, edge.get('source'))
                target_node = self._find_node_by_id(graph, edge.get('target'))
                
                if source_node and target_node:
                    flows.append({
                        'from': source_node.get('name', ''),
                        'to': target_node.get('name', ''),
                        'data': 'data'
                    })
        
        return flows[:20]  # Limit


class C4ContextExtractor(BaseContextExtractor):
    """Extract context for C4 System Context Diagrams."""
    
    def extract(self, graph: Dict, profile: Dict, scenario: str = None) -> Dict[str, Any]:
        """Extract system context with users and external systems."""
        
        # Identify the system
        system_name = self._infer_system_name(graph)
        
        # Identify users/actors
        users = self._identify_users(profile)
        
        # Identify external systems
        external_systems = self._identify_external_systems(graph, profile)
        
        # Identify interactions
        interactions = self._identify_interactions(profile)
        
        return {
            'diagram_type': 'c4_context',
            'system_name': system_name,
            'users': users,
            'external_systems': external_systems,
            'interactions': interactions,
            'project_type': profile.get('project_type')
        }
    
    def _infer_system_name(self, graph: Dict) -> str:
        """Infer system name from graph."""
        # Try to find from file paths
        for node in graph.get('nodes', []):
            if node.get('type') == 'file':
                path = node.get('name', '')
                # Extract project name from path
                parts = path.split('/')
                if len(parts) > 1:
                    return parts[0].replace('_', ' ').title()
        
        return "System"
    
    def _identify_users(self, profile: Dict) -> List[str]:
        """Identify user types."""
        users = []
        project_type = profile.get('project_type', '')
        
        if project_type == 'web_api':
            users = ['API Client', 'Developer']
        elif project_type == 'web_app':
            users = ['End User', 'Administrator']
        elif project_type == 'cli_tool':
            users = ['Developer', 'DevOps Engineer']
        elif project_type == 'library':
            users = ['Developer']
        else:
            users = ['User']
        
        return users
    
    def _identify_external_systems(self, graph: Dict, profile: Dict) -> List[str]:
        """Identify external systems the project interacts with."""
        external = []
        
        # Get external dependencies
        deps = self._find_external_dependencies(graph)
        
        # Map to external systems
        system_mapping = {
            'django': 'Django Framework',
            'flask': 'Flask Framework',
            'fastapi': 'FastAPI Framework',
            'requests': 'External APIs',
            'sqlalchemy': 'Database',
            'pymongo': 'MongoDB',
            'redis': 'Redis Cache',
            'celery': 'Task Queue',
            'boto3': 'AWS Services',
            'stripe': 'Payment Gateway'
        }
        
        for dep in deps:
            if dep.lower() in system_mapping:
                external.append(system_mapping[dep.lower()])
        
        # Add database if detected
        if profile.get('has_database') and 'Database' not in external:
            external.append('Database')
        
        return list(set(external))  # Remove duplicates
    
    def _identify_interactions(self, profile: Dict) -> List[Dict]:
        """Identify interactions between system and external entities."""
        interactions = []
        
        if profile.get('has_api'):
            interactions.append({
                'from': 'API Client',
                'to': 'System',
                'description': 'Makes API requests'
            })
        
        if profile.get('has_database'):
            interactions.append({
                'from': 'System',
                'to': 'Database',
                'description': 'Reads/Writes data'
            })
        
        return interactions


class ERDiagramContextExtractor(BaseContextExtractor):
    """Extract context for Entity-Relationship Diagrams."""
    
    def extract(self, graph: Dict, profile: Dict, scenario: str = None) -> Dict[str, Any]:
        """Extract database entities and relationships."""
        
        # Find model/entity classes
        entities = self._identify_entities(graph)
        
        # Extract entity attributes
        entity_details = []
        for entity in entities:
            details = self._extract_entity_details(entity, graph)
            entity_details.append(details)
        
        # Extract relationships
        relationships = self._extract_entity_relationships(entities, graph)
        
        return {
            'diagram_type': 'er_diagram',
            'entities': entity_details,
            'relationships': relationships,
            'total_entities': len(entity_details)
        }
    
    def _identify_entities(self, graph: Dict) -> List[Dict]:
        """Identify database entity classes."""
        entities = []
        
        for node in graph.get('nodes', []):
            if node.get('type') == 'class':
                name = node.get('name', '').lower()
                # Look for model classes
                if 'model' in name or name.endswith('schema') or name.endswith('entity'):
                    entities.append(node)
        
        return entities
    
    def _extract_entity_details(self, entity: Dict, graph: Dict) -> Dict:
        """Extract attributes for an entity."""
        attributes = []
        
        # Find attributes from connected nodes
        for edge in graph.get('edges', []):
            if edge.get('source') == entity.get('id'):
                target_node = self._find_node_by_id(graph, edge.get('target'))
                if target_node and target_node.get('type') == 'variable':
                    attributes.append({
                        'name': target_node.get('name', ''),
                        'is_primary_key': 'id' in target_node.get('name', '').lower()
                    })
        
        return {
            'name': entity.get('name', ''),
            'attributes': attributes[:10]  # Limit
        }
    
    def _extract_entity_relationships(self, entities: List[Dict], graph: Dict) -> List[Dict]:
        """Extract relationships between entities."""
        relationships = []
        
        for edge in graph.get('edges', []):
            if edge.get('type') in ['has_a', 'references', 'foreign_key']:
                source_id = edge.get('source')
                target_id = edge.get('target')
                
                # Check if both are entities
                source_is_entity = any(e.get('id') == source_id for e in entities)
                target_is_entity = any(e.get('id') == target_id for e in entities)
                
                if source_is_entity and target_is_entity:
                    relationships.append({
                        'from': source_id,
                        'to': target_id,
                        'type': 'one_to_many'
                    })
        
        return relationships


class ContextExtractorFactory:
    """Factory for creating appropriate context extractors."""
    
    _extractors = {
        'component': ComponentContextExtractor,
        'class': ClassContextExtractor,
        'sequence': SequenceContextExtractor,
        'activity': ActivityContextExtractor,
        'data_flow': DataFlowContextExtractor,
        'c4_context': C4ContextExtractor,
        'c4_container': C4ContextExtractor,  # Reuse context extractor
        'er_diagram': ERDiagramContextExtractor,
        'package': ComponentContextExtractor,  # Similar to component
        'state': ActivityContextExtractor,  # Similar control flow
        'deployment': C4ContextExtractor  # Similar system view
    }
    
    @classmethod
    def get_extractor(cls, diagram_type: str) -> BaseContextExtractor:
        """Get appropriate extractor for diagram type."""
        extractor_class = cls._extractors.get(diagram_type, BaseContextExtractor)
        return extractor_class()
    
    @classmethod
    def extract_all(cls, selected_diagrams: List[Dict], graph: Dict, profile: Dict) -> Dict[str, Dict]:
        """Extract context for all selected diagrams."""
        contexts = {}
        
        for diagram in selected_diagrams:
            diagram_type = diagram.get('type_id', '')
            scenario = diagram.get('scenarios', [None])[0]
            
            extractor = cls.get_extractor(diagram_type)
            context = extractor.extract(graph, profile, scenario)
            contexts[diagram_type] = context
        
        return contexts
