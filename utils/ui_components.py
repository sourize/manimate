import streamlit as st
from utils.performance_optimizer import PerformanceOptimizer
from utils.system_checker import SystemChecker
from utils.prompt_templates import PromptTemplates
from utils.error_handler import ErrorHandler
import os


def initialize_app():
    st.set_page_config(
        page_title="Manimate",
        page_icon="🎬",
        layout="centered",
        initial_sidebar_state="expanded"
    )
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .metric-box {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        padding: 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>🎬 Manim Video Generator</h1>
        <p>Transform your ideas into mathematical animations</p>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    with st.sidebar:
        st.header("⚙️ Configuration")
        with st.expander("🔧 System Status", expanded=False):
            system_info = SystemChecker.get_system_info()
            for key, value in system_info.items():
                status = "✅" if value else "❌"
                st.write(f"{status} {key.replace('_', ' ').title()}: {value}")
        
        model_options = {
            "llama-3.3-70b-versatile": "Llama 3.3 70B (Recommended)",
            "llama3-8b-8192": "Llama 3 8B (Fast)",
            "mixtral-8x7b-32768": "Mixtral 8x7B (Creative)",
            "gemma2-9b-it": "Gemma 2 9B (Efficient)"
        }
        selected_model = st.selectbox(
            "AI Model",
            options=list(model_options.keys()),
            format_func=lambda x: model_options[x],
            help="Choose the model for code generation"
        )
        quality_options = PerformanceOptimizer.QUALITY_SETTINGS
        video_quality = st.selectbox(
            "Video Quality",
            options=list(quality_options.keys()),
            index=1,
            format_func=lambda x: quality_options[x]["description"]
        )
        estimated_time = PerformanceOptimizer.estimate_render_time(video_quality)
        st.info(f"⏱️ Estimated render time: ~{estimated_time//60}min {estimated_time%60}s")
        st.markdown("---")
        st.markdown("### 📋 Quick Guide")
        st.markdown("""
        1. **Enter your prompt** - Be specific about animations
        2. **Choose quality** - Higher = better but slower  
        3. **Generate video** - Wait for processing
        4. **Download result** - Save your animation
        **Tips:**
        - Mention colors, shapes, math concepts
        - Keep descriptions clear and focused
        - Try examples for inspiration
        """)
        return True, selected_model, video_quality

# def render_examples():
#     st.header("💡 Example Prompts")
#     examples = {
#         "🧮 Algebra": [
#             "Visualize solving x² + 3x - 4 = 0 using the quadratic formula",
#             "Show function transformations with f(x) = x² shifting and scaling"
#         ],
#         "📐 Geometry": [
#             "Demonstrate the Pythagorean theorem with squares on triangle sides",
#             "Animate the construction of a regular pentagon using compass and straightedge"
#         ],
#         "📊 Calculus": [
#             "Show the concept of limits with a function approaching a value",
#             "Visualize area under curve using Riemann sums with rectangles"
#         ],
#         "📈 Statistics": [
#             "Animate the Central Limit Theorem with multiple distributions",
#             "Show correlation vs causation with scatter plot examples"
#         ]
#     }
#     cols = st.columns(2)
#     for i, (category, prompts) in enumerate(examples.items()):
#         with cols[i % 2]:
#             st.subheader(category)
#             for j, prompt in enumerate(prompts):
#                 if st.button(f"{prompt[:50]}..." if len(prompt) > 50 else prompt, key=f"example_{i}_{j}"):
#                     return prompt
#     return None

def render_main_interface():
    st.header("✨ Your Animation Prompt")
    user_prompt = st.text_area(
        "Describe the mathematical animation you want to create:",
        height=150,
        placeholder="Example: Create an animation showing the derivative of x² as the slope of tangent lines, with smooth transitions and clear labeling",
        help="Be as descriptive as possible for best results. Mention specific mathematical concepts, colors, and visual elements."
    )
    if user_prompt:
        category = PromptTemplates.detect_category(user_prompt)
        complexity = "complex" if len(user_prompt) > 100 else "medium"
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.info(f"📂 Detected category: **{category.title()}**")
        with col_info2:
            st.info(f"🎯 Complexity: **{complexity.title()}**")
    generate_button = st.button("🚀 Generate Animation", type="primary", disabled=not user_prompt.strip())
    
    # example_prompt = render_examples()
    return user_prompt, generate_button, None

def render_footer(generator=None):
    st.markdown("---")
    if generator and hasattr(generator, 'metrics'):
        metrics_summary = generator.metrics.get_summary()
        if metrics_summary["success_rate"] > 0:
            st.markdown("### 📊 Session Statistics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="metric-box">Success Rate<br><strong>{metrics_summary["success_rate"]:.1f}%</strong></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-box">Avg Render Time<br><strong>{metrics_summary["average_render_time"]:.1f}s</strong></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-box">Popular Quality<br><strong>{metrics_summary["most_popular_quality"]}</strong></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>🎬 Built with ❤️ using Streamlit, Manim, and Groq AI</p>
        <p>For issues or suggestions, please check the repository.</p>
    </div>
    """, unsafe_allow_html=True) 