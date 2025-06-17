"""
Enhanced Code validation utilities for Manim code generation
"""

import re
import ast
import logging
from typing import Tuple, Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class CodeValidator:
    """Validates and fixes Manim code generation issues."""
    
    @staticmethod
    def fix_common_issues(code: str) -> str:
        """Fix common issues in generated Manim code."""
        # Remove markdown formatting
        code = re.sub(r'```python\n?', '', code)
        code = re.sub(r'```\n?', '', code)
        code = code.replace('```', '')
        code = code.replace('`', '')
        
        # Fix string literals in Text objects
        code = re.sub(r'Text\(([^"\'()\[\]]*?)\)', r'Text("\1")', code)
        code = re.sub(r'Text\(([^"\']*?), font_size', r'Text("\1", font_size', code)
        
        # Fix unterminated string literals
        lines = code.split('\n')
        fixed_lines = []
        for line in lines:
            if 'Text(' in line and line.count('"') % 2 != 0:
                # Add closing quote before comma or parenthesis
                line = re.sub(r'([^"]*?)(,|\))', r'\1"\2', line)
            fixed_lines.append(line)
        
        code = '\n'.join(fixed_lines)
        
        # Ensure proper imports
        if not re.search(r'from manim import \*', code):
            code = 'from manim import *\n\n' + code
        
        return code.strip()
    
    @staticmethod
    def validate_python_syntax(code: str) -> Tuple[bool, Optional[str]]:
        """Validate Python syntax of the generated code."""
        try:
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, str(e)
    
    @staticmethod
    def has_scene_class(code: str) -> bool:
        """Check if the code has a proper Scene class."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if it inherits from Scene
                    for base in node.bases:
                        if isinstance(base, ast.Name) and base.id == 'Scene':
                            return True
                        elif isinstance(base, ast.Attribute) and base.attr == 'Scene':
                            return True
            return False
        except SyntaxError:
            return False
    
    @staticmethod
    def has_construct_method(code: str) -> bool:
        """Check if the Scene class has a construct method."""
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name == 'construct':
                            return True
            return False
        except SyntaxError:
            return False
    
    @staticmethod
    def has_animations(code: str) -> bool:
        """Check if the code has at least one animation."""
        required_patterns = [
            r'self\.play\(',
            r'self\.wait\('
        ]
        
        for pattern in required_patterns:
            if not re.search(pattern, code):
                return False
        return True
    
    @staticmethod
    def validate_manim_code(code: str) -> Tuple[bool, Optional[str]]:
        """Validate that the code meets Manim requirements."""
        # Check basic structure
        if not CodeValidator.has_scene_class(code):
            return False, "Code must contain a class that inherits from Scene"
        
        if not CodeValidator.has_construct_method(code):
            return False, "Scene class must have a construct method"
        
        if not CodeValidator.has_animations(code):
            return False, "Code must include at least one animation (self.play) and wait"
        
        # Check for problematic patterns
        problematic_patterns = [
            r'for\s+\*',
            r'\*\s*=',
            r'^\s*\*',  # Lines starting with *
            r'get\*center',
            r'import\s+\*',  # No wildcard imports except manim
            r'from\s+[^\s]+\s+import\s+\*'  # No wildcard imports except manim
        ]
        
        for pattern in problematic_patterns:
            if re.search(pattern, code, re.MULTILINE):
                return False, f"Code contains problematic pattern: {pattern}"
        
        return True, None