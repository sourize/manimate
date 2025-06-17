from pathlib import Path
from typing import Dict, Any

# Base paths
BASE_DIR = Path(__file__).parent.parent
TEMP_DIR = BASE_DIR / "temp"
MEDIA_DIR = BASE_DIR / "media"

# Create directories if they don't exist
TEMP_DIR.mkdir(exist_ok=True)
MEDIA_DIR.mkdir(exist_ok=True)

# API Settings
GROQ_API_BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_MODEL = "llama-3.3-70b-versatile"

# Available Models
AVAILABLE_MODELS = {
    "llama-3.3-70b-versatile": {
        "name": "Llama 3.3 70B",
        "description": "Most capable model, best for complex animations",
        "max_tokens": 4096,
        "temperature": 0.7
    },
    "llama3-8b-8192": {
        "name": "Llama 3 8B",
        "description": "Fast and efficient for simpler animations",
        "max_tokens": 8192,
        "temperature": 0.7
    }
}

# Video Quality Settings
QUALITY_SETTINGS = {
    "low_quality": {
        "flag": "-ql",
        "description": "Low Quality (Fast)",
        "estimated_time": 60,  # seconds
        "resolution": "480p"
    },
    "medium_quality": {
        "flag": "-qm",
        "description": "Medium Quality (Balanced)",
        "estimated_time": 180,  # seconds
        "resolution": "720p"
    }
}

# Application Settings
APP_SETTINGS = {
    "max_render_time": 300,  # seconds
    "max_prompt_length": 1000,
    "min_prompt_length": 10,
    "default_video_quality": "medium_quality",
    "temp_file_prefix": "manim_",
    "log_level": "INFO"
}

# UI Settings
UI_SETTINGS = {
    "page_title": "Manim Video Generator",
    "page_icon": "🎬",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "theme": {
        "primaryColor": "#667eea",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#f8f9fa",
        "textColor": "#262730",
        "font": "sans serif"
    }
}

def get_setting(key: str, default: Any = None) -> Any:
    if key in APP_SETTINGS:
        return APP_SETTINGS[key]
    if key in UI_SETTINGS:
        return UI_SETTINGS[key]
    return default

def update_setting(key: str, value: Any) -> None:
    if key in APP_SETTINGS:
        APP_SETTINGS[key] = value
    elif key in UI_SETTINGS:
        UI_SETTINGS[key] = value
    else:
        raise KeyError(f"Setting '{key}' not found") 