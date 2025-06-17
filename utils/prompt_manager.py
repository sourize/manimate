"""Prompt management and code generation utilities."""

import logging
from typing import Dict, Any, Optional
from groq import Groq

from config.constants import (
    AnimationCategory,
    ANIMATION_CONSTANTS,
    ErrorType
)
from utils.error_handler import ErrorHandler

logger = logging.getLogger(__name__)

class PromptManager:
    """Manages prompt enhancement and code generation."""
    
    def __init__(self):
        """Initialize the prompt manager."""
        self.category_contexts = {
            AnimationCategory.ALGEBRA: """
                Focus on algebraic concepts like:
                - Equations and inequalities
                - Function transformations
                - Polynomial operations
                - Algebraic proofs
                Use colors to distinguish different terms and operations.
            """,
            AnimationCategory.GEOMETRY: """
                Focus on geometric concepts like:
                - Shapes and their properties
                - Constructions and transformations
                - Theorems and proofs
                - Spatial relationships
                Use clear lines and shapes with appropriate colors.
            """,
            AnimationCategory.CALCULUS: """
                Focus on calculus concepts like:
                - Derivatives and integrals
                - Limits and continuity
                - Series and sequences
                - Applications of calculus
                Use smooth curves and clear visualizations of rates of change.
            """,
            AnimationCategory.STATISTICS: """
                Focus on statistical concepts like:
                - Probability distributions
                - Statistical measures
                - Data visualization
                - Statistical tests
                Use appropriate graphs and charts with clear labels.
            """,
            AnimationCategory.LINEAR_ALGEBRA: """
                Focus on linear algebra concepts like:
                - Matrices and vectors
                - Linear transformations
                - Eigenvalues and eigenvectors
                - Vector spaces
                Use clear geometric interpretations with appropriate colors.
            """,
            AnimationCategory.NUMBER_THEORY: """
                Focus on number theory concepts like:
                - Prime numbers and factorization
                - Modular arithmetic
                - Number sequences
                - Mathematical proofs
                Use clear visualizations of number patterns and relationships.
            """,
            AnimationCategory.OTHER: """
                Focus on creating clear and educational animations that:
                - Explain mathematical concepts visually
                - Use appropriate colors and shapes
                - Include clear labels and annotations
                - Maintain a logical flow of information
            """
        }
    
    def detect_category(self, prompt: str) -> AnimationCategory:
        """Detect the mathematical category of a prompt."""
        prompt_lower = prompt.lower()
        
        # Simple keyword-based category detection
        if any(word in prompt_lower for word in ["equation", "function", "polynomial", "algebra"]):
            return AnimationCategory.ALGEBRA
        elif any(word in prompt_lower for word in ["shape", "geometry", "triangle", "circle", "square"]):
            return AnimationCategory.GEOMETRY
        elif any(word in prompt_lower for word in ["derivative", "integral", "limit", "calculus"]):
            return AnimationCategory.CALCULUS
        elif any(word in prompt_lower for word in ["statistic", "probability", "distribution", "data"]):
            return AnimationCategory.STATISTICS
        elif any(word in prompt_lower for word in ["matrix", "vector", "linear", "eigen"]):
            return AnimationCategory.LINEAR_ALGEBRA
        elif any(word in prompt_lower for word in ["prime", "number", "sequence", "modular"]):
            return AnimationCategory.NUMBER_THEORY
        else:
            return AnimationCategory.OTHER
    
    def get_enhancement_context(self, prompt: str) -> str:
        """Get category-specific context for prompt enhancement."""
        category = self.detect_category(prompt)
        return self.category_contexts.get(category, self.category_contexts[AnimationCategory.OTHER])
    
    def enhance_prompt(
        self,
        user_prompt: str,
        client: Groq,
        model: str,
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> str:
        """Enhance the user prompt for better Manim code generation."""
        category_context = self.get_enhancement_context(user_prompt)
        
        enhancement_prompt = f"""
You are an expert at creating detailed prompts for Manim (Mathematical Animation Engine) video generation.

User's original prompt: "{user_prompt}"

Context: {category_context}

Please enhance this prompt by:
1. Adding specific mathematical or visual details
2. Suggesting appropriate Manim objects and animations  
3. Specifying colors, positioning, and timing
4. Including educational context if applicable
5. Making it clear and comprehensive for code generation

Enhanced prompt should be detailed but concise, focusing on visual elements that can be animated with Manim.

Return only the enhanced prompt, nothing else.
"""
        
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": enhancement_prompt}],
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error enhancing prompt: {e}")
            ErrorHandler.handle_error(ErrorType.PROMPT_ERROR, str(e))
            return user_prompt
    
    def generate_code(
        self,
        enhanced_prompt: str,
        client: Groq,
        model: str,
        temperature: float = 0.3,
        max_tokens: int = 2000
    ) -> str:
        """Generate Manim code from the enhanced prompt."""
        code_generation_prompt = f"""
You are an expert Manim developer. Generate a complete, working Manim scene based on this prompt:

"{enhanced_prompt}"

Requirements:
1. Create a class that inherits from Scene
2. Use proper Manim syntax and imports
3. Include appropriate animations (Create, Transform, Write, etc.)
4. Add colors, positioning, and timing
5. Make it visually appealing and educational
6. Ensure the code is syntactically correct
7. Use self.play() for animations and self.wait() for pauses
8. Include comments explaining key parts
9. Keep animations under {ANIMATION_CONSTANTS['MAX_DURATION']} seconds total duration
10. Use appropriate wait times between animations (between {ANIMATION_CONSTANTS['MIN_WAIT_TIME']} and {ANIMATION_CONSTANTS['MAX_WAIT_TIME']} seconds)
11. To set background color, use: self.camera.background_color = WHITE

Structure:
```python
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = WHITE
        
        # Your animation code here
        pass
```

Generate ONLY the Python code, no explanations or markdown formatting.
"""
        
        try:
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": code_generation_prompt}],
                model=model,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating Manim code: {e}")
            ErrorHandler.handle_error(ErrorType.CODE_GENERATION_ERROR, str(e))
            raise 