"""
Prompt templates and categorization for different types of mathematical animations
"""

class PromptTemplates:
    """Templates for different types of animations"""
    
    TEMPLATES = {
        "algebra": {
            "enhancement": "Focus on algebraic concepts like equations, functions, and graphing. Include coordinate systems, variable animations, and step-by-step solving processes with clear mathematical notation.",
            "keywords": ["equation", "function", "graph", "variable", "solve", "polynomial", "quadratic", "linear"],
            "example_objects": ["Axes", "NumberLine", "MathTex", "DecimalNumber"],
            "colors": ["BLUE", "RED", "GREEN", "YELLOW"]
        },
        "geometry": {
            "enhancement": "Emphasize geometric shapes, transformations, and proofs. Include angles, lines, circles, and spatial relationships with clear visual representations and construction animations.",
            "keywords": ["triangle", "circle", "angle", "polygon", "proof", "geometry", "shape", "construction"],
            "example_objects": ["Circle", "Square", "Triangle", "Line", "Arc", "Polygon"],
            "colors": ["PURPLE", "ORANGE", "PINK", "TEAL"]
        },
        "calculus": {
            "enhancement": "Highlight calculus concepts like derivatives, integrals, and limits. Show function behavior, area under curves, and rate of change visualizations with smooth transformations.",
            "keywords": ["derivative", "integral", "limit", "function", "calculus", "rate", "slope", "area"],
            "example_objects": ["Axes", "FunctionGraph", "Area", "Dot", "Vector"],
            "colors": ["MAROON", "DARK_BLUE", "GOLD", "LIGHT_BROWN"]
        },
        "statistics": {
            "enhancement": "Focus on data visualization, probability distributions, and statistical concepts. Include charts, graphs, histograms, and probability animations with clear data representation.",
            "keywords": ["probability", "distribution", "data", "statistics", "chart", "graph", "histogram", "mean"],
            "example_objects": ["BarChart", "Axes", "Rectangle", "Text", "NumberLine"],
            "colors": ["LIGHT_GREY", "DARK_GREY", "BLUE_E", "RED_E"]
        },
        "physics": {
            "enhancement": "Emphasize physics concepts with mathematical foundations. Include motion, forces, waves, and physical phenomena with proper mathematical representations and vector animations.",
            "keywords": ["motion", "force", "wave", "physics", "velocity", "acceleration", "vector", "field"],
            "example_objects": ["Vector", "Dot", "Circle", "Line", "FunctionGraph"],
            "colors": ["LIGHT_PINK", "LIGHT_BLUE", "WHITE", "GREY"]
        },
        "number_theory": {
            "enhancement": "Focus on number properties, sequences, patterns, and mathematical relationships. Include prime numbers, Fibonacci sequences, and number patterns with clear visual progression.",
            "keywords": ["prime", "fibonacci", "sequence", "pattern", "number", "divisor", "factor", "modular"],
            "example_objects": ["NumberLine", "Text", "Circle", "Rectangle", "MathTex"],
            "colors": ["GOLD", "SILVER", "BRONZE", "COPPER"]
        },
        "trigonometry": {
            "enhancement": "Emphasize trigonometric functions, unit circles, and wave patterns. Include sine, cosine, tangent functions with circular representations and periodic behavior.",
            "keywords": ["sine", "cosine", "tangent", "angle", "circle", "radian", "periodic", "wave"],
            "example_objects": ["Circle", "Axes", "FunctionGraph", "Arc", "Line"],
            "colors": ["BLUE_A", "BLUE_B", "BLUE_C", "BLUE_D"]
        },
        "linear_algebra": {
            "enhancement": "Focus on vectors, matrices, transformations, and linear systems. Include vector spaces, eigenvalues, and geometric interpretations of linear operations.",
            "keywords": ["vector", "matrix", "transformation", "eigenvalue", "linear", "basis", "determinant"],
            "example_objects": ["Vector", "Matrix", "Axes", "Arrow", "Rectangle"],
            "colors": ["RED_A", "RED_B", "RED_C", "RED_D"]
        },
        "complex_analysis": {
            "enhancement": "Emphasize complex numbers, complex plane, and complex functions. Include Argand diagrams, complex transformations, and visualizations of complex operations.",
            "keywords": ["complex", "imaginary", "real", "argand", "magnitude", "phase", "euler"],
            "example_objects": ["ComplexPlane", "Axes", "Vector", "Circle", "FunctionGraph"],
            "colors": ["PURPLE_A", "PURPLE_B", "PURPLE_C", "PURPLE_D"]
        }
    }
    
    @classmethod
    def detect_category(cls, prompt: str) -> str:
        """Detect the category of the prompt based on keywords"""
        prompt_lower = prompt.lower()
        
        scores = {}
        for category, template in cls.TEMPLATES.items():
            score = sum(1 for keyword in template["keywords"] if keyword in prompt_lower)
            scores[category] = score
        
        # Return category with highest score, default to algebra
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "algebra"
    
    @classmethod
    def get_enhancement_context(cls, prompt: str) -> str:
        """Get enhancement context based on detected category"""
        category = cls.detect_category(prompt)
        return cls.TEMPLATES[category]["enhancement"]
    
    @classmethod
    def get_suggested_objects(cls, prompt: str) -> list:
        """Get suggested Manim objects for the prompt category"""
        category = cls.detect_category(prompt)
        return cls.TEMPLATES[category]["example_objects"]
    
    @classmethod
    def get_suggested_colors(cls, prompt: str) -> list:
        """Get suggested colors for the prompt category"""
        category = cls.detect_category(prompt)
        return cls.TEMPLATES[category]["colors"]
    
    @classmethod
    def get_all_categories(cls) -> list:
        """Get all available categories"""
        return list(cls.TEMPLATES.keys())
    
    @classmethod
    def get_category_info(cls, category: str) -> dict:
        """Get complete information about a specific category"""
        return cls.TEMPLATES.get(category, cls.TEMPLATES["algebra"])

