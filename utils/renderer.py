"""Video rendering utilities."""

import os
import time
import logging
import subprocess
from pathlib import Path
from typing import Tuple, Optional

from config.settings import QUALITY_SETTINGS, APP_SETTINGS
from config.constants import (
    ErrorType,
    FILE_CONSTANTS,
    VideoQuality
)
from utils.error_handler import ErrorHandler

logger = logging.getLogger(__name__)

class VideoRenderer:
    """Handles Manim video rendering."""
    
    def __init__(
        self,
        code_file: str,
        temp_dir: str,
        quality: str = VideoQuality.MEDIUM.value,
        metrics: Optional[Any] = None
    ):
        """Initialize the video renderer.
        
        Args:
            code_file: Path to the Python file containing the Manim scene
            temp_dir: Directory to store temporary files
            quality: Video quality setting
            metrics: Optional metrics collector instance
        """
        self.code_file = code_file
        self.temp_dir = temp_dir
        self.quality = quality
        self.metrics = metrics
        self.start_time = None
    
    def _get_quality_settings(self) -> dict:
        """Get quality settings for the current quality level."""
        return QUALITY_SETTINGS.get(
            self.quality,
            QUALITY_SETTINGS[VideoQuality.MEDIUM.value]
        )
    
    def _build_manim_command(self) -> list:
        """Build the Manim command with appropriate flags."""
        quality_settings = self._get_quality_settings()
        
        return [
            "manim",
            "render",
            quality_settings["flag"],
            self.code_file,
            "GeneratedScene",
            "--output_file", FILE_CONSTANTS["OUTPUT_FILE_NAME"],
            "--media_dir", self.temp_dir
        ]
    
    def _find_output_video(self) -> Optional[str]:
        """Find the generated video file."""
        video_files = list(Path(self.temp_dir).rglob(f"*{FILE_CONSTANTS['VIDEO_EXTENSION']}"))
        return str(video_files[0]) if video_files else None
    
    def _record_metrics(self, success: bool, error_type: Optional[str] = None) -> None:
        """Record rendering metrics if metrics collector is available."""
        if self.metrics and self.start_time:
            render_time = time.time() - self.start_time
            if success:
                self.metrics.record_successful_render(
                    render_time,
                    "unknown",  # TODO: Add scene type detection
                    self.quality
                )
            else:
                self.metrics.record_failed_render(error_type or "UnknownError")
    
    def render(self) -> Tuple[bool, str, str]:
        """Render the Manim video.
        
        Returns:
            Tuple containing:
            - Success flag
            - Result message or error message
            - Log output
        """
        self.start_time = time.time()
        
        try:
            # Build and run command
            cmd = self._build_manim_command()
            logger.info(f"Running command: {' '.join(cmd)}")
            
            process = subprocess.run(
                cmd,
                cwd=self.temp_dir,
                capture_output=True,
                text=True,
                timeout=APP_SETTINGS["max_render_time"]
            )
            
            if process.returncode == 0:
                # Find and verify video file
                video_file = self._find_output_video()
                if video_file:
                    self._record_metrics(True)
                    return True, video_file, process.stdout
                else:
                    self._record_metrics(False, "NoVideoFile")
                    return False, "No video file generated", process.stderr
            else:
                self._record_metrics(False, "RenderingFailed")
                return False, process.stderr, process.stdout
                
        except subprocess.TimeoutExpired:
            self._record_metrics(False, "TimeoutError")
            return False, "Rendering timeout exceeded", ""
            
        except Exception as e:
            logger.error(f"Error rendering video: {e}")
            self._record_metrics(False, "RenderingError")
            ErrorHandler.handle_error(ErrorType.RENDERING_ERROR, str(e))
            return False, f"Rendering error: {str(e)}", ""
    
    @property
    def estimated_render_time(self) -> int:
        """Get estimated render time in seconds."""
        return self._get_quality_settings()["estimated_time"]
    
    @property
    def resolution(self) -> str:
        """Get video resolution for current quality setting."""
        return self._get_quality_settings()["resolution"] 