"""
Demo script to showcase the AWS Compute Referee with glassmorphic styling
"""

import streamlit as st
from style_injector import inject_custom_css, add_glassmorphic_header, add_floating_particles

def demo():
    st.set_page_config(
        page_title="AWS Compute Referee Demo",
        page_icon="⚖️",
        layout="wide"
    )
    
    # Inject the beautiful styling
    inject_custom_css()
    add_floating_particles()
    add_glassmorphic_header()
    
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        text-align: center;
        animation: fadeInUp 0.8s ease-out;
    ">
        <h2 style="
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
        ">🎨 Glassmorphic Design Demo</h2>
        <p style="color: rgba(255, 255, 255, 0.9); font-size: 1.2rem;">
            Beautiful, modern UI with glassmorphism effects, animations, and responsive design!
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    demo()