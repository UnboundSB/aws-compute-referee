"""
Data Models and Type Definitions for AWS Compute Referee

This module contains all the data structures, type definitions, and constants
used throughout the application.
"""

from typing import Dict, Tuple, TypedDict


# =============================================================================
# TYPE DEFINITIONS
# =============================================================================

class UserWeights(TypedDict):
    """Type definition for user priority weights (0-100 scale)"""
    operational_overhead: int  # Higher = prefer managed services
    cost_sensitivity: int      # Higher = prefer cost-effective options
    workload_consistency: int  # Higher = prefer steady workload optimization
    setup_speed: int          # Higher = prefer fast deployment


class ServiceCharacteristics(TypedDict):
    """Type definition for AWS service characteristics (0-100 scale)"""
    operational_overhead: int  # Service's management level
    cost_sensitivity: int      # Service's cost efficiency
    workload_consistency: int  # Service's steady workload optimization
    setup_speed: int          # Service's deployment speed


class CompatibilityResult(TypedDict):
    """Type definition for compatibility calculation results"""
    winner: str                    # Name of recommended service
    winner_score: float            # Compatibility score (0-100)
    all_scores: Dict[str, float]   # Scores for all services


# =============================================================================
# AWS SERVICES DATA
# =============================================================================

AWS_SERVICES: Dict[str, ServiceCharacteristics] = {
    "EC2": {
        "operational_overhead": 20,  # High operational overhead (custom management)
        "cost_sensitivity": 60,     # Moderate cost efficiency
        "workload_consistency": 80,  # Excellent for steady workloads
        "setup_speed": 30           # Slower setup time
    },
    "Lambda": {
        "operational_overhead": 90,  # Very low operational overhead (fully managed)
        "cost_sensitivity": 85,     # Excellent cost efficiency for sporadic use
        "workload_consistency": 30,  # Better for spiky/event-driven workloads
        "setup_speed": 95           # Very fast setup
    },
    "Fargate": {
        "operational_overhead": 75,  # Low operational overhead (managed containers)
        "cost_sensitivity": 70,     # Good cost efficiency
        "workload_consistency": 70,  # Good for both steady and variable workloads
        "setup_speed": 60           # Moderate setup time
    },
    "App Runner": {
        "operational_overhead": 85,  # Very low operational overhead
        "cost_sensitivity": 75,     # Good cost efficiency
        "workload_consistency": 60,  # Moderate workload flexibility
        "setup_speed": 90           # Very fast setup
    }
}


# =============================================================================
# CONSTANTS
# =============================================================================

PRIORITY_DIMENSIONS = [
    "operational_overhead",
    "cost_sensitivity", 
    "workload_consistency",
    "setup_speed"
]

SERVICE_DESCRIPTIONS = {
    "EC2": "🖥️ Virtual servers with full control and customization",
    "Lambda": "⚡ Serverless functions for event-driven workloads",
    "Fargate": "📦 Managed containers without server management",
    "App Runner": "🚀 Fully managed web applications and APIs"
}


# =============================================================================
# IMMUTABILITY SAFEGUARDS
# =============================================================================

def get_aws_services() -> Dict[str, ServiceCharacteristics]:
    """
    Get a defensive copy of AWS_SERVICES to prevent accidental modification.
    
    Returns:
        Deep copy of AWS_SERVICES dictionary
    """
    import copy
    return copy.deepcopy(AWS_SERVICES)


def validate_aws_services_integrity() -> bool:
    """
    Validate that AWS_SERVICES maintains its expected structure and values.
    
    Returns:
        True if AWS_SERVICES is intact, False otherwise
    """
    expected_services = {"EC2", "Lambda", "Fargate", "App Runner"}
    expected_dimensions = set(PRIORITY_DIMENSIONS)
    
    # Check service names
    if set(AWS_SERVICES.keys()) != expected_services:
        return False
    
    # Check each service structure and value ranges
    for service_name, service_data in AWS_SERVICES.items():
        # Check dimensions
        if set(service_data.keys()) != expected_dimensions:
            return False
        
        # Check value ranges
        for dimension, value in service_data.items():
            if not isinstance(value, (int, float)) or not (0 <= value <= 100):
                return False
    
    return True