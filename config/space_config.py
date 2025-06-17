import os

# Space-specific settings
SPACE_CONFIG = {
    "max_render_time": 300,  # 5 minutes max render time
    "max_video_size_mb": 50,  # Maximum video size in MB
    "allowed_models": [
        "llama-3.3-70b-versatile",
        "llama3-8b-8192"
    ],
    "default_quality": "medium_quality",
    "cache_ttl": 3600,  # Cache time-to-live in seconds
    "max_concurrent_renders": 2,
    "temp_dir": "/tmp/manimate",  # Space-specific temp directory
    "output_dir": "/tmp/manimate/output",  # Space-specific output directory
}

# Environment variables
ENV_VARS = {
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
    "SPACE_ID": os.getenv("SPACE_ID", ""),
    "SPACE_HOST": os.getenv("SPACE_HOST", ""),
}

# Performance settings
PERFORMANCE_CONFIG = {
    "quality_settings": {
        "low_quality": {
            "flag": "-ql",
            "description": "Low Quality (Fast)",
            "max_duration": 10,
            "max_objects": 20
        },
        "medium_quality": {
            "flag": "-qm",
            "description": "Medium Quality (Balanced)",
            "max_duration": 15,
            "max_objects": 30
        }
    },
    "memory_limit_mb": 2048,  # 2GB memory limit
    "cpu_limit": 2,  # CPU core limit
}

# UI settings
UI_CONFIG = {
    "theme": "light",
    "max_prompt_length": 500,
    "show_advanced_options": False,
    "enable_metrics": True,
    "enable_error_reporting": True
}

AVAILABLE_MODELS = [
    "llama-3.3-70b-versatile",
    "llama3-8b-8192"
]

QUALITY_SETTINGS = {
    "low_quality": {
        "flag": "-ql",
        "description": "Low Quality (Fast)",
        "resolution": "480p",
        "fps": 30
    },
    "medium_quality": {
        "flag": "-qm",
        "description": "Medium Quality (Balanced)",
        "resolution": "720p",
        "fps": 30
    }
}

def get_space_config():
    """Get the current space configuration."""
    return {
        "space": SPACE_CONFIG,
        "env": ENV_VARS,
        "performance": PERFORMANCE_CONFIG,
        "ui": UI_CONFIG
    } 