class ManimCodeExamples:
    """Collection of Manim code examples for reference"""
    
    BASIC_EXAMPLES = {
        "text_animation": """
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create and animate text
        title = Text("Hello Manim!", font_size=48)
        self.play(Write(title))
        self.wait(1)
        
        # Transform text
        subtitle = Text("Mathematical Animations", font_size=36)
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Transform(title, subtitle))
        self.wait(2)
""",
        
        "shape_animation": """
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create shapes
        circle = Circle(radius=1, color=BLUE)
        square = Square(side_length=2, color=RED)
        
        # Position shapes
        circle.to_edge(LEFT)
        square.to_edge(RIGHT)
        
        # Animate creation
        self.play(Create(circle), Create(square))
        self.wait(1)
        
        # Transform circle to square
        self.play(Transform(circle, square))
        self.wait(2)
""",
        
        "graph_animation": """
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": WHITE}
        )
        
        # Create function
        func = axes.plot(lambda x: x**2, color=YELLOW)
        func_label = axes.get_graph_label(func, label="f(x) = x^2")
        
        # Animate
        self.play(Create(axes))
        self.play(Create(func))
        self.play(Write(func_label))
        self.wait(2)
""",
        
        "algebra_example": """
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create equation
        equation = MathTex("x^2 + 3x - 4 = 0")
        equation.scale(1.5)
        self.play(Write(equation))
        self.wait(1)
        
        # Show factoring
        factored = MathTex("(x + 4)(x - 1) = 0")
        factored.scale(1.5)
        self.play(Transform(equation, factored))
        self.wait(2)
""",
        
        "geometry_example": """
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create triangle
        triangle = Triangle(color=BLUE)
        triangle.scale(2)
        self.play(Create(triangle))
        
        # Add labels
        labels = ["A", "B", "C"]
        vertices = triangle.get_vertices()
        for i, label in enumerate(labels):
            text = Text(label).next_to(vertices[i], vertices[i]/2)
            self.play(Write(text))
        
        self.wait(2)
""",
        
        "calculus_example": """
from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create axes and function
        axes = Axes(x_range=[-2, 2], y_range=[-1, 3])
        func = axes.plot(lambda x: x**2, color=BLUE)
        
        # Create tangent line
        tangent = axes.plot(lambda x: 2*x, color=RED)
        
        self.play(Create(axes))
        self.play(Create(func))
        self.play(Create(tangent))
        self.wait(2)
"""
    }
    
    @classmethod
    def get_example_by_type(cls, animation_type: str) -> str:
        """Get example code by type"""
        return cls.BASIC_EXAMPLES.get(animation_type, cls.BASIC_EXAMPLES["text_animation"])
    
    @classmethod
    def get_example_by_category(cls, category: str) -> str:
        """Get example code by mathematical category"""
        category_examples = {
            "algebra": "algebra_example",
            "geometry": "geometry_example", 
            "calculus": "calculus_example",
            "statistics": "graph_animation",
            "physics": "graph_animation"
        }
        example_key = category_examples.get(category, "text_animation")
        return cls.BASIC_EXAMPLES[example_key]
    
    @classmethod
    def get_all_examples(cls) -> dict:
        """Get all available examples"""
        return cls.BASIC_EXAMPLES