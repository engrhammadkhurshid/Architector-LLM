"""
Version Detector
Automatically detects project version from various project configuration files
Supports multiple languages and package managers
"""

import os
import json
import re
import logging
from typing import Optional, Dict, Any
from pathlib import Path
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

class VersionDetector:
    """
    Detects project version from configuration files across multiple languages and ecosystems
    """
    
    def __init__(self):
        self.version_patterns = {
            # Semantic versioning patterns
            'semver': r'(\d+\.\d+\.\d+(?:-[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?(?:\+[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*)?)',
            'loose_semver': r'(\d+\.\d+(?:\.\d+)?)',
        }
    
    def detect(self, codebase_path: str) -> Dict[str, Any]:
        """
        Detect version from project files
        
        Args:
            codebase_path: Root path of the codebase
            
        Returns:
            Dictionary with version info:
            {
                'version': str,  # Detected version or None
                'source': str,   # Source file where version was found
                'language': str, # Language/ecosystem
                'confidence': str # 'high', 'medium', 'low'
            }
        """
        logger.info(f'Detecting version from: {codebase_path}')
        
        # Try detection methods in order of reliability
        detectors = [
            # Node.js / JavaScript / TypeScript
            ('package.json', self._detect_npm_version),
            
            # Python
            ('setup.py', self._detect_setup_py_version),
            ('pyproject.toml', self._detect_pyproject_version),
            ('__init__.py', self._detect_python_init_version),
            ('setup.cfg', self._detect_setup_cfg_version),
            
            # PHP
            ('composer.json', self._detect_composer_version),
            
            # Java / Kotlin / Scala
            ('pom.xml', self._detect_maven_version),
            ('build.gradle', self._detect_gradle_version),
            ('build.gradle.kts', self._detect_gradle_kotlin_version),
            
            # C# / .NET
            ('*.csproj', self._detect_csproj_version),
            ('Directory.Build.props', self._detect_dotnet_props_version),
            
            # Rust
            ('Cargo.toml', self._detect_cargo_version),
            
            # Go
            ('go.mod', self._detect_go_mod_version),
            
            # Ruby
            ('Gemfile', self._detect_gemfile_version),
            ('*.gemspec', self._detect_gemspec_version),
            
            # C/C++
            ('CMakeLists.txt', self._detect_cmake_version),
            ('configure.ac', self._detect_autoconf_version),
            
            # Swift
            ('Package.swift', self._detect_swift_package_version),
            
            # WordPress
            ('style.css', self._detect_wordpress_theme_version),
            ('*.php', self._detect_wordpress_plugin_version),
            
            # Generic VERSION files
            ('VERSION', self._detect_version_file),
            ('version.txt', self._detect_version_file),
            ('.version', self._detect_version_file),
        ]
        
        for pattern, detector in detectors:
            result = self._try_detector(codebase_path, pattern, detector)
            if result and result.get('version'):
                logger.info(f'Version detected: {result["version"]} from {result["source"]}')
                return result
        
        logger.warning('No version detected from project files')
        return {
            'version': None,
            'source': None,
            'language': 'unknown',
            'confidence': 'none'
        }
    
    def _try_detector(self, codebase_path: str, pattern: str, detector) -> Optional[Dict[str, Any]]:
        """Try a detector on matching files"""
        try:
            if '*' in pattern:
                # Glob pattern
                from glob import glob
                matches = glob(os.path.join(codebase_path, '**', pattern), recursive=True)
                for match in matches[:5]:  # Limit to first 5 matches
                    result = detector(match)
                    if result:
                        return result
            else:
                # Direct file
                file_path = os.path.join(codebase_path, pattern)
                if os.path.exists(file_path):
                    return detector(file_path)
        except Exception as e:
            logger.debug(f'Detector {pattern} failed: {e}')
        
        return None
    
    # ===== Node.js / JavaScript / TypeScript =====
    
    def _detect_npm_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from package.json"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                version = data.get('version')
                if version:
                    return {
                        'version': version,
                        'source': 'package.json',
                        'language': 'node.js',
                        'confidence': 'high'
                    }
        except Exception as e:
            logger.debug(f'Failed to parse package.json: {e}')
        
        return None
    
    # ===== Python =====
    
    def _detect_pyproject_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from pyproject.toml (PEP 518)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Try [project] section (PEP 621)
                match = re.search(r'\[project\].*?version\s*=\s*["\']([^"\']+)["\']', content, re.DOTALL)
                if match:
                    return {
                        'version': match.group(1),
                        'source': 'pyproject.toml',
                        'language': 'python',
                        'confidence': 'high'
                    }
                
                # Try [tool.poetry] section
                match = re.search(r'\[tool\.poetry\].*?version\s*=\s*["\']([^"\']+)["\']', content, re.DOTALL)
                if match:
                    return {
                        'version': match.group(1),
                        'source': 'pyproject.toml (poetry)',
                        'language': 'python',
                        'confidence': 'high'
                    }
        except Exception as e:
            logger.debug(f'Failed to parse pyproject.toml: {e}')
        
        return None
    
    def _detect_setup_py_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from setup.py"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Look for version= in setup()
                match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return {
                        'version': match.group(1),
                        'source': 'setup.py',
                        'language': 'python',
                        'confidence': 'medium'
                    }
        except Exception as e:
            logger.debug(f'Failed to parse setup.py: {e}')
        
        return None
    
    def _detect_setup_cfg_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from setup.cfg"""
        try:
            import configparser
            config = configparser.ConfigParser()
            config.read(file_path)
            
            if 'metadata' in config and 'version' in config['metadata']:
                return {
                    'version': config['metadata']['version'],
                    'source': 'setup.cfg',
                    'language': 'python',
                    'confidence': 'high'
                }
        except Exception as e:
            logger.debug(f'Failed to parse setup.cfg: {e}')
        
        return None
    
    def _detect_python_init_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect __version__ from __init__.py"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return {
                        'version': match.group(1),
                        'source': '__init__.py',
                        'language': 'python',
                        'confidence': 'medium'
                    }
        except Exception as e:
            logger.debug(f'Failed to parse __init__.py: {e}')
        
        return None
    
    # ===== PHP =====
    
    def _detect_composer_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from composer.json"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                version = data.get('version')
                if version:
                    return {
                        'version': version,
                        'source': 'composer.json',
                        'language': 'php',
                        'confidence': 'high'
                    }
        except Exception as e:
            logger.debug(f'Failed to parse composer.json: {e}')
        
        return None
    
    def _detect_wordpress_plugin_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from WordPress plugin header"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(8192)  # Read first 8KB
                
                # Look for WordPress plugin header
                if 'Plugin Name:' in content:
                    match = re.search(r'Version:\s*([0-9.]+)', content)
                    if match:
                        return {
                            'version': match.group(1),
                            'source': os.path.basename(file_path),
                            'language': 'php (wordpress plugin)',
                            'confidence': 'high'
                        }
        except Exception as e:
            logger.debug(f'Failed to parse WordPress plugin: {e}')
        
        return None
    
    def _detect_wordpress_theme_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from WordPress theme style.css"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(8192)
                
                # Look for WordPress theme header
                if 'Theme Name:' in content:
                    match = re.search(r'Version:\s*([0-9.]+)', content)
                    if match:
                        return {
                            'version': match.group(1),
                            'source': 'style.css',
                            'language': 'php (wordpress theme)',
                            'confidence': 'high'
                        }
        except Exception as e:
            logger.debug(f'Failed to parse WordPress theme: {e}')
        
        return None
    
    # ===== Java / Kotlin / Scala =====
    
    def _detect_maven_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from Maven pom.xml"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # Handle XML namespaces
            ns = {'maven': 'http://maven.apache.org/POM/4.0.0'}
            
            version = root.find('.//maven:version', ns)
            if version is None:
                version = root.find('.//version')
            
            if version is not None and version.text:
                return {
                    'version': version.text,
                    'source': 'pom.xml',
                    'language': 'java (maven)',
                    'confidence': 'high'
                }
        except Exception as e:
            logger.debug(f'Failed to parse pom.xml: {e}')
        
        return None
    
    def _detect_gradle_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from build.gradle"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                match = re.search(r'version\s*=?\s*["\']([^"\']+)["\']', content)
                if match:
                    return {
                        'version': match.group(1),
                        'source': 'build.gradle',
                        'language': 'java (gradle)',
                        'confidence': 'medium'
                    }
        except Exception as e:
            logger.debug(f'Failed to parse build.gradle: {e}')
        
        return None
    
    def _detect_gradle_kotlin_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from build.gradle.kts"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                match = re.search(r'version\s*=\s*"([^"]+)"', content)
                if match:
                    return {
                        'version': match.group(1),
                        'source': 'build.gradle.kts',
                        'language': 'kotlin (gradle)',
                        'confidence': 'medium'
                    }
        except Exception as e:
            logger.debug(f'Failed to parse build.gradle.kts: {e}')
        
        return None
    
    # ===== C# / .NET =====
    
    def _detect_csproj_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from .csproj file"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            version = root.find('.//Version')
            if version is None:
                version = root.find('.//VersionPrefix')
            
            if version is not None and version.text:
                return {
                    'version': version.text,
                    'source': os.path.basename(file_path),
                    'language': 'csharp (.net)',
                    'confidence': 'high'
                }
        except Exception as e:
            logger.debug(f'Failed to parse .csproj: {e}')
        
        return None
    
    def _detect_dotnet_props_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from Directory.Build.props"""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            version = root.find('.//Version')
            if version is not None and version.text:
                return {
                    'version': version.text,
                    'source': 'Directory.Build.props',
                    'language': 'csharp (.net)',
                    'confidence': 'high'
                }
        except Exception as e:
            logger.debug(f'Failed to parse Directory.Build.props: {e}')
        
        return None
    
    # ===== Rust =====
    
    def _detect_cargo_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from Cargo.toml"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                match = re.search(r'\[package\].*?version\s*=\s*"([^"]+)"', content, re.DOTALL)
                if match:
                    return {
                        'version': match.group(1),
                        'source': 'Cargo.toml',
                        'language': 'rust',
                        'confidence': 'high'
                    }
        except Exception as e:
            logger.debug(f'Failed to parse Cargo.toml: {e}')
        
        return None
    
    # ===== Go =====
    
    def _detect_go_mod_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from go.mod (Git tags convention)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Go uses Git tags for versioning (v1.2.3)
                match = re.search(r'module\s+([^\s]+)(/v\d+)?', content)
                if match:
                    # Go doesn't store version in go.mod, return None
                    # Version must come from Git tags
                    return None
        except Exception as e:
            logger.debug(f'Failed to parse go.mod: {e}')
        
        return None
    
    # ===== Ruby =====
    
    def _detect_gemfile_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from Gemfile (usually not present)"""
        # Gemfile typically doesn't contain version
        return None
    
    def _detect_gemspec_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from .gemspec"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                match = re.search(r'\.version\s*=\s*["\']([^"\']+)["\']', content)
                if match:
                    return {
                        'version': match.group(1),
                        'source': os.path.basename(file_path),
                        'language': 'ruby',
                        'confidence': 'high'
                    }
        except Exception as e:
            logger.debug(f'Failed to parse .gemspec: {e}')
        
        return None
    
    # ===== C/C++ =====
    
    def _detect_cmake_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from CMakeLists.txt"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Look for project(NAME VERSION x.y.z)
                match = re.search(r'project\s*\([^)]*VERSION\s+([0-9.]+)', content, re.IGNORECASE)
                if match:
                    return {
                        'version': match.group(1),
                        'source': 'CMakeLists.txt',
                        'language': 'c/c++ (cmake)',
                        'confidence': 'high'
                    }
        except Exception as e:
            logger.debug(f'Failed to parse CMakeLists.txt: {e}')
        
        return None
    
    def _detect_autoconf_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from configure.ac"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                match = re.search(r'AC_INIT\s*\([^,]*,\s*\[?([0-9.]+)\]?', content)
                if match:
                    return {
                        'version': match.group(1),
                        'source': 'configure.ac',
                        'language': 'c/c++ (autoconf)',
                        'confidence': 'high'
                    }
        except Exception as e:
            logger.debug(f'Failed to parse configure.ac: {e}')
        
        return None
    
    # ===== Swift =====
    
    def _detect_swift_package_version(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from Package.swift"""
        # Swift Package Manager doesn't store version in Package.swift
        # Version comes from Git tags
        return None
    
    # ===== Generic VERSION files =====
    
    def _detect_version_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Detect version from VERSION, version.txt, .version files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
                # Extract first semver-like pattern
                match = re.search(self.version_patterns['semver'], content)
                if not match:
                    match = re.search(self.version_patterns['loose_semver'], content)
                
                if match:
                    return {
                        'version': match.group(1),
                        'source': os.path.basename(file_path),
                        'language': 'generic',
                        'confidence': 'medium'
                    }
        except Exception as e:
            logger.debug(f'Failed to parse version file: {e}')
        
        return None
    
    def validate_semver(self, version: str) -> bool:
        """Validate semantic version format"""
        return bool(re.match(self.version_patterns['semver'], version))
