"""
Codebase Analyzer
Analyzes codebase to detect features, frameworks, patterns, and complexity
Used for intelligent diagram selection
"""

import os
import re
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class CodebaseAnalyzer:
    """
    Analyzes codebase characteristics to inform diagram generation decisions
    """
    
    def __init__(self):
        self.framework_patterns = {
            # Python frameworks
            'django': ['django', 'settings.py', 'manage.py', 'wsgi.py'],
            'flask': ['flask', 'Flask(', 'app.run('],
            'fastapi': ['fastapi', 'FastAPI(', '@app.get', '@app.post'],
            'sqlalchemy': ['sqlalchemy', 'declarative_base', 'Column', 'relationship'],
            'pytest': ['pytest', 'test_', 'conftest.py'],
            
            # JavaScript/TypeScript frameworks
            'react': ['react', 'React', 'useState', 'useEffect', 'jsx'],
            'vue': ['vue', 'Vue', '.vue', 'v-if', 'v-for'],
            'express': ['express', 'Express(', 'app.listen'],
            'nestjs': ['@nestjs', 'NestFactory', '@Controller', '@Injectable'],
            'angular': ['@angular', '@Component', '@NgModule'],
            
            # Testing
            'jest': ['jest', 'describe(', 'it(', 'test('],
            'mocha': ['mocha', 'describe(', 'it('],
        }
        
        self.architectural_patterns = {
            'mvc': ['models/', 'views/', 'controllers/'],
            'mvvm': ['viewmodels/', 'models/', 'views/'],
            'repository': ['repositories/', 'repository.py', 'repository.ts'],
            'service_layer': ['services/', 'service.py', 'service.ts'],
            'microservices': ['docker-compose', 'kubernetes/', 'k8s/'],
        }
    
    def analyze(self, codebase_path: str, parsed_files: List[Dict], dependency_graph: Dict) -> Dict[str, Any]:
        """
        Comprehensive codebase analysis
        
        Args:
            codebase_path: Root path of codebase
            parsed_files: Output from CodeParser
            dependency_graph: Output from DependencyGraphBuilder
            
        Returns:
            CodebaseProfile dictionary with detailed characteristics
        """
        logger.info(f'Analyzing codebase: {codebase_path}')
        
        profile = {
            'path': codebase_path,
            'language': self._detect_primary_language(parsed_files),
            'languages': self._detect_languages(parsed_files),
            'features': self._detect_language_features(parsed_files),
            'frameworks': self._detect_frameworks(codebase_path, parsed_files),
            'architectural_patterns': self._detect_architectural_patterns(codebase_path),
            'has_database': self._has_database_models(parsed_files),
            'has_api': self._has_api_endpoints(parsed_files),
            'has_async': self._has_async_code(parsed_files),
            'has_tests': self._has_tests(codebase_path),
            'has_deployment_configs': self._has_deployment_configs(codebase_path),
            'complexity': self._calculate_complexity(parsed_files, dependency_graph),
            'project_type': None,  # Will be determined
            'metadata': dependency_graph.get('metadata', {}),
        }
        
        # Determine project type
        profile['project_type'] = self._determine_project_type(profile)
        
        logger.info(f'Analysis complete: {profile["project_type"]} project with {len(profile["frameworks"])} frameworks')
        return profile
    
    def _detect_primary_language(self, parsed_files: List[Dict]) -> str:
        """Detect the primary programming language"""
        language_counts = {}
        
        for file_info in parsed_files:
            lang = file_info.get('language', 'unknown')
            language_counts[lang] = language_counts.get(lang, 0) + 1
        
        if not language_counts:
            return 'unknown'
        
        primary_lang = max(language_counts.items(), key=lambda x: x[1])[0]
        return primary_lang
    
    def _detect_languages(self, parsed_files: List[Dict]) -> List[str]:
        """Detect all languages used"""
        languages = set()
        
        for file_info in parsed_files:
            lang = file_info.get('language')
            if lang:
                languages.add(lang)
        
        return sorted(list(languages))
    
    def _detect_language_features(self, parsed_files: List[Dict]) -> List[str]:
        """Detect language features (OOP, async, type hints, etc.)"""
        features = set()
        
        for file_info in parsed_files:
            # Check for OOP
            if file_info.get('classes'):
                features.add('oop')
            
            # Check for async
            content = file_info.get('content', '')
            if 'async' in content or 'await' in content:
                features.add('async')
            
            # Check for type hints (Python)
            if file_info.get('language') == 'python':
                if '->' in content or ': ' in content:
                    features.add('type_hints')
            
            # Check for generics (TypeScript/Java)
            if '<' in content and '>' in content:
                features.add('generics')
            
            # Check for decorators
            if '@' in content:
                features.add('decorators')
        
        return sorted(list(features))
    
    def _detect_frameworks(self, codebase_path: str, parsed_files: List[Dict]) -> List[str]:
        """Detect frameworks used in the project"""
        detected_frameworks = set()
        
        # Check file contents
        for file_info in parsed_files:
            content = file_info.get('content', '').lower()
            
            for framework, patterns in self.framework_patterns.items():
                for pattern in patterns:
                    if pattern.lower() in content:
                        detected_frameworks.add(framework)
                        break
        
        # Check for common framework files
        for framework, patterns in self.framework_patterns.items():
            for pattern in patterns:
                if pattern.endswith('.py') or pattern.endswith('.ts'):
                    if os.path.exists(os.path.join(codebase_path, pattern)):
                        detected_frameworks.add(framework)
        
        return sorted(list(detected_frameworks))
    
    def _detect_architectural_patterns(self, codebase_path: str) -> List[str]:
        """Detect architectural patterns used"""
        detected_patterns = set()
        
        for pattern, indicators in self.architectural_patterns.items():
            for indicator in indicators:
                search_path = os.path.join(codebase_path, indicator)
                if os.path.exists(search_path):
                    detected_patterns.add(pattern)
                    break
        
        return sorted(list(detected_patterns))
    
    def _has_database_models(self, parsed_files: List[Dict]) -> bool:
        """Check if project has database models"""
        for file_info in parsed_files:
            content = file_info.get('content', '').lower()
            
            # Look for ORM patterns
            if any(pattern in content for pattern in [
                'models.model', 'declarative_base', 'db.model',
                '@entity', 'schema', 'table', 'column'
            ]):
                return True
            
            # Look for model file names
            file_path = file_info.get('file_path', '').lower()
            if 'models.py' in file_path or 'models/' in file_path:
                return True
        
        return False
    
    def _has_api_endpoints(self, parsed_files: List[Dict]) -> bool:
        """Check if project has API endpoints"""
        for file_info in parsed_files:
            content = file_info.get('content', '')
            
            # Look for API patterns
            if any(pattern in content for pattern in [
                '@app.route', '@app.get', '@app.post', 'router.get', 'router.post',
                'app.get(', 'app.post(', '@Controller', '@RestController'
            ]):
                return True
        
        return False
    
    def _has_async_code(self, parsed_files: List[Dict]) -> bool:
        """Check if project uses async/await"""
        for file_info in parsed_files:
            content = file_info.get('content', '')
            if 'async ' in content or 'await ' in content:
                return True
        
        return False
    
    def _has_tests(self, codebase_path: str) -> bool:
        """Check if project has tests"""
        test_indicators = ['tests/', 'test/', '__tests__/', 'spec/']
        
        for indicator in test_indicators:
            if os.path.exists(os.path.join(codebase_path, indicator)):
                return True
        
        return False
    
    def _has_deployment_configs(self, codebase_path: str) -> bool:
        """Check if project has deployment configurations"""
        config_files = [
            'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml',
            'kubernetes/', 'k8s/', '.github/workflows/',
            'deploy/', 'deployment/', 'terraform/'
        ]
        
        for config_file in config_files:
            if os.path.exists(os.path.join(codebase_path, config_file)):
                return True
        
        return False
    
    def _calculate_complexity(self, parsed_files: List[Dict], dependency_graph: Dict) -> Dict[str, Any]:
        """Calculate complexity metrics"""
        metadata = dependency_graph.get('metadata', {})
        
        total_classes = metadata.get('total_classes', 0)
        total_functions = metadata.get('total_functions', 0)
        total_files = len(parsed_files)
        
        # Calculate average depth (based on imports)
        edges = dependency_graph.get('edges', [])
        avg_dependencies = len(edges) / total_files if total_files > 0 else 0
        
        return {
            'total_files': total_files,
            'total_classes': total_classes,
            'total_functions': total_functions,
            'total_lines': sum(f.get('line_count', 0) for f in parsed_files),
            'avg_dependencies': round(avg_dependencies, 2),
            'coupling_score': self._calculate_coupling(dependency_graph),
            'size_category': self._categorize_size(total_files),
        }
    
    def _calculate_coupling(self, dependency_graph: Dict) -> float:
        """Calculate coupling score (0-1, higher = more coupled)"""
        nodes = dependency_graph.get('nodes', [])
        edges = dependency_graph.get('edges', [])
        
        if not nodes:
            return 0.0
        
        # Possible edges = n * (n-1) for directed graph
        max_edges = len(nodes) * (len(nodes) - 1)
        
        if max_edges == 0:
            return 0.0
        
        coupling = len(edges) / max_edges
        return round(coupling, 3)
    
    def _categorize_size(self, total_files: int) -> str:
        """Categorize project size"""
        if total_files < 5:
            return 'tiny'
        elif total_files < 20:
            return 'small'
        elif total_files < 50:
            return 'medium'
        elif total_files < 200:
            return 'large'
        else:
            return 'very_large'
    
    def _determine_project_type(self, profile: Dict[str, Any]) -> str:
        """Determine the type of project"""
        frameworks = profile.get('frameworks', [])
        has_api = profile.get('has_api', False)
        has_database = profile.get('has_database', False)
        
        # Web applications
        if any(fw in frameworks for fw in ['django', 'flask', 'fastapi', 'express', 'nestjs']):
            if has_api:
                return 'web_api'
            return 'web_application'
        
        # Frontend frameworks
        if any(fw in frameworks for fw in ['react', 'vue', 'angular']):
            return 'frontend_application'
        
        # CLI tools
        if profile.get('complexity', {}).get('total_files', 0) < 10 and not has_api:
            return 'cli_tool'
        
        # Libraries
        if not has_api and not profile.get('has_deployment_configs', False):
            return 'library'
        
        # Microservices
        if profile.get('has_deployment_configs', False):
            return 'microservice'
        
        return 'application'
