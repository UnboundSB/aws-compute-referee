"""
Core Business Logic Engine for AWS Compute Referee

This module contains the pure Python business logic for calculating
service compatibility scores. It has no dependencies on Streamlit
or any UI framework, making it easily testable and reusable.
"""

import math
from typing import Dict, Tuple
from models import UserWeights, get_aws_services, validate_aws_services_integrity, PRIORITY_DIMENSIONS
from models import UserWeights, AWS_SERVICES, PRIORITY_DIMENSIONS


def calculate_compatibility(user_weights: UserWeights) -> Tuple[str, float, Dict[str, float]]:
    """
    Calculate compatibility scores for all AWS services using weighted Euclidean distance.
    
    This function implements a sophisticated scoring algorithm that:
    1. Calculates the Euclidean distance between user preferences and service characteristics
    2. Applies equal weighting to all dimensions (can be enhanced later)
    3. Converts distances to compatibility scores (0-100 scale)
    4. Returns the service with the highest compatibility score
    
    Args:
        user_weights: Dictionary containing user priority weights (0-100 for each dimension)
        
    Returns:
        Tuple containing:
        - winner_service_name: Name of the service with highest compatibility
        - winner_score: Compatibility score of the winner (0-100)
        - all_scores: Dictionary with compatibility scores for all services
        
    Raises:
        ValueError: If user_weights contains invalid values or missing dimensions
        
    Example:
        >>> weights = {
        ...     'operational_overhead': 80,
        ...     'cost_sensitivity': 60,
        ...     'workload_consistency': 40,
        ...     'setup_speed': 90
        ... }
        >>> winner, score, all_scores = calculate_compatibility(weights)
        >>> print(f"Recommended: {winner} (Score: {score:.1f})")
    """
    
    # Input validation
    _validate_user_weights(user_weights)
    
    # Validate AWS_SERVICES integrity
    if not validate_aws_services_integrity():
        raise RuntimeError("AWS_SERVICES data integrity compromised")
    
    # Get AWS services data (defensive copy)
    aws_services = get_aws_services()
    
    # Calculate compatibility scores for each service
    all_scores = {}
    
    for service_name, service_chars in aws_services.items():
        score = _calculate_service_score(user_weights, service_chars)
        all_scores[service_name] = score
    
    # Find the winner (service with highest score)
    winner_service = max(all_scores.keys(), key=lambda k: all_scores[k])
    winner_score = all_scores[winner_service]
    
    return winner_service, winner_score, all_scores


def _validate_user_weights(user_weights: UserWeights) -> None:
    """
    Validate user weights input for correctness.
    
    Args:
        user_weights: User priority weights to validate
        
    Raises:
        ValueError: If weights are invalid
    """
    # Check that all required dimensions are present
    missing_dims = set(PRIORITY_DIMENSIONS) - set(user_weights.keys())
    if missing_dims:
        raise ValueError(f"Missing priority dimensions: {missing_dims}")
    
    # Check that all values are in valid range (0-100)
    for dim, value in user_weights.items():
        if not isinstance(value, (int, float)):
            raise ValueError(f"Priority '{dim}' must be a number, got {type(value)}")
        if not (0 <= value <= 100):
            raise ValueError(f"Priority '{dim}' must be between 0-100, got {value}")


def _calculate_service_score(user_weights: UserWeights, service_chars: Dict[str, int]) -> float:
    """
    Calculate compatibility score for a single service using weighted Euclidean distance.
    
    The algorithm:
    1. Calculate squared differences for each dimension
    2. Apply equal weighting (weight_factor = 1.0 for all dimensions)
    3. Calculate Euclidean distance: sqrt(sum(differences))
    4. Convert to compatibility score: 100 - (distance / max_possible_distance * 100)
    
    Args:
        user_weights: User priority weights
        service_chars: Service characteristics
        
    Returns:
        Compatibility score (0-100, higher is better)
    """
    
    # Calculate weighted squared differences
    squared_diffs = []
    weight_factor = 1.0  # Equal weighting for all dimensions
    
    for dimension in PRIORITY_DIMENSIONS:
        user_value = user_weights[dimension]
        service_value = service_chars[dimension]
        
        # Calculate squared difference with weighting
        diff = (user_value - service_value) ** 2 * weight_factor
        squared_diffs.append(diff)
    
    # Calculate Euclidean distance
    distance = math.sqrt(sum(squared_diffs))
    
    # Convert distance to compatibility score (0-100 scale)
    # Maximum possible distance is when all dimensions are at opposite extremes
    max_possible_distance = math.sqrt(len(PRIORITY_DIMENSIONS) * (100 ** 2) * weight_factor)
    
    # Convert to compatibility score (higher is better)
    compatibility_score = 100 - (distance / max_possible_distance * 100)
    
    # Ensure score is within bounds
    return max(0.0, min(100.0, compatibility_score))


def get_service_explanation(winner: str, user_weights: UserWeights) -> str:
    """
    Generate a human-readable explanation of why a service was recommended.
    
    Args:
        winner: Name of the winning service
        user_weights: User's priority weights
        
    Returns:
        Explanation string describing the recommendation rationale
    """
    aws_services = get_aws_services()
    service_chars = aws_services[winner]
    
    # Find the user's top priorities (values > 70)
    top_priorities = [
        dim for dim, value in user_weights.items() 
        if value > 70
    ]
    
    # Find service strengths (values > 70)
    service_strengths = [
        dim for dim, value in service_chars.items()
        if value > 70
    ]
    
    # Find alignment between user priorities and service strengths
    aligned_strengths = set(top_priorities) & set(service_strengths)
    
    if aligned_strengths:
        strength_names = [dim.replace('_', ' ').title() for dim in aligned_strengths]
        return f"Great match! {winner} excels in {', '.join(strength_names)}, which aligns with your priorities."
    else:
        return f"{winner} provides the best overall balance for your requirements."