"""Application constants and enums."""

from enum import Enum, auto
from typing import Dict, List, Tuple

class VideoQuality(Enum):
    """Video quality levels."""
    LOW = "low_quality"
    MEDIUM = "medium_quality"
    HIGH = "high_quality"
    PRODUCTION = "production_quality"

class ModelType(Enum):
    """Available AI models."""
    LLAMA_70B = "llama-3.3-70b-versatile"
    LLAMA_8B = "llama3-8b-8192"
    MIXTRAL = "mixtral-8x7b-32768"
    GEMMA = "gemma2-9b-it"

class AnimationCategory(Enum):
    """Categories of mathematical animations."""
    ALGEBRA = "algebra"
    GEOMETRY = "geometry"
    CALCULUS = "calculus"
    STATISTICS = "statistics"
    LINEAR_ALGEBRA = "linear_algebra"
    NUMBER_THEORY = "number_theory"
    OTHER = "other"

class ErrorType(Enum):
    """Types of errors that can occur."""
    RENDERING_ERROR = auto()
    CODE_GENERATION_ERROR = auto()
    PROMPT_ERROR = auto()
    SYSTEM_ERROR = auto()
    VALIDATION_ERROR = auto()
    TIMEOUT_ERROR = auto()
    API_ERROR = auto()

# UI Constants
UI_CONSTANTS = {
    "MAX_EXAMPLE_LENGTH": 50,
    "PROGRESS_STEPS": 4,
    "DEFAULT_TEXT_AREA_HEIGHT": 150,
    "LOG_DISPLAY_HEIGHT": 200,
    "METRIC_BOX_COLUMNS": 3
}

# Animation Constants
ANIMATION_CONSTANTS = {
    "MAX_DURATION": 15,  # seconds
    "DEFAULT_WAIT_TIME": 1.0,  # seconds
    "MIN_WAIT_TIME": 0.5,  # seconds
    "MAX_WAIT_TIME": 3.0,  # seconds
    "DEFAULT_RUN_TIME": 2.0,  # seconds
}

# File Constants
FILE_CONSTANTS = {
    "SCENE_FILE_NAME": "scene.py",
    "OUTPUT_FILE_NAME": "output_video",
    "VIDEO_EXTENSION": ".mp4",
    "TEMP_DIR_PREFIX": "manim_",
    "LOG_FILE_NAME": "manimate.log"
}

# Example Prompts by Category
EXAMPLE_PROMPTS: Dict[AnimationCategory, List[str]] = {
    AnimationCategory.ALGEBRA: [
        "Visualize solving x² + 3x - 4 = 0 using the quadratic formula",
        "Show function transformations with f(x) = x² shifting and scaling"
    ],
    AnimationCategory.GEOMETRY: [
        "Demonstrate the Pythagorean theorem with squares on triangle sides",
        "Animate the construction of a regular pentagon using compass and straightedge"
    ],
    AnimationCategory.CALCULUS: [
        "Show the concept of limits with a function approaching a value",
        "Visualize area under curve using Riemann sums with rectangles"
    ],
    AnimationCategory.STATISTICS: [
        "Animate the Central Limit Theorem with multiple distributions",
        "Show correlation vs causation with scatter plot examples"
    ]
}

# CSS Classes
CSS_CLASSES = {
    "MAIN_HEADER": "main-header",
    "STATUS_BOX": "status-box",
    "SUCCESS_BOX": "success-box",
    "ERROR_BOX": "error-box",
    "INFO_BOX": "info-box",
    "METRIC_BOX": "metric-box"
}

# CSS Styles
CSS_STYLES = {
    "MAIN_HEADER_STYLE": """
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    """,
    "BUTTON_STYLE": """
        width: 100%;
        height: 3rem;
    """,
    "BOX_STYLE": """
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    """
}

# Status Messages
STATUS_MESSAGES = {
    "PROMPT_ENHANCEMENT": "🔄 Step 1/4: Enhancing your prompt...",
    "CODE_GENERATION": "🔄 Step 2/4: Generating Manim code...",
    "RENDER_SETUP": "🔄 Step 3/4: Setting up rendering environment...",
    "RENDERING": "🔄 Step 4/4: Rendering video...",
    "SUCCESS": "✅ Video generated successfully!",
    "ERROR": "❌ Error occurred during generation"
}

def get_example_prompts(category: AnimationCategory) -> List[str]:
    """Get example prompts for a specific category."""
    return EXAMPLE_PROMPTS.get(category, [])

def get_css_class(class_name: str) -> str:
    """Get CSS class name by key."""
    return CSS_CLASSES.get(class_name, "")

def get_status_message(key: str) -> str:
    """Get status message by key."""
    return STATUS_MESSAGES.get(key, "") 