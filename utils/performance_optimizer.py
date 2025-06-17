"""
Performance optimization utilities for Manim rendering
"""

import re
from typing import Dict, Tuple

# Quality settings for different performance levels
QUALITY_SETTINGS = {
    "low_quality": {
        "flag": "-ql",
        "description": "Low Quality (Fast)",
        "resolution": "480p",
        "fps": 30,
        "max_duration": 10,
        "max_objects": 20,
        "performance_threshold": {
            "render_time": 60,  # seconds
            "memory_usage": 1024  # MB
        }
    },
    "medium_quality": {
        "flag": "-qm",
        "description": "Medium Quality (Balanced)",
        "resolution": "720p",
        "fps": 30,
        "max_duration": 15,
        "max_objects": 30,
        "performance_threshold": {
            "render_time": 180,  # seconds
            "memory_usage": 2048  # MB
        }
    }
}

class PerformanceOptimizer:
    """Optimize rendering performance and resource usage"""
    
    # Performance thresholds
    RENDER_TIME_THRESHOLDS = {
        "low_quality": 60,
        "medium_quality": 180
    }
    
    # Memory usage thresholds (in GB)
    MEMORY_THRESHOLDS = {
        "low_quality": 4.0,
        "medium_quality": 6.0
    }
    
    @classmethod
    def estimate_render_time(cls, quality: str, complexity: str = "medium") -> int:
        """Estimate rendering time in seconds"""
        base_times = {
            "low_quality": 30,
            "medium_quality": 60,
            "high_quality": 120,
            "production_quality": 300
        }
        
        complexity_multipliers = {
            "simple": 0.5,
            "medium": 1.0,
            "complex": 2.0,
            "very_complex": 3.0
        }
        
        base_time = base_times.get(quality, 60)
        multiplier = complexity_multipliers.get(complexity, 1.0)
        
        return int(base_time * multiplier)
    
    @classmethod
    def analyze_code_complexity(cls, code: str) -> str:
        """Analyze code complexity to estimate render time"""
        complexity_indicators = {
            "simple": ["Text", "Write", "Create"],
            "medium": ["Transform", "FadeIn", "FadeOut", "MoveTo"],
            "complex": ["Axes", "plot", "FunctionGraph", "BarChart"],
            "very_complex": ["ThreeDScene", "rotate", "complex", "integral"]
        }
        
        code_lower = code.lower()
        scores = {"simple": 0, "medium": 0, "complex": 0, "very_complex": 0}
        
        for complexity, indicators in complexity_indicators.items():
            for indicator in indicators:
                scores[complexity] += code_lower.count(indicator.lower())
        
        # Determine overall complexity
        max_score = max(scores.values())
        if max_score == 0:
            return "simple"
        
        return max(scores, key=scores.get)
    
    @classmethod
    def get_recommended_quality(cls, prompt_length: int, has_complex_math: bool) -> str:
        """Recommend quality based on prompt complexity"""
        if prompt_length < 50 and not has_complex_math:
            return "medium_quality"
        elif prompt_length < 100:
            return "medium_quality" 
        else:
            return "low_quality"  # Start with lower quality for complex animations
    
    @classmethod
    def optimize_code_for_performance(cls, code: str) -> str:
        """Optimize Manim code for better performance"""
        optimized_code = code
        
        # Limit excessive wait times
        optimized_code = re.sub(r'self\.wait\((\d+)\)', 
                               lambda m: f'self.wait({min(int(m.group(1)), 3)})', 
                               optimized_code)
        
        # Optimize animation run times
        optimized_code = re.sub(r'run_time=(\d+)', 
                               lambda m: f'run_time={min(int(m.group(1)), 5)}', 
                               optimized_code)
        
        # Add performance hints as comments
        performance_hints = [
            "# Performance optimized: Limited wait times to 3 seconds max",
            "# Performance optimized: Limited animation run times to 5 seconds max"
        ]
        
        if any(hint.split(": ")[1] in optimized_code for hint in performance_hints):
            optimized_code = "\n".join(performance_hints) + "\n" + optimized_code
        
        return optimized_code
    
    @classmethod
    def get_memory_efficient_settings(cls) -> Dict[str, str]:
        """Get settings for memory-efficient rendering"""
        return {
            "preview": True,
            "disable_caching": True,
            "low_quality": True,
            "save_last_frame": False,
            "write_to_movie": True
        }
    
    @classmethod
    def calculate_estimated_file_size(cls, quality: str, duration: int = 10) -> Tuple[float, str]:
        """Calculate estimated output file size in MB"""
        # Rough estimates based on quality settings
        bitrate_estimates = {
            "low_quality": 1.0,  # MB per minute
            "medium_quality": 3.0,
            "high_quality": 8.0,
            "production_quality": 25.0
        }
        
        bitrate = bitrate_estimates.get(quality, 3.0)
        size_mb = (bitrate * duration) / 60  # Convert to actual duration
        
        if size_mb < 1:
            return size_mb * 1024, "KB"
        else:
            return size_mb, "MB"
    
    @classmethod
    def get_optimization_tips(cls, quality: str, complexity: str) -> list:
        """Get optimization tips based on settings"""
        tips = []
        
        if quality in ["high_quality", "production_quality"]:
            tips.append("Consider using medium quality for faster rendering during development")
        
        if complexity in ["complex", "very_complex"]:
            tips.append("Break complex animations into smaller scenes for easier debugging")
            tips.append("Use preview mode (-p flag) to quickly test animations")
        
        tips.append("Close other applications to free up system resources")
        tips.append("Ensure sufficient disk space for temporary files")
        
        return tips

    def optimize_quality(self, available_memory: float, estimated_render_time: float) -> str:
        if available_memory < self.MEMORY_THRESHOLDS["low_quality"]:
            return "low_quality"
        if estimated_render_time > self.RENDER_TIME_THRESHOLDS["medium_quality"]:
            return "low_quality"
        return "medium_quality"

    @staticmethod
    def estimate_render_time(quality_level: str) -> int:
        """Estimate render time based on quality level"""
        return QUALITY_SETTINGS[quality_level]["performance_threshold"]["render_time"]
    
    @staticmethod
    def get_quality_settings(quality_level: str) -> dict:
        """Get quality settings for the specified level"""
        return QUALITY_SETTINGS[quality_level]
    
    @staticmethod
    def optimize_for_performance(quality_level: str, scene_complexity: int) -> dict:
        """Optimize settings based on quality level and scene complexity"""
        settings = QUALITY_SETTINGS[quality_level].copy()
        
        # Adjust settings based on scene complexity
        if scene_complexity > settings["max_objects"]:
            settings["max_objects"] = min(scene_complexity, settings["max_objects"] * 2)
        
        return settings