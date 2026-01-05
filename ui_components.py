"""
UI Components for AWS Compute Referee

This module contains reusable Streamlit UI components that are clean,
modular, and focused on specific functionality.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict
from models import UserWeights, get_aws_services, SERVICE_DESCRIPTIONS


def create_sidebar_configurator() -> UserWeights:
    """
    Create the sidebar configuration panel with priority sliders.
    
    Returns:
        UserWeights dictionary with user's priority values (0-100)
    """
    st.sidebar.header("🎯 Your Priorities")
    st.sidebar.markdown("*Adjust the sliders to reflect your priorities*")
    
    # Create sliders with descriptive labels and help text
    operational_overhead = st.sidebar.slider(
        "**Operational Overhead**",
        min_value=0,
        max_value=100,
        value=50,
        help="Higher = Prefer managed services with less operational work"
    )
    st.sidebar.caption("*Managed vs. Custom*")
    
    cost_sensitivity = st.sidebar.slider(
        "**Cost Sensitivity**",
        min_value=0,
        max_value=100,
        value=70,
        help="Higher = Prioritize cost-effective solutions"
    )
    st.sidebar.caption("*Budget vs. Performance*")
    
    workload_consistency = st.sidebar.slider(
        "**Workload Consistency**",
        min_value=0,
        max_value=100,
        value=60,
        help="Higher = Prefer services optimized for steady, predictable workloads"
    )
    st.sidebar.caption("*Spiky vs. Steady*")
    
    setup_speed = st.sidebar.slider(
        "**Setup Speed**",
        min_value=0,
        max_value=100,
        value=75,
        help="Higher = Need fast deployment and quick time-to-market"
    )
    st.sidebar.caption("*Instant vs. Planned*")
    
    return UserWeights(
        operational_overhead=operational_overhead,
        cost_sensitivity=cost_sensitivity,
        workload_consistency=workload_consistency,
        setup_speed=setup_speed
    )


def display_winner(winner: str, winner_score: float, explanation: str) -> None:
    """
    Display the winning service with attractive styling.
    
    Args:
        winner: Name of the winning service
        winner_score: Compatibility score (0-100)
        explanation: Human-readable explanation of the recommendation
    """
    # Main winner announcement
    st.success(f"🏆 **Recommended Service: {winner}**")
    
    # Create columns for metrics and description
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric(
            label="Compatibility Score",
            value=f"{winner_score:.1f}%",
            help="How well this service matches your priorities"
        )
    
    with col2:
        st.info(SERVICE_DESCRIPTIONS[winner])
    
    # Explanation
    st.markdown(f"**Why {winner}?** {explanation}")


def create_radar_chart(user_weights: UserWeights, winner_service: str) -> go.Figure:
    """
    Create a beautiful radar chart comparing user ideal vs winner characteristics.
    
    Args:
        user_weights: User's priority weights
        winner_service: Name of the winning service
        
    Returns:
        Plotly Figure object ready for display
    """
    winner_chars = get_aws_services()[winner_service]
    
    # Define the dimensions and their display names
    dimensions = [
        ("operational_overhead", "Operational<br>Overhead"),
        ("cost_sensitivity", "Cost<br>Sensitivity"),
        ("workload_consistency", "Workload<br>Consistency"),
        ("setup_speed", "Setup<br>Speed")
    ]
    
    # Extract values for both traces
    user_values = [user_weights[dim[0]] for dim in dimensions]
    winner_values = [winner_chars[dim[0]] for dim in dimensions]
    dimension_labels = [dim[1] for dim in dimensions]
    
    # Create the radar chart
    fig = go.Figure()
    
    # Add user's ideal trace
    fig.add_trace(go.Scatterpolar(
        r=user_values,
        theta=dimension_labels,
        fill='toself',
        name="Your Ideal",
        line_color='rgba(0, 123, 255, 0.8)',
        fillcolor='rgba(0, 123, 255, 0.1)',
        hovertemplate="<b>Your Ideal</b><br>%{theta}: %{r}<extra></extra>"
    ))
    
    # Add winner's stats trace
    fig.add_trace(go.Scatterpolar(
        r=winner_values,
        theta=dimension_labels,
        fill='toself',
        name=f"{winner_service} Stats",
        line_color='rgba(40, 167, 69, 0.8)',
        fillcolor='rgba(40, 167, 69, 0.1)',
        hovertemplate=f"<b>{winner_service}</b><br>%{{theta}}: %{{r}}<extra></extra>"
    ))
    
    # Update layout for better appearance
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=25,
                gridcolor='rgba(128, 128, 128, 0.3)'
            ),
            angularaxis=dict(
                gridcolor='rgba(128, 128, 128, 0.3)'
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5
        ),
        title=dict(
            text=f"<b>Compatibility Analysis: You vs {winner_service}</b>",
            x=0.5,
            font=dict(size=16)
        ),
        height=500,
        margin=dict(t=80, b=80, l=80, r=80)
    )
    
    return fig


def display_all_scores(all_scores: Dict[str, float]) -> None:
    """
    Display compatibility scores for all services in an attractive format.
    
    Args:
        all_scores: Dictionary with service names and their compatibility scores
    """
    st.subheader("📊 All Service Scores")
    
    # Sort services by score (descending)
    sorted_services = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Create columns for the scores
    cols = st.columns(len(sorted_services))
    
    for i, (service, score) in enumerate(sorted_services):
        with cols[i]:
            # Add medal emoji for top 3
            medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "📊"
            
            st.metric(
                label=f"{medal} {service}",
                value=f"{score:.1f}%",
                help=SERVICE_DESCRIPTIONS[service]
            )