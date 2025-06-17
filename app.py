import streamlit as st
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
import time
from groq import Groq
import logging
from typing import Optional, Tuple
from dotenv import load_dotenv
from utils.code_validator import CodeValidator
from utils.prompt_templates import PromptTemplates
from utils.system_checker import SystemChecker
from utils.performance_optimizer import PerformanceOptimizer
from utils.error_handler import ErrorHandler
from utils.config_manager import ConfigManager
from utils.metrics_collector import MetricsCollector
from utils.ui_components import (
    initialize_app,
    render_header,
    render_sidebar,
    render_main_interface,
    render_footer
)
import re
import ast

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ManimVideoGenerator:
    
    def __init__(self, groq_api_key: str):
        self.client = Groq(api_key=groq_api_key)
        self.available_models = {
            "llama-3.3-70b-versatile": "Llama 3.3 70B",
            "llama3-8b-8192": "Llama 3 8B"
        }
        self.temp_dir = None
        self.metrics = MetricsCollector()
        
    def enhance_prompt(self, user_prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
        if model not in self.available_models:
            logger.warning(f"Model {model} not available, using default")
            model = "llama-3.3-70b-versatile"
        
        category_context = PromptTemplates.get_enhancement_context(user_prompt)
        
        enhancement_prompt = f"""
You are an expert at creating detailed prompts for Manim (Mathematical Animation Engine) video generation.

User's original prompt: "{user_prompt}"

Context: {category_context}

Please enhance this prompt by:
1. Adding specific mathematical or visual details
2. Suggesting appropriate Manim objects and animations  
3. Specifying colors, positioning, and timing
4. Including educational context if applicable
5. Making it clear and comprehensive for code generation

Enhanced prompt should be detailed but concise, focusing on visual elements that can be animated with Manim.

Return only the enhanced prompt, nothing else.
"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": enhancement_prompt}],
                model=model,
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error enhancing prompt: {e}")
            return user_prompt
    
    def generate_manim_code(self, enhanced_prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
        
        if model not in self.available_models:
            logger.warning(f"Model {model} not available, using default")
            model = "llama-3.3-70b-versatile"
        
        system_message = """You are a Manim expert. Generate clean, working Python code for mathematical animations.

STRICT REQUIREMENTS:
1. Start with: from manim import *
2. Use: class GeneratedScene(Scene):
3. Use: def construct(self):
4. Include self.play() and self.wait()
5. Use simple objects: Circle, Square, Text, Line, Arrow, Dot
6. Use basic colors: BLUE, RED, GREEN, WHITE, YELLOW
7. Keep animations simple and working
8. NO complex loops or advanced features
9. Return ONLY the Python code
10. NO markdown formatting or code blocks
11. All strings must be properly quoted
12. No syntax errors allowed"""

        user_prompt = f"""Create a simple Manim animation for: {enhanced_prompt}

Use this exact template structure:

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Create simple objects
        obj = Circle(color=BLUE)
        
        # Simple animations
        self.play(Create(obj))
        self.wait(1)
        
        # One more animation
        self.play(obj.animate.shift(RIGHT))
        self.wait(1)

Replace the Circle with appropriate objects for: {enhanced_prompt}
Keep it simple and working. Available objects: Circle, Square, Rectangle, Text, MathTex, Line, Arrow, Dot
Available animations: Create, Write, FadeIn, FadeOut, GrowFromCenter
Available colors: BLUE, RED, GREEN, WHITE, YELLOW, BLACK, GRAY

IMPORTANT: Make sure all Text objects use double quotes like Text("hello")
Return only the complete working Python code."""

        max_attempts = 3
        
        for attempt in range(max_attempts):
            try:
                logger.info(f"Generating Manim code (attempt {attempt + 1}/{max_attempts})...")
                
                response = self.client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_prompt}
                    ],
                    model=model,
                    temperature=0.1,
                    max_tokens=800,
                    stop=["```", "Note:", "Example:"]
                )
                
                generated_code = response.choices[0].message.content.strip()
                
                generated_code = self._clean_generated_code(generated_code)
                
                if self._validate_code_structure(generated_code):
                    logger.info("Generated valid code")
                    logger.info("-" * 40)
                    logger.info(generated_code)
                    logger.info("-" * 40)
                    return generated_code
                else:
                    logger.warning(f"Generated code failed validation on attempt {attempt + 1}")
                    if attempt < max_attempts - 1:
                        user_prompt = self._get_simpler_prompt(enhanced_prompt)
                    
            except Exception as e:
                logger.error(f"Error generating Manim code on attempt {attempt + 1}: {e}")
                if attempt < max_attempts - 1:
                    continue
        
        logger.warning("All generation attempts failed, using emergency fallback")
        return self._generate_emergency_fallback(enhanced_prompt)

    def _get_simpler_prompt(self, enhanced_prompt: str) -> str:
        return f"""Generate the simplest possible Manim code for: {enhanced_prompt}

Use exactly this structure:

from manim import *

class GeneratedScene(Scene):
    def construct(self):
        shape = Circle(color=BLUE)
        self.play(Create(shape))
        self.wait(2)

Change only the shape and color to match the request.
Available: Circle, Square, Rectangle, Text("hello")
Colors: BLUE, RED, GREEN, WHITE, YELLOW
Keep it extremely simple. Return only the code."""

    def _clean_generated_code(self, code: str) -> str:
        code = re.sub(r'```python\n?', '', code)
        code = re.sub(r'```\n?', '', code)
        code = code.replace('```', '')
        code = code.replace('`', '')
        
        lines = code.split('\n')
        code_lines = []
        found_start = False
        
        for line in lines:
            stripped = line.strip()
            
            if not found_start:
                if (stripped.startswith('from manim') or 
                    stripped.startswith('import manim') or
                    stripped.startswith('class GeneratedScene')):
                    found_start = True
                    code_lines.append(line)
                    continue
                else:
                    continue
            
            if (stripped.startswith('Here') or 
                stripped.startswith('This code') or 
                stripped.startswith('The animation') or
                stripped.startswith('Note:')):
                continue
                
            code_lines.append(line)
        
        code = '\n'.join(code_lines)
        
        code = self._fix_string_literals(code)
        
        code = self._fix_syntax_issues(code)
        
        if not re.search(r'from manim import \*', code):
            code = 'from manim import *\n\n' + code
        
        return code.strip()

    def _fix_string_literals(self, code: str) -> str:
        lines = code.split('\n')
        fixed_lines = []
        
        for line in lines:
            line = re.sub(r'Text\(([^"\'()\[\]]*?)\)', r'Text("\1")', line)
            
            line = re.sub(r'Text\(([^"\']*?), font_size', r'Text("\1", font_size', line)
            
            if line.count('"') % 2 != 0:
                if 'Text(' in line and not line.strip().endswith('"'):
                    line = re.sub(r'([^"]*?)(,|\))', r'\1"\2', line)
            
            if line.count("'") % 2 != 0:
                if 'Text(' in line:
                    line = line.replace("'", '"')
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)

    def _fix_syntax_issues(self, code: str) -> str:
        lines = code.split('\n')
        fixed_lines = []
        
        in_for_loop = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            if stripped.startswith('for ') and stripped.endswith(':'):
                in_for_loop = True
                fixed_lines.append(line)
                continue
            
            if in_for_loop:
                if not stripped or not line.startswith('    '):
                    fixed_lines.append('        pass')
                    in_for_loop = False
            
            if re.search(r'for\s+\*', stripped):
                continue
            
            if re.search(r'\*\s*=', stripped):
                continue
            
            if re.search(r'^\s*\*', stripped):
                continue
            
            fixed_lines.append(line)
        
        if in_for_loop:
            fixed_lines.append('        pass')
        
        return '\n'.join(fixed_lines)

    def _validate_code_structure(self, code: str) -> bool:
        try:
            required_patterns = [
                r'from manim import \*',
                r'class GeneratedScene\(Scene\)',
                r'def construct\(self\)',
                r'self\.play\(',
                r'self\.wait\('
            ]
            
            for pattern in required_patterns:
                if not re.search(pattern, code):
                    logger.warning(f"Missing required pattern: {pattern}")
                    return False
            
            problematic_patterns = [
                r'for\s+\*',
                r'\*\s*=',
                r'^\s*\*'
            ]
            
            for pattern in problematic_patterns:
                if re.search(pattern, code, re.MULTILINE):
                    logger.warning(f"Found problematic pattern: {pattern}")
                    return False
            
            try:
                ast.parse(code)
                return True
            except SyntaxError as e:
                logger.warning(f"Syntax error in generated code: {e}")
                return False
            
        except Exception as e:
            logger.error(f"Error validating code structure: {e}")
            return False

    def _generate_emergency_fallback(self, enhanced_prompt: str) -> str:
        
        prompt_lower = enhanced_prompt.lower()
        
        if any(word in prompt_lower for word in ['circle', 'round', 'ball', 'sphere']):
            shape = "Circle(color=BLUE, radius=1.5)"
            shape_name = "circle"
        elif any(word in prompt_lower for word in ['square', 'box', 'cube']):
            shape = "Square(color=RED, side_length=2)"
            shape_name = "square"
        elif any(word in prompt_lower for word in ['triangle']):
            shape = "Triangle(color=GREEN)"
            shape_name = "triangle"
        elif any(word in prompt_lower for word in ['text', 'word', 'letter']):
            shape = 'Text("Animation", color=WHITE)'
            shape_name = "text"
        else:
            shape = "Circle(color=BLUE, radius=1.5)"
            shape_name = "circle"
        
        safe_prompt = re.sub(r'[^\w\s]', '', enhanced_prompt)[:50]
        
        return f"""from manim import *

class GeneratedScene(Scene):
    def construct(self):
        # Animation for: {safe_prompt}
        title = Text("Animation", color=WHITE, font_size=36)
        title.to_edge(UP)
        
        main_object = {shape}
        main_object.move_to(ORIGIN)
        
        # Create animations
        self.play(Write(title))
        self.wait(0.5)
        
        self.play(Create(main_object))
        self.wait(1)
        
        # Simple movement
        self.play(main_object.animate.shift(RIGHT * 2))
        self.wait(0.5)
        
        self.play(main_object.animate.shift(LEFT * 4))
        self.wait(0.5)
        
        self.play(main_object.animate.shift(RIGHT * 2))
        self.wait(1)
        
        # Fade out
        self.play(FadeOut(main_object), FadeOut(title))
        self.wait(0.5)
"""
    
    def process_and_validate_code(self, raw_code: str) -> str:
        try:
            cleaned_code = CodeValidator.fix_common_issues(raw_code)
            
            if len(cleaned_code.strip()) < 100:
                raise ValueError("Generated code is too short. Please provide a complete scene with proper class and method definitions.")
            
            is_valid, error_msg = CodeValidator.validate_python_syntax(cleaned_code)
            if not is_valid:
                logger.error(f"Syntax validation failed: {error_msg}")
                cleaned_code = self._fix_syntax_issues(cleaned_code)
                is_valid, error_msg = CodeValidator.validate_python_syntax(cleaned_code)
                if not is_valid:
                    raise ValueError(f"Generated code has syntax errors: {error_msg}")
            
            if not CodeValidator.has_scene_class(cleaned_code):
                raise ValueError("Generated code doesn't contain a proper Scene class")
            
            if not CodeValidator.has_construct_method(cleaned_code):
                raise ValueError("Generated code doesn't contain a construct method")
            
            return cleaned_code
            
        except Exception as e:
            logger.error(f"Code validation failed: {e}")
            return self._generate_emergency_fallback("simple animation")
    
    def create_temp_directory(self) -> str:
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        
        self.temp_dir = tempfile.mkdtemp(prefix="manim_")
        return self.temp_dir
    
    def save_code_to_file(self, code: str, temp_dir: str) -> str:
        code_file = os.path.join(temp_dir, "scene.py")
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write(code)
        return code_file
    
    def render_video(self, code_file: str, temp_dir: str, quality: str = "medium_quality") -> Tuple[bool, str, str]:
        start_time = time.time()
        
        try:
            quality_settings = PerformanceOptimizer.QUALITY_SETTINGS
            quality_flag = quality_settings.get(quality, quality_settings["medium_quality"])["flag"]
            
            cmd = [
                "manim", quality_flag, code_file, "GeneratedScene",
                "--output_file", "output_video",
                "--media_dir", temp_dir
            ]
            
            logger.info(f"Running command: {' '.join(cmd)}")
            
            timeout = ConfigManager.get_config("max_render_time", 300)
            process = subprocess.run(
                cmd,
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            render_time = time.time() - start_time
            
            if process.returncode == 0:
                video_files = list(Path(temp_dir).rglob("*.mp4"))
                if video_files:
                    self.metrics.record_successful_render(render_time, "unknown", quality)
                    return True, str(video_files[0]), process.stdout
                else:
                    self.metrics.record_failed_render("NoVideoFile")
                    return False, "No video file generated", process.stderr
            else:
                self.metrics.record_failed_render("RenderingFailed")
                return False, process.stderr, process.stdout
                
        except subprocess.TimeoutExpired:
            self.metrics.record_failed_render("TimeoutError")
            return False, "Rendering timeout exceeded", ""
        except Exception as e:
            logger.error(f"Error rendering video: {e}")
            self.metrics.record_failed_render("RenderingError")
            return False, f"Rendering error: {str(e)}", ""
    
    def cleanup(self):
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                logger.info(f"Cleaned up temporary directory: {self.temp_dir}")
            except Exception as e:
                logger.error(f"Error cleaning up: {e}")

def process_video_generation(generator, user_prompt, selected_model, video_quality):
    try:
        generator.metrics.record_generation_attempt()
        
        progress_bar = st.progress(0)
        status_container = st.container()
        
        with status_container:
            st.markdown('<div class="info-box">🔄 Step 1/4: Enhancing your prompt...</div>', 
                       unsafe_allow_html=True)
            progress_bar.progress(25)
            
            enhanced_prompt = generator.enhance_prompt(user_prompt, selected_model)
            
            with st.expander("📝 Enhanced Prompt", expanded=False):
                st.write(enhanced_prompt)
            
            st.markdown('<div class="info-box">🔄 Step 2/4: Generating Manim code...</div>', 
                       unsafe_allow_html=True)
            progress_bar.progress(50)
            
            raw_code = generator.generate_manim_code(enhanced_prompt, selected_model)
            clean_code = generator.process_and_validate_code(raw_code)
            
            with st.expander("💻 Generated Code", expanded=False):
                st.code(clean_code, language="python")
            
            st.markdown('<div class="info-box">🔄 Step 3/4: Setting up rendering environment...</div>', 
                       unsafe_allow_html=True)
            progress_bar.progress(75)
            
            temp_dir = generator.create_temp_directory()
            code_file = generator.save_code_to_file(clean_code, temp_dir)
            
            estimated_time = PerformanceOptimizer.estimate_render_time(video_quality)
            st.markdown(f'<div class="info-box">🔄 Step 4/4: Rendering video (estimated: {estimated_time//60}min {estimated_time%60}s)...</div>', 
                       unsafe_allow_html=True)
            
            success, result, logs = generator.render_video(code_file, temp_dir, video_quality)
            
            progress_bar.progress(100)
            
            if success:
                st.markdown('<div class="success-box">✅ Video generated successfully!</div>', 
                           unsafe_allow_html=True)
                
                if os.path.exists(result):
                    st.video(result)
                    
                    with open(result, 'rb') as video_file:
                        st.download_button(
                            label="📥 Download Video",
                            data=video_file.read(),
                            file_name="manim_animation.mp4",
                            mime="video/mp4"
                        )
                else:
                    st.error("Video file not found after rendering")
                    
                if logs and st.checkbox("Show rendering details"):
                    st.text_area("Rendering Logs", logs, height=200)
                    
            else:
                error_info = ErrorHandler.get_user_friendly_error("RenderingError", result)
                st.markdown(f'<div class="error-box">❌ {error_info["user_message"]}</div>', 
                           unsafe_allow_html=True)
                
                # Always show error details
                st.markdown("**Error Details:**")
                st.text_area("Error Message", result, height=100)
                
                if logs:
                    st.markdown("**Rendering Logs:**")
                    st.text_area("Logs", logs, height=200)
                
                suggestions = ErrorHandler.suggest_fixes(result)
                if suggestions:
                    st.markdown("**Possible solutions:**")
                    for suggestion in suggestions:
                        st.markdown(f"• {suggestion}")
            
            # Cleanup after everything is done
            if temp_dir and os.path.exists(temp_dir):
                try:
                    shutil.rmtree(temp_dir)
                    logger.info(f"Cleaned up temporary directory: {temp_dir}")
                except Exception as e:
                    logger.error(f"Error cleaning up temporary directory: {e}")
            
    except Exception as e:
        error_info = ErrorHandler.get_user_friendly_error(type(e).__name__, str(e))
        st.markdown(f'<div class="error-box">❌ {error_info["user_message"]}</div>', 
                   unsafe_allow_html=True)
        
        # Always show error details
        st.markdown("**Error Details:**")
        st.text_area("Error Message", str(e), height=100)
        
        suggestions = ErrorHandler.suggest_fixes(str(e))
        if suggestions:
            st.markdown("**Try these solutions:**")
            for suggestion in suggestions:
                st.markdown(f"• {suggestion}")
        
        logger.error(f"Application error: {e}")
        
        # Cleanup in case of error
        if 'temp_dir' in locals() and temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                logger.info(f"Cleaned up temporary directory after error: {temp_dir}")
            except Exception as cleanup_error:
                logger.error(f"Error cleaning up temporary directory after error: {cleanup_error}")

def main():
    initialize_app()
    render_header()
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        st.error("""
        GROQ_API_KEY not found in environment. Please ensure:
        
        1. You have a .env file in the project root with:
           GROQ_API_KEY=your_key_here
        
        2. Or set it in your environment:
           - Windows: set GROQ_API_KEY=your_key_here
           - Linux/Mac: export GROQ_API_KEY=your_key_here
        
        3. For Docker:
           - Pass it as an environment variable: docker run -e GROQ_API_KEY=your_key_here ...
           - Or use docker-compose with the environment variable set
        """)
        st.stop()
    
    # Render sidebar and get configuration
    config = render_sidebar()
    if config[0] is None:  # No API key in environment
        st.error("Failed to get API key from environment. Please check your .env file.")
        st.stop()
    
    _, selected_model, video_quality = config  # We already have the API key from environment
    
    # Initialize generator
    generator = ManimVideoGenerator(groq_api_key)
    
    # Render main interface
    user_prompt, generate_button = render_main_interface()
    
    # Process generation only if button is clicked and there's a prompt
    if generate_button and user_prompt and user_prompt.strip():
        process_video_generation(generator, user_prompt, selected_model, video_quality)
        generator.cleanup()
    
    # Render footer
    render_footer(generator)

if __name__ == "__main__":
    main()