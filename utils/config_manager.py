"""
Configuration management for the Manim Video Generator
"""

from typing import List, Any


class ConfigManager:
    """Manage application configuration and settings"""
    
    DEFAULT_CONFIG = {
        "max_render_time": 300,  # 5 minutes
        "temp_dir_cleanup": True,
        "log_level": "INFO",
        "default_quality": "medium_quality",
        "default_model": "llama-3.3-70b-versatile",
        "max_prompt_length": 1000,
        "enable_caching": True,
        "ffmpeg_timeout": 180  # 3 minutes
    }
    
    @classmethod
    def get_config(cls, key: str, default=None) -> Any:
        """Get configuration value"""
        return cls.DEFAULT_CONFIG.get(key, default)
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """Validate current configuration"""
        issues = []
        
        if cls.get_config("max_render_time") < 60:
            issues.append("Max render time should be at least 60 seconds")
        
        if cls.get_config("max_prompt_length") < 10:
            issues.append("Max prompt length should be at least 10 characters")
        
        return issues