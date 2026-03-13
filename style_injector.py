"""
Style Injector for AWS Compute Referee

This module handles CSS injection for beautiful glassmorphic styling.
"""

import streamlit as st


def inject_custom_css():
    """
    Inject custom CSS styles for glassmorphic design.
    Reads from styles.css and injects into Streamlit app.
    """
    try:
        with open('styles.css', 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        st.markdown(f"""
        <style>
        {css_content}
        </style>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.warning("⚠️ Custom styles file not found. Using default styling.")
    except Exception as e:
        st.error(f"❌ Error loading custom styles: {str(e)}")


def add_glassmorphic_header():
    """
    Add a beautiful glassmorphic header with animations.
    """
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 25px;
            padding: 2rem;
            margin: 1rem 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            animation: fadeInUp 0.8s ease-out;
        ">
            <h1 style="
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                font-size: 3.5rem;
                font-weight: 700;
                margin: 0;
                animation: titleGlow 2s ease-in-out infinite alternate;
            ">⚖️ AWS Compute Referee</h1>
            <p style="
                color: rgba(255, 255, 255, 0.9);
                font-size: 1.3rem;
                margin: 1rem 0 0 0;
                font-weight: 300;
            ">Choose the optimal AWS compute service with AI-powered recommendations</p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def add_floating_particles():
    """
    Add floating particle animation background.
    """
    st.markdown("""
    <div class="particles">
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
        <div class="particle"></div>
    </div>
    
    <style>
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .particle {
        position: absolute;
        width: 4px;
        height: 4px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    .particle:nth-child(1) {
        left: 20%;
        animation-delay: 0s;
        animation-duration: 6s;
    }
    
    .particle:nth-child(2) {
        left: 40%;
        animation-delay: 2s;
        animation-duration: 8s;
    }
    
    .particle:nth-child(3) {
        left: 60%;
        animation-delay: 4s;
        animation-duration: 7s;
    }
    
    .particle:nth-child(4) {
        left: 80%;
        animation-delay: 1s;
        animation-duration: 9s;
    }
    
    .particle:nth-child(5) {
        left: 10%;
        animation-delay: 3s;
        animation-duration: 5s;
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(100vh) rotate(0deg);
            opacity: 0;
        }
        10%, 90% {
            opacity: 1;
        }
        50% {
            transform: translateY(-10vh) rotate(180deg);
        }
    }
    </style>
    """, unsafe_allow_html=True)


def add_winner_glow_effect():
    """
    Add special glow effect for winner display.
    """
    st.markdown("""
    <style>
    .winner-container {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(17, 153, 142, 0.4);
        animation: winnerPulse 2s ease-in-out infinite alternate;
        position: relative;
        overflow: hidden;
    }
    
    .winner-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shimmer 3s linear infinite;
    }
    
    @keyframes winnerPulse {
        from { 
            box-shadow: 0 15px 35px rgba(17, 153, 142, 0.4);
            transform: scale(1);
        }
        to { 
            box-shadow: 0 20px 40px rgba(56, 239, 125, 0.6);
            transform: scale(1.02);
        }
    }
    </style>
    """, unsafe_allow_html=True)