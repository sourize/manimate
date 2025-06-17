"""
Error handling utilities for Manim Video Generator
"""

from typing import Dict, List, Optional
import re
import logging
from config.constants import ErrorType

logger = logging.getLogger(__name__)

class ErrorHandler:
    """Handle and provide helpful error messages"""
    
    COMMON_ERRORS = {
        "ImportError": {
            "message": "Missing required packages. Please ensure all dependencies are installed.",
            "solution": "Run: pip install -r requirements.txt"
        },
        "SyntaxError": {
            "message": "The generated code has syntax errors.",
            "solution": "Try regenerating with a more specific prompt or different model."
        },
        "AttributeError": {
            "message": "Invalid Manim object or method used.",
            "solution": "The AI may have used outdated Manim syntax. Try a different model."
        },
        "TimeoutError": {
            "message": "Rendering took too long and was cancelled.",
            "solution": "Try using lower quality settings or simplify your prompt."
        },
        "FFmpegError": {
            "message": "Video encoding failed.",
            "solution": "Check if FFmpeg is properly installed and accessible."
        },
        "FileNotFoundError": {
            "message": "Required system command not found.",
            "solution": "Ensure Manim and FFmpeg are properly installed and in PATH."
        },
        "MemoryError": {
            "message": "Insufficient memory to complete rendering.",
            "solution": "Try lower quality settings or restart the application."
        },
        "PermissionError": {
            "message": "Insufficient permissions to write output files.",
            "solution": "Check file permissions and available disk space."
        }
    }
    
    ERROR_PATTERNS = {
        r"No module named '(\w+)'": "ImportError",
        r"invalid syntax": "SyntaxError", 
        r"'(\w+)' object has no attribute '(\w+)'": "AttributeError",
        r"Timed out": "TimeoutError",
        r"ffmpeg.*not found": "FFmpegError",
        r"No such file or directory": "FileNotFoundError",
        r"MemoryError": "MemoryError",
        r"Permission denied": "PermissionError"
    }
    
    # Error type to user-friendly message mapping
    ERROR_MESSAGES = {
        ErrorType.RENDERING_ERROR: {
            "user_message": "Failed to render the animation. Please try again with a simpler scene or lower quality.",
            "suggestions": [
                "Try reducing the complexity of your animation",
                "Lower the video quality setting",
                "Check if Manim is properly installed",
                "Ensure you have enough system resources"
            ]
        },
        ErrorType.CODE_GENERATION_ERROR: {
            "user_message": "Failed to generate animation code. Please try rephrasing your prompt.",
            "suggestions": [
                "Make your prompt more specific and clear",
                "Try a different AI model",
                "Break down complex animations into simpler parts",
                "Check the example prompts for inspiration"
            ]
        },
        ErrorType.PROMPT_ERROR: {
            "user_message": "Error processing your prompt. Please try again with a clearer description.",
            "suggestions": [
                "Be more specific about what you want to animate",
                "Include mathematical concepts and visual elements",
                "Mention colors and timing preferences",
                "Keep the description focused and concise"
            ]
        },
        ErrorType.SYSTEM_ERROR: {
            "user_message": "A system error occurred. Please try again or contact support.",
            "suggestions": [
                "Refresh the page and try again",
                "Check your internet connection",
                "Ensure you have the latest version of the application",
                "Clear your browser cache"
            ]
        },
        ErrorType.VALIDATION_ERROR: {
            "user_message": "The generated code has validation errors. Please try again.",
            "suggestions": [
                "Try a simpler animation",
                "Use a different AI model",
                "Check the example prompts for reference",
                "Make your prompt more specific"
            ]
        },
        ErrorType.TIMEOUT_ERROR: {
            "user_message": "The operation took too long to complete. Please try again with simpler settings.",
            "suggestions": [
                "Lower the video quality setting",
                "Simplify your animation",
                "Try a faster AI model",
                "Break down complex animations into parts"
            ]
        },
        ErrorType.API_ERROR: {
            "user_message": "Error communicating with the AI service. Please try again.",
            "suggestions": [
                "Check your API key",
                "Verify your internet connection",
                "Try again in a few minutes",
                "Contact support if the issue persists"
            ]
        }
    }
    
    @classmethod
    def classify_error(cls, error_message: str) -> str:
        """Classify error based on message patterns"""
        error_lower = error_message.lower()
        
        for pattern, error_type in cls.ERROR_PATTERNS.items():
            if re.search(pattern, error_lower):
                return error_type
        
        return "UnknownError"
    
    @classmethod
    def handle_error(cls, error_type: ErrorType, error_message: str) -> None:
        """Handle an error by logging it and potentially taking additional actions.
        
        Args:
            error_type: Type of error that occurred
            error_message: Detailed error message
        """
        logger.error(f"{error_type.name}: {error_message}")
        
        # Additional error handling logic can be added here
        # For example, sending error reports, updating metrics, etc.
    
    @classmethod
    def get_user_friendly_error(cls, error_type: str, error_message: str) -> Dict[str, str]:
        """Get user-friendly error message and suggestions.
        
        Args:
            error_type: Type of error (can be ErrorType or string)
            error_message: Original error message
            
        Returns:
            Dictionary containing user-friendly message and suggestions
        """
        # Try to match error type
        if isinstance(error_type, ErrorType):
            error_info = cls.ERROR_MESSAGES.get(error_type)
        else:
            # Try to infer error type from message
            error_type = cls._infer_error_type(error_message)
            error_info = cls.ERROR_MESSAGES.get(error_type)
        
        if not error_info:
            # Fallback to generic error
            error_info = {
                "user_message": "An unexpected error occurred. Please try again.",
                "suggestions": [
                    "Refresh the page",
                    "Try a different prompt",
                    "Check your settings",
                    "Contact support if the issue persists"
                ]
            }
        
        return error_info
    
    @classmethod
    def suggest_fixes(cls, error_message: str) -> List[str]:
        """Get suggested fixes for an error.
        
        Args:
            error_message: The error message to analyze
            
        Returns:
            List of suggested fixes
        """
        error_type = cls._infer_error_type(error_message)
        error_info = cls.ERROR_MESSAGES.get(error_type)
        
        if error_info and "suggestions" in error_info:
            return error_info["suggestions"]
        
        return [
            "Try again with different settings",
            "Simplify your animation",
            "Check the example prompts",
            "Contact support if the issue persists"
        ]
    
    @classmethod
    def _infer_error_type(cls, error_message: str) -> ErrorType:
        """Infer the type of error from the error message.
        
        Args:
            error_message: The error message to analyze
            
        Returns:
            Inferred ErrorType
        """
        error_message_lower = error_message.lower()
        
        for pattern, error_type in cls.ERROR_PATTERNS.items():
            if pattern in error_message_lower:
                return error_type
        
        return ErrorType.SYSTEM_ERROR  # Default to system error if no pattern matches
    
    @classmethod
    def get_debug_info(cls, error_message: str, code: str = None) -> Dict[str, any]:
        """Get detailed debug information for error reporting"""
        debug_info = {
            "error_type": cls.classify_error(error_message),
            "error_message": error_message,
            "suggested_fixes": cls.suggest_fixes(error_message),
            "timestamp": None,  # Would be set by caller
            "code_length": len(code) if code else None,
            "has_imports": "from manim import" in code if code else None,
            "has_scene_class": "class" in code and "Scene" in code if code else None
        }
        
        return debug_info
    
    @classmethod
    def format_error_for_display(cls, error_info: Dict[str, str]) -> str:
        """Format error information for user display"""
        formatted = f"❌ **{error_info['user_message']}**\n\n"
        formatted += f"💡 **Solution:** {error_info['solution']}\n\n"
        
        if error_info.get('technical_details'):
            formatted += f"🔧 **Technical Details:** {error_info['technical_details']}"
        
        return formatted
    
    @classmethod
    def is_recoverable_error(cls, error_type: str) -> bool:
        """Determine if an error is recoverable with user action"""
        recoverable_errors = [
            "SyntaxError", "AttributeError", "TimeoutError", 
            "ImportError", "FileNotFoundError"
        ]
        return error_type in recoverable_errors
    
    @classmethod
    def get_error_severity(cls, error_type: str) -> str:
        """Get error severity level"""
        severity_map = {
            "ImportError": "high",
            "FFmpegError": "high", 
            "MemoryError": "high",
            "SyntaxError": "medium",
            "AttributeError": "medium",
            "TimeoutError": "medium",
            "FileNotFoundError": "low",
            "PermissionError": "low"
        }
        return severity_map.get(error_type, "medium")
    
    @classmethod
    def create_error_report(cls, error_type: str, error_message: str, code: str = None) -> Dict:
        """Create a comprehensive error report"""
        error_info = cls.get_user_friendly_error(error_type, error_message)
        debug_info = cls.get_debug_info(error_message, code)
        
        return {
            "error_info": error_info,
            "debug_info": debug_info,
            "severity": cls.get_error_severity(error_type),
            "recoverable": cls.is_recoverable_error(error_type),
            "formatted_message": cls.format_error_for_display(error_info)
        }