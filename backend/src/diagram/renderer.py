"""
Diagram Renderer
Converts Mermaid diagram code to PNG/SVG images
"""

import os
import logging
import subprocess
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class DiagramRenderer:
    """
    Renders Mermaid diagram code to visual assets (PNG/SVG)
    """
    
    def __init__(self):
        self.mermaid_cli = 'mmdc'  # Mermaid CLI command
        self.check_dependencies()
    
    def check_dependencies(self) -> bool:
        """Check if Mermaid CLI is installed"""
        try:
            result = subprocess.run(
                [self.mermaid_cli, '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f'Mermaid CLI found: {result.stdout.strip()}')
                return True
            else:
                logger.warning('Mermaid CLI not found. Install with: npm install -g @mermaid-js/mermaid-cli')
                return False
        except FileNotFoundError:
            logger.warning('Mermaid CLI not found. Install with: npm install -g @mermaid-js/mermaid-cli')
            return False
        except Exception as e:
            logger.error(f'Error checking Mermaid CLI: {e}')
            return False
    
    def render(
        self,
        diagram_code: str,
        output_path: str,
        output_format: str = 'png'
    ) -> bool:
        """
        Render Mermaid diagram code to an image file
        
        Args:
            diagram_code: Mermaid syntax diagram code
            output_path: Path where the image should be saved
            output_format: Output format ('png' or 'svg')
            
        Returns:
            True if successful, False otherwise
        """
        logger.info(f'Rendering diagram to {output_path}')
        
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Extract Mermaid code from markdown code blocks if present
            diagram_code = self._extract_mermaid_code(diagram_code)
            
            # Create temporary input file
            temp_input = output_path.replace(f'.{output_format}', '.mmd')
            with open(temp_input, 'w', encoding='utf-8') as f:
                f.write(diagram_code)
            
            # Run Mermaid CLI
            cmd = [
                self.mermaid_cli,
                '-i', temp_input,
                '-o', output_path,
                '-b', 'transparent'
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Clean up temp file
            if os.path.exists(temp_input):
                os.remove(temp_input)
            
            if result.returncode == 0:
                logger.info(f'Diagram rendered successfully: {output_path}')
                return True
            else:
                logger.error(f'Failed to render diagram: {result.stderr}')
                return False
                
        except Exception as e:
            logger.error(f'Error rendering diagram: {str(e)}')
            return False
    
    def _extract_mermaid_code(self, content: str) -> str:
        """Extract Mermaid code from markdown code blocks"""
        # Look for ```mermaid ... ``` blocks
        if '```mermaid' in content:
            start = content.find('```mermaid') + 10
            end = content.find('```', start)
            return content[start:end].strip()
        return content.strip()
    
    def render_multiple(
        self,
        diagrams: list,
        output_dir: str,
        output_format: str = 'png'
    ) -> list:
        """
        Render multiple diagrams
        
        Args:
            diagrams: List of tuples (name, diagram_code)
            output_dir: Directory to save rendered diagrams
            output_format: Output format ('png' or 'svg')
            
        Returns:
            List of successfully rendered file paths
        """
        rendered_files = []
        
        for name, code in diagrams:
            output_path = os.path.join(output_dir, f'{name}.{output_format}')
            if self.render(code, output_path, output_format):
                rendered_files.append(output_path)
        
        return rendered_files
