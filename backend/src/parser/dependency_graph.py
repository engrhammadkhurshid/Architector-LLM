"""
Dependency graph builder
Constructs a structured graph of code dependencies for RAG context
"""

import logging
from typing import Dict, List, Any, Set

logger = logging.getLogger(__name__)

class DependencyGraphBuilder:
    """
    Builds a dependency graph from parsed code metadata
    """
    
    def __init__(self):
        self.graph = {
            'nodes': [],
            'edges': []
        }
    
    def build_graph(self, parsed_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Build a dependency graph from parsed file data
        
        Args:
            parsed_files: List of parsed file metadata from CodeParser
            
        Returns:
            Structured dependency graph:
            {
                'nodes': [
                    {'id': str, 'type': str, 'name': str, 'file': str, 'details': dict},
                    ...
                ],
                'edges': [
                    {'from': str, 'to': str, 'type': str},
                    ...
                ],
                'metadata': {
                    'total_files': int,
                    'total_classes': int,
                    'total_functions': int,
                    'total_imports': int
                }
            }
        """
        logger.info(f'Building dependency graph from {len(parsed_files)} files')
        
        nodes = []
        edges = []
        file_imports_map = {}  # Track imports for dependency edges
        
        for file_data in parsed_files:
            file_path = file_data['file_path']
            
            # Add file node with details
            nodes.append({
                'id': file_path,
                'type': 'file',
                'name': file_path.split('/')[-1],
                'file': file_path,
                'details': {
                    'language': file_data.get('language', 'unknown'),
                    'imports_count': len(file_data.get('imports', [])),
                    'classes_count': len(file_data.get('classes', [])),
                    'functions_count': len(file_data.get('functions', []))
                }
            })
            
            # Store imports for later processing
            file_imports_map[file_path] = file_data.get('imports', [])
            
            # Add class nodes with details
            for cls in file_data.get('classes', []):
                class_name = cls.get('name', 'Unknown')
                class_id = f"{file_path}::{class_name}"
                nodes.append({
                    'id': class_id,
                    'type': 'class',
                    'name': class_name,
                    'file': file_path,
                    'details': {
                        'line': cls.get('line', 0),
                        'methods': cls.get('methods', []),
                        'methods_count': len(cls.get('methods', []))
                    }
                })
                
                # Add edge from file to class
                edges.append({
                    'from': file_path,
                    'to': class_id,
                    'type': 'contains'
                })
                
                # Add method nodes
                for method_name in cls.get('methods', []):
                    method_id = f"{class_id}.{method_name}"
                    nodes.append({
                        'id': method_id,
                        'type': 'method',
                        'name': method_name,
                        'file': file_path,
                        'details': {
                            'parent_class': class_name
                        }
                    })
                    edges.append({
                        'from': class_id,
                        'to': method_id,
                        'type': 'contains'
                    })
            
            # Add function nodes with details
            for func in file_data.get('functions', []):
                func_name = func.get('name', 'Unknown')
                func_id = f"{file_path}::{func_name}"
                nodes.append({
                    'id': func_id,
                    'type': 'function',
                    'name': func_name,
                    'file': file_path,
                    'details': {
                        'line': func.get('line', 0),
                        'parameters': func.get('parameters', []),
                        'parameters_count': len(func.get('parameters', []))
                    }
                })
                
                edges.append({
                    'from': file_path,
                    'to': func_id,
                    'type': 'contains'
                })
        
        # Build import dependency edges
        self._build_import_edges(parsed_files, file_imports_map, edges)
        
        graph = {
            'nodes': nodes,
            'edges': edges,
            'metadata': {
                'total_files': len(parsed_files),
                'total_classes': sum(len(f.get('classes', [])) for f in parsed_files),
                'total_functions': sum(len(f.get('functions', [])) for f in parsed_files),
                'total_imports': sum(len(f.get('imports', [])) for f in parsed_files),
                'total_nodes': len(nodes),
                'total_edges': len(edges)
            }
        }
        
        logger.info(f'Graph built: {len(nodes)} nodes, {len(edges)} edges')
        return graph
    
    def _build_import_edges(self, parsed_files: List[Dict[str, Any]], file_imports_map: Dict, edges: List[Dict]) -> None:
        """Build edges based on import statements"""
        # Create a mapping of file names to full paths for matching imports
        file_name_to_path = {}
        for file_data in parsed_files:
            file_path = file_data['file_path']
            file_name = file_path.split('/')[-1].replace('.py', '').replace('.js', '').replace('.ts', '')
            file_name_to_path[file_name] = file_path
        
        # Analyze imports and create dependency edges
        for file_path, imports in file_imports_map.items():
            for import_statement in imports:
                # Try to find which file is being imported
                for imported_name, imported_path in file_name_to_path.items():
                    if imported_name in import_statement and imported_path != file_path:
                        edges.append({
                            'from': file_path,
                            'to': imported_path,
                            'type': 'imports'
                        })
                        logger.debug(f'{file_path} imports {imported_path}')
                        break
    
    def export_to_json(self, output_path: str) -> None:
        """Export the graph to a JSON file"""
        import json
        with open(output_path, 'w') as f:
            json.dump(self.graph, f, indent=2)
        logger.info(f'Graph exported to {output_path}')
