"""
Unit tests for the parser module
"""

import unittest
import os
import sys
import tempfile
from pathlib import Path

# Add backend/src to sys.path
BACKEND_SRC = Path(__file__).resolve().parent.parent / 'backend' / 'src'
if str(BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(BACKEND_SRC))

from parser.ast_parser import CodeParser
from parser.dependency_graph import DependencyGraphBuilder


class TestCodeParser(unittest.TestCase):
    """Test cases for CodeParser"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = CodeParser()
        self.temp_dir = tempfile.mkdtemp()
    
    def test_detect_language_python(self):
        """Test Python language detection"""
        lang = self.parser._detect_language('.py')
        self.assertEqual(lang, 'python')
    
    def test_detect_language_javascript(self):
        """Test JavaScript language detection"""
        lang = self.parser._detect_language('.js')
        self.assertEqual(lang, 'javascript')
    
    def test_detect_language_typescript(self):
        """Test TypeScript language detection"""
        lang = self.parser._detect_language('.ts')
        self.assertEqual(lang, 'typescript')
    
    def test_is_source_file(self):
        """Test source file detection"""
        self.assertTrue(self.parser._is_source_file('test.py'))
        self.assertTrue(self.parser._is_source_file('test.js'))
        self.assertTrue(self.parser._is_source_file('test.ts'))
        self.assertFalse(self.parser._is_source_file('test.txt'))
        self.assertFalse(self.parser._is_source_file('test.md'))
    
    def test_parse_file_structure(self):
        """Test that parse_file returns correct structure"""
        # Create a temporary Python file
        test_file = os.path.join(self.temp_dir, 'test.py')
        with open(test_file, 'w') as f:
            f.write('def test_function():\n    pass\n')
        
        result = self.parser.parse_file(test_file)
        
        self.assertIn('file_path', result)
        self.assertIn('language', result)
        self.assertIn('classes', result)
        self.assertIn('functions', result)
        self.assertIn('imports', result)
        self.assertEqual(result['language'], 'python')
    
    def test_parse_directory_ignores_patterns(self):
        """Test that parse_directory ignores common patterns"""
        # Create directory structure with ignored folders
        os.makedirs(os.path.join(self.temp_dir, 'node_modules'))
        os.makedirs(os.path.join(self.temp_dir, '__pycache__'))
        os.makedirs(os.path.join(self.temp_dir, 'src'))
        
        # Create source files
        with open(os.path.join(self.temp_dir, 'src', 'test.py'), 'w') as f:
            f.write('def test():\n    pass\n')
        
        with open(os.path.join(self.temp_dir, 'node_modules', 'test.js'), 'w') as f:
            f.write('console.log("test");\n')
        
        result = self.parser.parse_directory(self.temp_dir)
        
        # Should only find the file in src/, not in node_modules
        self.assertEqual(len(result), 1)
        self.assertIn('src', result[0]['file_path'])
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir)


class TestDependencyGraphBuilder(unittest.TestCase):
    """Test cases for DependencyGraphBuilder"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.builder = DependencyGraphBuilder()
    
    def test_build_graph_structure(self):
        """Test that build_graph returns correct structure"""
        parsed_files = [
            {
                'file_path': 'test.py',
                'language': 'python',
                'classes': [{'name': 'TestClass'}],
                'functions': [{'name': 'test_function'}],
                'imports': []
            }
        ]
        
        result = self.builder.build_graph(parsed_files)
        
        self.assertIn('nodes', result)
        self.assertIn('edges', result)
        self.assertIn('metadata', result)
        self.assertIsInstance(result['nodes'], list)
        self.assertIsInstance(result['edges'], list)
    
    def test_graph_metadata(self):
        """Test that graph metadata is calculated correctly"""
        parsed_files = [
            {
                'file_path': 'test1.py',
                'classes': [{'name': 'Class1'}, {'name': 'Class2'}],
                'functions': [{'name': 'func1'}],
                'imports': []
            },
            {
                'file_path': 'test2.py',
                'classes': [{'name': 'Class3'}],
                'functions': [{'name': 'func2'}, {'name': 'func3'}],
                'imports': []
            }
        ]
        
        result = self.builder.build_graph(parsed_files)
        
        metadata = result['metadata']
        self.assertEqual(metadata['total_files'], 2)
        self.assertEqual(metadata['total_classes'], 3)
        self.assertEqual(metadata['total_functions'], 3)
    
    def test_node_structure(self):
        """Test that nodes have correct structure"""
        parsed_files = [
            {
                'file_path': 'test.py',
                'classes': [{'name': 'TestClass'}],
                'functions': [],
                'imports': []
            }
        ]
        
        result = self.builder.build_graph(parsed_files)
        nodes = result['nodes']
        
        # Should have file node and class node
        self.assertGreaterEqual(len(nodes), 2)
        
        # Check node structure
        for node in nodes:
            self.assertIn('id', node)
            self.assertIn('type', node)
            self.assertIn('name', node)
            self.assertIn('file', node)
    
    def test_edge_structure(self):
        """Test that edges have correct structure"""
        parsed_files = [
            {
                'file_path': 'test.py',
                'classes': [{'name': 'TestClass'}],
                'functions': [],
                'imports': []
            }
        ]
        
        result = self.builder.build_graph(parsed_files)
        edges = result['edges']
        
        # Should have at least one edge (file -> class)
        self.assertGreater(len(edges), 0)
        
        # Check edge structure
        for edge in edges:
            self.assertIn('from', edge)
            self.assertIn('to', edge)
            self.assertIn('type', edge)


if __name__ == '__main__':
    unittest.main()
