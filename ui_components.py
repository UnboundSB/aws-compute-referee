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
    # Add glassmorphic styling to sidebar
    st.sidebar.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    ">
        <h2 style="
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 600;
            margin-bottom: 0.5rem;
        ">🎯 Your Priorities</h2>
        <p style="color: rgba(255, 255, 255, 0.8); font-style: italic;">
            Adjust the sliders to reflect your priorities
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create sliders with enhanced styling
    st.sidebar.markdown('<div class="slider-container">', unsafe_allow_html=True)
    
    operational_overhead = st.sidebar.slider(
        "**🔧 Operational Overhead**",
        min_value=0,
        max_value=100,
        value=50,
        help="Higher = Prefer managed services with less operational work"
    )
    st.sidebar.markdown('<p style="color: rgba(255,255,255,0.7); font-style: italic; text-align: center; margin-top: -10px;">Managed vs. Custom</p>', unsafe_allow_html=True)
    
    cost_sensitivity = st.sidebar.slider(
        "**💰 Cost Sensitivity**",
        min_value=0,
        max_value=100,
        value=70,
        help="Higher = Prioritize cost-effective solutions"
    )
    st.sidebar.markdown('<p style="color: rgba(255,255,255,0.7); font-style: italic; text-align: center; margin-top: -10px;">Budget vs. Performance</p>', unsafe_allow_html=True)
    
    workload_consistency = st.sidebar.slider(
        "**📊 Workload Consistency**",
        min_value=0,
        max_value=100,
        value=60,
        help="Higher = Prefer services optimized for steady, predictable workloads"
    )
    st.sidebar.markdown('<p style="color: rgba(255,255,255,0.7); font-style: italic; text-align: center; margin-top: -10px;">Spiky vs. Steady</p>', unsafe_allow_html=True)
    
    setup_speed = st.sidebar.slider(
        "**⚡ Setup Speed**",
        min_value=0,
        max_value=100,
        value=75,
        help="Higher = Need fast deployment and quick time-to-market"
    )
    st.sidebar.markdown('<p style="color: rgba(255,255,255,0.7); font-style: italic; text-align: center; margin-top: -10px;">Instant vs. Planned</p>', unsafe_allow_html=True)
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    return UserWeights(
        operational_overhead=operational_overhead,
        cost_sensitivity=cost_sensitivity,
        workload_consistency=workload_consistency,
        setup_speed=setup_speed
    )


def display_winner(winner: str, winner_score: float, explanation: str) -> None:
    """
    Display the winning service with attractive glassmorphic styling.
    
    Args:
        winner: Name of the winning service
        winner_score: Compatibility score (0-100)
        explanation: Human-readable explanation of the recommendation
    """
    # Main winner announcement with glassmorphic styling
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(17, 153, 142, 0.4);
        animation: winnerPulse 2s ease-in-out infinite alternate;
        position: relative;
        overflow: hidden;
        text-align: center;
    ">
        <div style="
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
            transform: rotate(45deg);
            animation: shimmer 3s linear infinite;
        "></div>
        <h2 style="
            color: white;
            font-size: 2.5rem;
            margin: 0;
            position: relative;
            z-index: 1;
        ">🏆 Recommended Service: {winner}</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for metrics and description
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
            color: white;
            box-shadow: 0 10px 25px rgba(79, 172, 254, 0.3);
            animation: floating 3s ease-in-out infinite;
        ">
            <h3 style="margin: 0; font-size: 1.2rem;">Compatibility Score</h3>
            <div style="font-size: 3rem; font-weight: bold; margin: 0.5rem 0;">{winner_score:.1f}%</div>
            <p style="margin: 0; opacity: 0.9;">Perfect Match!</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 1.5rem;
            color: white;
            animation: slideIn 0.6s ease-out;
        ">
            <div style="font-size: 1.1rem; margin-bottom: 1rem;">
                {SERVICE_DESCRIPTIONS[winner]}
            </div>
            <div style="
                background: rgba(255, 255, 255, 0.1);
                border-radius: 10px;
                padding: 1rem;
                border-left: 4px solid #38ef7d;
            ">
                <strong>Why {winner}?</strong> {explanation}
            </div>
        </div>
        """, unsafe_allow_html=True)


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
    Display compatibility scores for all services in an attractive glassmorphic format.
    
    Args:
        all_scores: Dictionary with service names and their compatibility scores
    """
    st.markdown("""
    <div style="
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <h3 style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-bottom: 1.5rem;
        ">📊 All Service Scores</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Sort services by score (descending)
    sorted_services = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Display each service with glassmorphic styling
    for i, (service, score) in enumerate(sorted_services):
        # Add medal emoji for top 3
        medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "📊"
        
        # Different gradient for each position
        gradients = [
            "linear-gradient(135deg, #FFD700 0%, #FFA500 100%)",  # Gold
            "linear-gradient(135deg, #C0C0C0 0%, #808080 100%)",  # Silver
            "linear-gradient(135deg, #CD7F32 0%, #8B4513 100%)",  # Bronze
            "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"   # Default
        ]
        
        gradient = gradients[min(i, 3)]
        
        st.markdown(f"""
        <div style="
            background: {gradient};
            border-radius: 15px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            color: white;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
            animation: slideIn 0.6s ease-out;
            animation-delay: {i * 0.1}s;
            animation-fill-mode: both;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: -50%;
                right: -50%;
                width: 200%;
                height: 200%;
                background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
                transform: rotate(45deg);
                animation: shimmer 4s linear infinite;
                animation-delay: {i * 0.5}s;
            "></div>
            <div style="position: relative; z-index: 1;">
                <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{medal} {service}</div>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">{score:.1f}%</div>
                <div style="font-size: 0.9rem; opacity: 0.9;">{SERVICE_DESCRIPTIONS[service]}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)