"""
AWS Compute Referee - Streamlit Decision Support System

A sophisticated Decision Support System that helps developers choose the optimal 
AWS Compute service (EC2, Lambda, Fargate, App Runner) based on their priorities.

This is the main application file that orchestrates all components.
"""

import streamlit as st
from engine import calculate_compatibility, get_service_explanation
from ui_components import (
    create_sidebar_configurator, 
    display_winner, 
    create_radar_chart,
    display_all_scores
)
from style_injector import inject_custom_css, add_glassmorphic_header, add_floating_particles


def main():
    """Main application entry point"""
    # Configure the Streamlit page
    st.set_page_config(
        page_title="AWS Compute Referee",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Inject custom CSS for glassmorphic design
    inject_custom_css()
    
    # Add floating particles background
    add_floating_particles()
    
    # Add beautiful glassmorphic header
    add_glassmorphic_header()
    
    # Create sidebar configurator
    user_weights = create_sidebar_configurator()
    
    # Calculate compatibility scores
    try:
        winner, winner_score, all_scores = calculate_compatibility(user_weights)
        explanation = get_service_explanation(winner, user_weights)
        
        # Display results in main area with glassmorphic styling
        col1, col2 = st.columns([2, 1], gap="large")
        
        with col1:
            # Display winner and explanation with special styling
            st.markdown('<div class="winner-glow floating">', unsafe_allow_html=True)
            display_winner(winner, winner_score, explanation)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Display radar chart with glassmorphic container
            st.markdown("### 📈 Visual Comparison")
            st.markdown('<div class="chart-container floating">', unsafe_allow_html=True)
            radar_chart = create_radar_chart(user_weights, winner)
            st.plotly_chart(radar_chart, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            # Display all scores with animation
            st.markdown('<div class="scores-container pulse">', unsafe_allow_html=True)
            display_all_scores(all_scores)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Add helpful information with glassmorphic styling
            st.markdown("---")
            st.markdown("""
            <div style="
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(15px);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 1.5rem;
                margin: 1rem 0;
                animation: slideIn 0.6s ease-out;
            ">
                <h3 style="
                    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin-bottom: 1rem;
                ">💡 How it works</h3>
                <div style="color: rgba(255, 255, 255, 0.9); line-height: 1.6;">
                    <p>🎯 <strong>Set your priorities</strong> using the sliders</p>
                    <p>🧠 <strong>AI calculates</strong> compatibility scores</p>
                    <p>🏆 <strong>Best match</strong> is recommended</p>
                    <p>📊 <strong>Visual comparison</strong> shows the fit</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error calculating recommendations: {str(e)}")
        st.info("Please check your input values and try again.")


if __name__ == "__main__":
    main()