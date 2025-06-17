from enum import Enum, auto
from typing import Dict, List, Tuple

# Quality levels
LOW = "low_quality"
MEDIUM = "medium_quality"

# Model identifiers
LLAMA_70B = "llama-3.3-70b-versatile"
LLAMA_8B = "llama3-8b-8192"

class VideoQuality(Enum):
    LOW = "low_quality"
    MEDIUM = "medium_quality"

class ModelType(Enum):
    LLAMA_70B = "llama-3.3-70b-versatile"
    LLAMA_8B = "llama3-8b-8192"

class AnimationCategory(Enum):
    ALGEBRA = "algebra"
    GEOMETRY = "geometry"
    CALCULUS = "calculus"
    STATISTICS = "statistics"
    LINEAR_ALGEBRA = "linear_algebra"
    NUMBER_THEORY = "number_theory"
    OTHER = "other"

class ErrorType(Enum):
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

# CSS Classes
CSS_CLASSES = {
    "MAIN_HEADER": "main-header",
    "STATUS_BOX": "status-box",
    "SUCCESS_BOX": "success-box",
    "ERROR_BOX": "error-box",
    "INFO_BOX": "info-box",
    "METRIC_BOX": "metric-box",
    "header": """
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 7%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    """,
    "container": """
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    """
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

# Application constants
APP_CONSTANTS = {
    "MAX_RENDER_TIME": 300,  # seconds
    "MAX_PROMPT_LENGTH": 1000,
    "MIN_PROMPT_LENGTH": 10,
    "DEFAULT_VIDEO_QUALITY": VideoQuality.MEDIUM.value,
    "TEMP_FILE_PREFIX": "manim_",
    "LOG_FILE_NAME": "manimate.log"
}

def get_css_class(class_name: str) -> str:
    return CSS_CLASSES.get(class_name, "")

def get_status_message(key: str) -> str:
    return STATUS_MESSAGES.get(key, "") 