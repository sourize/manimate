import os
import logging
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Tuple, Dict, Any

from groq import Groq
from config.settings import (
    GROQ_API_BASE_URL,
    DEFAULT_MODEL,
    AVAILABLE_MODELS,
    QUALITY_SETTINGS,
    APP_SETTINGS,
    TEMP_DIR
)
from config.constants import (
    ModelType,
    VideoQuality,
    ErrorType,
    FILE_CONSTANTS,
    ANIMATION_CONSTANTS
)
from utils.code_validator import CodeValidator
from utils.prompt_manager import PromptManager
from utils.error_handler import ErrorHandler
from utils.metrics_collector import MetricsCollector

logger = logging.getLogger(__name__)

class ManimVideoGenerator:
    
    def __init__(self, groq_api_key: str):
        self.client = Groq(api_key=groq_api_key)
        self.available_models = AVAILABLE_MODELS
        self.temp_dir = None
        self.metrics = MetricsCollector()
        self.prompt_manager = PromptManager()
        self.code_validator = CodeValidator()
        
    def enhance_prompt(self, user_prompt: str, model: str = DEFAULT_MODEL) -> str:
        try:
            model_config = self.available_models[model]
            return self.prompt_manager.enhance_prompt(
                user_prompt,
                self.client,
                model,
                temperature=model_config["temperature"],
                max_tokens=model_config["max_tokens"]
            )
        except Exception as e:
            logger.error(f"Error enhancing prompt: {e}")
            ErrorHandler.handle_error(ErrorType.PROMPT_ERROR, str(e))
            return user_prompt
    
    def generate_manim_code(self, enhanced_prompt: str, model: str = DEFAULT_MODEL) -> str:
        try:
            model_config = self.available_models[model]
            return self.prompt_manager.generate_code(
                enhanced_prompt,
                self.client,
                model,
                temperature=0.3,  # Lower temperature for code generation
                max_tokens=model_config["max_tokens"]
            )
        except Exception as e:
            logger.error(f"Error generating Manim code: {e}")
            ErrorHandler.handle_error(ErrorType.CODE_GENERATION_ERROR, str(e))
            raise
    
    def process_and_validate_code(self, raw_code: str) -> str:
        try:
            cleaned_code = self.code_validator.fix_common_issues(raw_code)
            
            validation_result = self.code_validator.validate_code(cleaned_code)
            if not validation_result["is_valid"]:
                raise ValueError(validation_result["error_message"])
            
            return cleaned_code
        except Exception as e:
            logger.error(f"Error validating code: {e}")
            ErrorHandler.handle_error(ErrorType.VALIDATION_ERROR, str(e))
            raise
    
    def create_temp_directory(self) -> str:
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        
        self.temp_dir = tempfile.mkdtemp(
            prefix=FILE_CONSTANTS["TEMP_DIR_PREFIX"],
            dir=TEMP_DIR
        )
        return self.temp_dir
    
    def save_code_to_file(self, code: str, temp_dir: str) -> str:
        code_file = os.path.join(temp_dir, FILE_CONSTANTS["SCENE_FILE_NAME"])
        try:
            with open(code_file, 'w', encoding='utf-8') as f:
                f.write(code)
            return code_file
        except Exception as e:
            logger.error(f"Error saving code to file: {e}")
            ErrorHandler.handle_error(ErrorType.SYSTEM_ERROR, str(e))
            raise
    
    def render_video(
        self,
        code_file: str,
        temp_dir: str,
        quality: str = VideoQuality.MEDIUM.value
    ) -> Tuple[bool, str, str]:
        from utils.renderer import VideoRenderer
        
        try:
            renderer = VideoRenderer(
                code_file=code_file,
                temp_dir=temp_dir,
                quality=quality,
                metrics=self.metrics
            )
            
            return renderer.render()
            
        except Exception as e:
            logger.error(f"Error rendering video: {e}")
            ErrorHandler.handle_error(ErrorType.RENDERING_ERROR, str(e))
            return False, str(e), ""
    
    def cleanup(self) -> None:
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                logger.info(f"Cleaned up temporary directory: {self.temp_dir}")
            except Exception as e:
                logger.error(f"Error cleaning up: {e}")
                ErrorHandler.handle_error(ErrorType.SYSTEM_ERROR, str(e))
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        return self.metrics.get_summary()
    
    @property
    def model_options(self) -> Dict[str, str]:
        return {
            model_id: f"{config['name']} ({config['description']})"
            for model_id, config in self.available_models.items()
        }
    
    @property
    def quality_options(self) -> Dict[str, str]:
        return {
            quality_id: config["description"]
            for quality_id, config in QUALITY_SETTINGS.items()
        } 