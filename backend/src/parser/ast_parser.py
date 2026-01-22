"""
AST-based code parser using Tree-sitter
Extracts classes, functions, imports, and other metadata from source code
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
import tree_sitter_typescript as tstypescript
from tree_sitter import Language, Parser, Node

logger = logging.getLogger(__name__)

class CodeParser:
    """
    Multi-language code parser using Tree-sitter
    Supports Python and TypeScript/JavaScript
    """
    
    def __init__(self):
        self.parsers = {
            'python': Parser(Language(tspython.language())),
            'javascript': Parser(Language(tsjavascript.language())),
            'typescript': Parser(Language(tstypescript.language_typescript()))
        }
        logger.info('Initialized parsers for Python, JavaScript, and TypeScript')
        
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a single source code file
        
        Args:
            file_path: Path to the source file
            
        Returns:
            Dictionary containing extracted metadata:
            {
                'file_path': str,
                'language': str,
                'classes': List[Dict],
                'functions': List[Dict],
                'imports': List[str],
                'exports': List[str]
            }
        """
        logger.info(f'Parsing file: {file_path}')
        
        file_extension = Path(file_path).suffix
        language = self._detect_language(file_extension)
        
        if language not in self.parsers:
            logger.warning(f'Unsupported language: {language}')
            return {
                'file_path': file_path,
                'language': language,
                'classes': [],
                'functions': [],
                'imports': [],
                'exports': []
            }
        
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                source_code = f.read()
            
            # Parse with Tree-sitter
            parser = self.parsers[language]
            tree = parser.parse(source_code)
            root_node = tree.root_node
            
            # Extract metadata based on language
            if language == 'python':
                return self._parse_python(file_path, source_code, root_node)
            elif language in ['javascript', 'typescript']:
                return self._parse_javascript_typescript(file_path, source_code, root_node, language)
            
        except Exception as e:
            logger.error(f'Error parsing {file_path}: {e}', exc_info=True)
            return {
                'file_path': file_path,
                'language': language,
                'classes': [],
                'functions': [],
                'imports': [],
                'exports': [],
                'error': str(e)
            }
        
        return {
            'file_path': file_path,
            'language': language,
            'classes': [],
            'functions': [],
            'imports': [],
            'exports': []
        }
    
    def parse_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        Recursively parse all source files in a directory
        
        Args:
            directory_path: Path to the directory
            
        Returns:
            List of parsed file metadata
        """
        logger.info(f'Parsing directory: {directory_path}')
        
        parsed_files = []
        
        for root, dirs, files in os.walk(directory_path):
            # Skip common ignore patterns
            dirs[:] = [d for d in dirs if d not in [
                'node_modules', '__pycache__', '.git', 'venv', 'env', 'dist', 'build', 'out'
            ]]
            
            for file in files:
                if self._is_source_file(file):
                    file_path = os.path.join(root, file)
                    try:
                        parsed_data = self.parse_file(file_path)
                        parsed_files.append(parsed_data)
                    except Exception as e:
                        logger.warning(f'Failed to parse {file_path}: {e}')
        
        logger.info(f'Parsed {len(parsed_files)} files')
        return parsed_files
    
    def _parse_python(self, file_path: str, source_code: bytes, root_node: Node) -> Dict[str, Any]:
        """Parse Python-specific constructs"""
        classes = []
        functions = []
        imports = []
        
        def traverse(node: Node):
            """Recursively traverse AST nodes"""
            # Extract class definitions
            if node.type == 'class_definition':
                class_name_node = node.child_by_field_name('name')
                if class_name_node:
                    class_name = source_code[class_name_node.start_byte:class_name_node.end_byte].decode('utf-8')
                    # Get methods
                    methods = []
                    body = node.child_by_field_name('body')
                    if body:
                        for child in body.children:
                            if child.type == 'function_definition':
                                method_name_node = child.child_by_field_name('name')
                                if method_name_node:
                                    method_name = source_code[method_name_node.start_byte:method_name_node.end_byte].decode('utf-8')
                                    methods.append(method_name)
                    
                    classes.append({
                        'name': class_name,
                        'line': node.start_point[0] + 1,
                        'methods': methods
                    })
            
            # Extract function definitions (not inside classes)
            elif node.type == 'function_definition' and node.parent and node.parent.type != 'class_definition':
                func_name_node = node.child_by_field_name('name')
                if func_name_node:
                    func_name = source_code[func_name_node.start_byte:func_name_node.end_byte].decode('utf-8')
                    # Get parameters
                    params = []
                    parameters_node = node.child_by_field_name('parameters')
                    if parameters_node:
                        for param in parameters_node.children:
                            if param.type == 'identifier':
                                param_name = source_code[param.start_byte:param.end_byte].decode('utf-8')
                                params.append(param_name)
                    
                    functions.append({
                        'name': func_name,
                        'line': node.start_point[0] + 1,
                        'parameters': params
                    })
            
            # Extract imports
            elif node.type == 'import_statement':
                import_text = source_code[node.start_byte:node.end_byte].decode('utf-8')
                imports.append(import_text.strip())
            
            elif node.type == 'import_from_statement':
                import_text = source_code[node.start_byte:node.end_byte].decode('utf-8')
                imports.append(import_text.strip())
            
            # Traverse children
            for child in node.children:
                traverse(child)
        
        traverse(root_node)
        
        return {
            'file_path': file_path,
            'language': 'python',
            'classes': classes,
            'functions': functions,
            'imports': imports,
            'exports': []
        }
    
    def _parse_javascript_typescript(self, file_path: str, source_code: bytes, root_node: Node, language: str) -> Dict[str, Any]:
        """Parse JavaScript/TypeScript-specific constructs"""
        classes = []
        functions = []
        imports = []
        exports = []
        
        def traverse(node: Node):
            """Recursively traverse AST nodes"""
            # Extract class declarations
            if node.type == 'class_declaration':
                class_name_node = node.child_by_field_name('name')
                if class_name_node:
                    class_name = source_code[class_name_node.start_byte:class_name_node.end_byte].decode('utf-8')
                    # Get methods
                    methods = []
                    body = node.child_by_field_name('body')
                    if body:
                        for child in body.children:
                            if child.type == 'method_definition':
                                method_name_node = child.child_by_field_name('name')
                                if method_name_node:
                                    method_name = source_code[method_name_node.start_byte:method_name_node.end_byte].decode('utf-8')
                                    methods.append(method_name)
                    
                    classes.append({
                        'name': class_name,
                        'line': node.start_point[0] + 1,
                        'methods': methods
                    })
            
            # Extract function declarations
            elif node.type in ['function_declaration', 'arrow_function']:
                func_name_node = node.child_by_field_name('name')
                if func_name_node:
                    func_name = source_code[func_name_node.start_byte:func_name_node.end_byte].decode('utf-8')
                    functions.append({
                        'name': func_name,
                        'line': node.start_point[0] + 1
                    })
            
            # Extract imports
            elif node.type == 'import_statement':
                import_text = source_code[node.start_byte:node.end_byte].decode('utf-8')
                imports.append(import_text.strip())
            
            # Extract exports
            elif node.type in ['export_statement', 'export_default_declaration']:
                export_text = source_code[node.start_byte:node.end_byte].decode('utf-8')
                exports.append(export_text.strip())
            
            # Traverse children
            for child in node.children:
                traverse(child)
        
        traverse(root_node)
        
        return {
            'file_path': file_path,
            'language': language,
            'classes': classes,
            'functions': functions,
            'imports': imports,
            'exports': exports
        }
        
        parsed_files = []
        
        for root, dirs, files in os.walk(directory_path):
            # Skip common ignore patterns
            dirs[:] = [d for d in dirs if d not in [
                'node_modules', '__pycache__', '.git', 'venv', 'env', 'dist', 'build'
            ]]
            
            for file in files:
                if self._is_source_file(file):
                    file_path = os.path.join(root, file)
                    try:
                        parsed_data = self.parse_file(file_path)
                        parsed_files.append(parsed_data)
                    except Exception as e:
                        logger.warning(f'Failed to parse {file_path}: {e}')
        
        logger.info(f'Parsed {len(parsed_files)} files')
        return parsed_files
    
    def _detect_language(self, file_extension: str) -> str:
        """Detect programming language from file extension"""
        extension_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript'
        }
        return extension_map.get(file_extension.lower(), 'unknown')
    
    def _is_source_file(self, filename: str) -> bool:
        """Check if a file is a source code file"""
        source_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx'}
        return Path(filename).suffix.lower() in source_extensions
