"""Metrics collection and analysis utilities."""

import time
import logging
from typing import Dict, Any, List, Optional
from collections import defaultdict
from datetime import datetime

from config.constants import VideoQuality

logger = logging.getLogger(__name__)

class MetricsCollector:
    """Collects and analyzes application metrics."""
    
    def __init__(self):
        """Initialize the metrics collector."""
        self.generation_attempts = 0
        self.successful_renders = 0
        self.failed_renders = 0
        self.render_times: List[float] = []
        self.error_counts = defaultdict(int)
        self.quality_usage = defaultdict(int)
        self.scene_types = defaultdict(int)
        self.start_time = time.time()
    
    def record_generation_attempt(self) -> None:
        """Record a new generation attempt."""
        self.generation_attempts += 1
        logger.debug(f"Recorded generation attempt #{self.generation_attempts}")
    
    def record_successful_render(
        self,
        render_time: float,
        scene_type: str,
        quality: str
    ) -> None:
        """Record a successful render.
        
        Args:
            render_time: Time taken to render in seconds
            scene_type: Type of scene rendered
            quality: Video quality setting used
        """
        self.successful_renders += 1
        self.render_times.append(render_time)
        self.quality_usage[quality] += 1
        self.scene_types[scene_type] += 1
        
        logger.debug(
            f"Recorded successful render: {render_time:.2f}s, "
            f"quality={quality}, type={scene_type}"
        )
    
    def record_failed_render(self, error_type: str) -> None:
        """Record a failed render.
        
        Args:
            error_type: Type of error that caused the failure
        """
        self.failed_renders += 1
        self.error_counts[error_type] += 1
        
        logger.debug(f"Recorded failed render: {error_type}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of collected metrics.
        
        Returns:
            Dictionary containing metrics summary
        """
        total_renders = self.successful_renders + self.failed_renders
        
        if not total_renders:
            return {
                "success_rate": 0.0,
                "average_render_time": 0.0,
                "most_popular_quality": "N/A",
                "total_attempts": 0,
                "error_distribution": {},
                "quality_distribution": {},
                "scene_type_distribution": {},
                "uptime": self._get_uptime()
            }
        
        # Calculate success rate
        success_rate = (self.successful_renders / total_renders) * 100
        
        # Calculate average render time
        avg_render_time = (
            sum(self.render_times) / len(self.render_times)
            if self.render_times else 0.0
        )
        
        # Find most popular quality setting
        most_popular_quality = max(
            self.quality_usage.items(),
            key=lambda x: x[1],
            default=(VideoQuality.MEDIUM.value, 0)
        )[0]
        
        return {
            "success_rate": success_rate,
            "average_render_time": avg_render_time,
            "most_popular_quality": most_popular_quality,
            "total_attempts": self.generation_attempts,
            "error_distribution": dict(self.error_counts),
            "quality_distribution": dict(self.quality_usage),
            "scene_type_distribution": dict(self.scene_types),
            "uptime": self._get_uptime()
        }
    
    def _get_uptime(self) -> str:
        """Get application uptime in a human-readable format."""
        uptime_seconds = time.time() - self.start_time
        
        if uptime_seconds < 60:
            return f"{uptime_seconds:.0f} seconds"
        elif uptime_seconds < 3600:
            minutes = uptime_seconds / 60
            return f"{minutes:.1f} minutes"
        elif uptime_seconds < 86400:
            hours = uptime_seconds / 3600
            return f"{hours:.1f} hours"
        else:
            days = uptime_seconds / 86400
            return f"{days:.1f} days"
    
    def reset(self) -> None:
        """Reset all metrics to initial state."""
        self.__init__()
        logger.info("Metrics collector reset")
    
    def export_metrics(self, filepath: Optional[str] = None) -> Dict[str, Any]:
        """Export metrics to a file or return as dictionary.
        
        Args:
            filepath: Optional path to save metrics to JSON file
            
        Returns:
            Dictionary containing all metrics
        """
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.get_summary(),
            "raw_data": {
                "generation_attempts": self.generation_attempts,
                "successful_renders": self.successful_renders,
                "failed_renders": self.failed_renders,
                "render_times": self.render_times,
                "error_counts": dict(self.error_counts),
                "quality_usage": dict(self.quality_usage),
                "scene_types": dict(self.scene_types)
            }
        }
        
        if filepath:
            import json
            try:
                with open(filepath, 'w') as f:
                    json.dump(metrics, f, indent=2)
                logger.info(f"Metrics exported to {filepath}")
            except Exception as e:
                logger.error(f"Error exporting metrics: {e}")
        
        return metrics


# Global metrics collector instance
metrics_collector = MetricsCollector()