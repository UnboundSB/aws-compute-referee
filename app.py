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


@st.cache_data
def cached_calculate_compatibility(operational_overhead, cost_sensitivity, workload_consistency, setup_speed):
    """Cached version of calculate_compatibility for better performance"""
    from models import UserWeights
    user_weights = UserWeights(
        operational_overhead=operational_overhead,
        cost_sensitivity=cost_sensitivity,
        workload_consistency=workload_consistency,
        setup_speed=setup_speed
    )
    return calculate_compatibility(user_weights)


def main():
    """Main application entry point"""
    # Configure the Streamlit page
    st.set_page_config(
        page_title="AWS Compute Referee",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Main header
    st.title("⚖️ AWS Compute Referee")
    st.markdown("*Choose the optimal AWS compute service based on your priorities*")
    st.markdown("---")
    
    # Create sidebar configurator
    user_weights = create_sidebar_configurator()
    
    # Calculate compatibility scores (with caching)
    try:
        winner, winner_score, all_scores = cached_calculate_compatibility(
            user_weights['operational_overhead'],
            user_weights['cost_sensitivity'],
            user_weights['workload_consistency'],
            user_weights['setup_speed']
        )
        explanation = get_service_explanation(winner, user_weights)
        
        # Display results in main area
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Display winner and explanation
            display_winner(winner, winner_score, explanation)
            
            # Display radar chart
            st.subheader("📈 Visual Comparison")
            radar_chart = create_radar_chart(user_weights, winner)
            st.plotly_chart(radar_chart, use_container_width=True)
        
        with col2:
            # Display all scores
            display_all_scores(all_scores)
            
            # Add some helpful information
            st.markdown("---")
            st.markdown("### 💡 How it works")
            st.markdown("""
            1. **Set your priorities** using the sliders
            2. **Algorithm calculates** compatibility scores
            3. **Best match** is recommended
            4. **Visual comparison** shows the fit
            """)
            
    except Exception as e:
        st.error(f"Error calculating recommendations: {str(e)}")
        st.info("Please check your input values and try again.")


if __name__ == "__main__":
    main()