"""
AST-based code parser using Tree-sitter
Extracts classes, functions, imports, and other metadata from source code
Supports: Python, JavaScript, TypeScript, PHP, Java, C, C++, C#, Go, Rust, Ruby
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from tree_sitter import Parser, Node
import tree_sitter_python as tspython
import tree_sitter_javascript as tsjavascript
import tree_sitter_typescript as tstypescript
import tree_sitter_php as tsphp
import tree_sitter_java as tsjava
import tree_sitter_c as tsc
import tree_sitter_cpp as tscpp
import tree_sitter_c_sharp as tscsharp
import tree_sitter_go as tsgo
import tree_sitter_rust as tsrust
import tree_sitter_ruby as tsruby

logger = logging.getLogger(__name__)

class CodeParser:
    """
    Multi-language code parser using Tree-sitter
    Supports 11 programming languages by default
    """
    
    def __init__(self):
        # Initialize all parsers - all languages supported by default
        # Tree-sitter 0.22+ uses parser.set_language() instead of Language wrapper
        self.parsers = {}
        
        # Python
        python_parser = Parser()
        python_parser.set_language(tspython.language())
        self.parsers['python'] = python_parser
        
        # JavaScript
        js_parser = Parser()
        js_parser.set_language(tsjavascript.language())
        self.parsers['javascript'] = js_parser
        
        # TypeScript
        ts_parser = Parser()
        ts_parser.set_language(tstypescript.language_typescript())
        self.parsers['typescript'] = ts_parser
        
        # PHP
        php_parser = Parser()
        php_parser.set_language(tsphp.language_php())
        self.parsers['php'] = php_parser
        
        # Java
        java_parser = Parser()
        java_parser.set_language(tsjava.language())
        self.parsers['java'] = java_parser
        
        # C
        c_parser = Parser()
        c_parser.set_language(tsc.language())
        self.parsers['c'] = c_parser
        
        # C++
        cpp_parser = Parser()
        cpp_parser.set_language(tscpp.language())
        self.parsers['cpp'] = cpp_parser
        
        # C#
        csharp_parser = Parser()
        csharp_parser.set_language(tscsharp.language())
        self.parsers['csharp'] = csharp_parser
        
        # Go
        go_parser = Parser()
        go_parser.set_language(tsgo.language())
        self.parsers['go'] = go_parser
        
        # Rust
        rust_parser = Parser()
        rust_parser.set_language(tsrust.language())
        self.parsers['rust'] = rust_parser
        
        # Ruby
        ruby_parser = Parser()
        ruby_parser.set_language(tsruby.language())
        self.parsers['ruby'] = ruby_parser
        
        logger.info('Initialized parsers for: Python, JavaScript, TypeScript, PHP, Java, C, C++, C#, Go, Rust, Ruby')

        
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
            elif language == 'php':
                return self._parse_php(file_path, source_code, root_node)
            elif language == 'java':
                return self._parse_java(file_path, source_code, root_node)
            elif language in ['c', 'cpp']:
                return self._parse_c_cpp(file_path, source_code, root_node, language)
            elif language == 'csharp':
                return self._parse_csharp(file_path, source_code, root_node)
            elif language == 'go':
                return self._parse_go(file_path, source_code, root_node)
            elif language == 'rust':
                return self._parse_rust(file_path, source_code, root_node)
            elif language == 'ruby':
                return self._parse_ruby(file_path, source_code, root_node)
            else:
                # Fallback for languages with parsers but no specific handler
                return self._parse_generic(file_path, source_code, root_node, language)
            
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
    
    def _parse_php(self, file_path: str, source_code: bytes, root_node: Node) -> Dict[str, Any]:
        """Parse PHP-specific constructs"""
        classes = []
        functions = []
        imports = []
        
        def traverse(node: Node):
            """Recursively traverse AST nodes"""
            # Extract class declarations
            if node.type == 'class_declaration':
                name_node = node.child_by_field_name('name')
                if name_node:
                    class_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    # Get methods
                    methods = []
                    body = node.child_by_field_name('declaration_list')
                    if body:
                        for child in body.children:
                            if child.type == 'method_declaration':
                                method_name_node = child.child_by_field_name('name')
                                if method_name_node:
                                    method_name = source_code[method_name_node.start_byte:method_name_node.end_byte].decode('utf-8')
                                    methods.append(method_name)
                    
                    classes.append({
                        'name': class_name,
                        'line': node.start_point[0] + 1,
                        'methods': methods
                    })
            
            # Extract function definitions
            elif node.type == 'function_definition':
                name_node = node.child_by_field_name('name')
                if name_node:
                    function_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    # Get parameters
                    params = []
                    parameters_node = node.child_by_field_name('parameters')
                    if parameters_node:
                        for child in parameters_node.children:
                            if child.type in ['simple_parameter', 'property_promotion_parameter']:
                                param_name_node = child.child_by_field_name('name')
                                if param_name_node:
                                    param_name = source_code[param_name_node.start_byte:param_name_node.end_byte].decode('utf-8')
                                    params.append(param_name)
                    
                    functions.append({
                        'name': function_name,
                        'line': node.start_point[0] + 1,
                        'params': params
                    })
            
            # Extract namespace imports (use/require statements)
            elif node.type in ['namespace_use_declaration', 'namespace_aliasing_clause']:
                import_text = source_code[node.start_byte:node.end_byte].decode('utf-8')
                imports.append(import_text.strip())
            
            # Traverse children
            for child in node.children:
                traverse(child)
        
        traverse(root_node)
        
        return {
            'file_path': file_path,
            'language': 'php',
            'classes': classes,
            'functions': functions,
            'imports': imports,
            'exports': []  # PHP doesn't have ES6-style exports
        }
    
    def _parse_java(self, file_path: str, source_code: bytes, root_node: Node) -> Dict[str, Any]:
        """Parse Java-specific constructs"""
        classes = []
        functions = []
        imports = []
        
        def traverse(node: Node):
            if node.type == 'class_declaration':
                name_node = node.child_by_field_name('name')
                if name_node:
                    class_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    methods = []
                    body = node.child_by_field_name('body')
                    if body:
                        for child in body.children:
                            if child.type == 'method_declaration':
                                method_name_node = child.child_by_field_name('name')
                                if method_name_node:
                                    method_name = source_code[method_name_node.start_byte:method_name_node.end_byte].decode('utf-8')
                                    methods.append(method_name)
                    classes.append({'name': class_name, 'line': node.start_point[0] + 1, 'methods': methods})
            
            elif node.type == 'import_declaration':
                import_text = source_code[node.start_byte:node.end_byte].decode('utf-8')
                imports.append(import_text.strip())
            
            for child in node.children:
                traverse(child)
        
        traverse(root_node)
        return {'file_path': file_path, 'language': 'java', 'classes': classes, 'functions': functions, 'imports': imports, 'exports': []}
    
    def _parse_c_cpp(self, file_path: str, source_code: bytes, root_node: Node, language: str) -> Dict[str, Any]:
        """Parse C/C++-specific constructs"""
        classes = []
        functions = []
        
        def traverse(node: Node):
            if node.type in ['class_specifier', 'struct_specifier']:
                name_node = node.child_by_field_name('name')
                if name_node:
                    class_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    classes.append({'name': class_name, 'line': node.start_point[0] + 1, 'methods': []})
            
            elif node.type == 'function_definition':
                declarator = node.child_by_field_name('declarator')
                if declarator:
                    if declarator.type == 'function_declarator':
                        name_node = declarator.child_by_field_name('declarator')
                        if name_node:
                            func_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                            functions.append({'name': func_name, 'line': node.start_point[0] + 1})
            
            for child in node.children:
                traverse(child)
        
        traverse(root_node)
        return {'file_path': file_path, 'language': language, 'classes': classes, 'functions': functions, 'imports': [], 'exports': []}
    
    def _parse_csharp(self, file_path: str, source_code: bytes, root_node: Node) -> Dict[str, Any]:
        """Parse C#-specific constructs"""
        classes = []
        functions = []
        imports = []
        
        def traverse(node: Node):
            if node.type == 'class_declaration':
                name_node = node.child_by_field_name('name')
                if name_node:
                    class_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    methods = []
                    body = node.child_by_field_name('body')
                    if body:
                        for child in body.children:
                            if child.type == 'method_declaration':
                                method_name_node = child.child_by_field_name('name')
                                if method_name_node:
                                    method_name = source_code[method_name_node.start_byte:method_name_node.end_byte].decode('utf-8')
                                    methods.append(method_name)
                    classes.append({'name': class_name, 'line': node.start_point[0] + 1, 'methods': methods})
            
            elif node.type == 'using_directive':
                import_text = source_code[node.start_byte:node.end_byte].decode('utf-8')
                imports.append(import_text.strip())
            
            for child in node.children:
                traverse(child)
        
        traverse(root_node)
        return {'file_path': file_path, 'language': 'csharp', 'classes': classes, 'functions': functions, 'imports': imports, 'exports': []}
    
    def _parse_go(self, file_path: str, source_code: bytes, root_node: Node) -> Dict[str, Any]:
        """Parse Go-specific constructs"""
        classes = []  # Go doesn't have classes, but has structs
        functions = []
        imports = []
        
        def traverse(node: Node):
            if node.type == 'type_declaration':
                # Look for struct definitions
                for child in node.children:
                    if child.type == 'type_spec':
                        name_node = child.child_by_field_name('name')
                        if name_node:
                            struct_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                            classes.append({'name': struct_name, 'line': node.start_point[0] + 1, 'methods': []})
            
            elif node.type == 'function_declaration':
                name_node = node.child_by_field_name('name')
                if name_node:
                    func_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    functions.append({'name': func_name, 'line': node.start_point[0] + 1})
            
            elif node.type == 'import_declaration':
                import_text = source_code[node.start_byte:node.end_byte].decode('utf-8')
                imports.append(import_text.strip())
            
            for child in node.children:
                traverse(child)
        
        traverse(root_node)
        return {'file_path': file_path, 'language': 'go', 'classes': classes, 'functions': functions, 'imports': imports, 'exports': []}
    
    def _parse_rust(self, file_path: str, source_code: bytes, root_node: Node) -> Dict[str, Any]:
        """Parse Rust-specific constructs"""
        classes = []  # Rust has structs, enums, traits
        functions = []
        imports = []
        
        def traverse(node: Node):
            if node.type in ['struct_item', 'enum_item', 'trait_item']:
                name_node = node.child_by_field_name('name')
                if name_node:
                    item_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    classes.append({'name': item_name, 'line': node.start_point[0] + 1, 'methods': []})
            
            elif node.type == 'function_item':
                name_node = node.child_by_field_name('name')
                if name_node:
                    func_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    functions.append({'name': func_name, 'line': node.start_point[0] + 1})
            
            elif node.type == 'use_declaration':
                import_text = source_code[node.start_byte:node.end_byte].decode('utf-8')
                imports.append(import_text.strip())
            
            for child in node.children:
                traverse(child)
        
        traverse(root_node)
        return {'file_path': file_path, 'language': 'rust', 'classes': classes, 'functions': functions, 'imports': imports, 'exports': []}
    
    def _parse_ruby(self, file_path: str, source_code: bytes, root_node: Node) -> Dict[str, Any]:
        """Parse Ruby-specific constructs"""
        classes = []
        functions = []
        imports = []
        
        def traverse(node: Node):
            if node.type == 'class':
                name_node = node.child_by_field_name('name')
                if name_node:
                    class_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    methods = []
                    for child in node.children:
                        if child.type == 'method':
                            method_name_node = child.child_by_field_name('name')
                            if method_name_node:
                                method_name = source_code[method_name_node.start_byte:method_name_node.end_byte].decode('utf-8')
                                methods.append(method_name)
                    classes.append({'name': class_name, 'line': node.start_point[0] + 1, 'methods': methods})
            
            elif node.type == 'method':
                name_node = node.child_by_field_name('name')
                if name_node:
                    func_name = source_code[name_node.start_byte:name_node.end_byte].decode('utf-8')
                    functions.append({'name': func_name, 'line': node.start_point[0] + 1})
            
            elif node.type in ['call', 'require']:
                call_text = source_code[node.start_byte:node.end_byte].decode('utf-8')
                if call_text.startswith('require'):
                    imports.append(call_text.strip())
            
            for child in node.children:
                traverse(child)
        
        traverse(root_node)
        return {'file_path': file_path, 'language': 'ruby', 'classes': classes, 'functions': functions, 'imports': imports, 'exports': []}
    
    def _parse_generic(self, file_path: str, source_code: bytes, root_node: Node, language: str) -> Dict[str, Any]:
        """Generic parser for languages without specific handlers"""
        logger.info(f'Using generic parser for {language}')
        return {
            'file_path': file_path,
            'language': language,
            'classes': [],
            'functions': [],
            'imports': [],
            'exports': [],
            'note': 'Parsed with generic handler - limited metadata extraction'
        }
    
    def parse_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """
        Parse all source files in a directory recursively
        
        Args:
            directory_path: Root directory to parse
            
        Returns:
            List of parsed file metadata dictionaries
        """
        logger.info(f'Parsing directory: {directory_path}')
        
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
            # Python
            '.py': 'python',
            '.pyw': 'python',
            
            # JavaScript / TypeScript
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.mjs': 'javascript',
            '.cjs': 'javascript',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            
            # PHP
            '.php': 'php',
            '.phtml': 'php',
            '.php3': 'php',
            '.php4': 'php',
            '.php5': 'php',
            
            # Java
            '.java': 'java',
            
            # C/C++
            '.c': 'c',
            '.h': 'c',
            '.cpp': 'cpp',
            '.cc': 'cpp',
            '.cxx': 'cpp',
            '.c++': 'cpp',
            '.hpp': 'cpp',
            '.hh': 'cpp',
            '.hxx': 'cpp',
            '.h++': 'cpp',
            
            # C#
            '.cs': 'csharp',
            
            # Go
            '.go': 'go',
            
            # Rust
            '.rs': 'rust',
            
            # Ruby
            '.rb': 'ruby',
            '.rake': 'ruby',
        }
        return extension_map.get(file_extension.lower(), 'unknown')
    
    def _is_source_file(self, filename: str) -> bool:
        """Check if a file is a source code file"""
        source_extensions = {
            # Python
            '.py', '.pyw',
            # JavaScript / TypeScript
            '.js', '.jsx', '.mjs', '.cjs', '.ts', '.tsx',
            # PHP
            '.php', '.phtml', '.php3', '.php4', '.php5',
            # Java
            '.java',
            # C/C++
            '.c', '.h', '.cpp', '.cc', '.cxx', '.c++', '.hpp', '.hh', '.hxx', '.h++',
            # C#
            '.cs',
            # Go
            '.go',
            # Rust
            '.rs',
            # Ruby
            '.rb', '.rake'
        }
        return Path(filename).suffix.lower() in source_extensions
