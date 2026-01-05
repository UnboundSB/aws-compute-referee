"""
Property-based tests for AWS Compute Referee

Tests the core data structures and business logic using property-based testing
to ensure correctness across all possible inputs.
"""

import pytest
from hypothesis import given, strategies as st
from models import AWS_SERVICES, UserWeights, ServiceCharacteristics
from engine import calculate_compatibility


class TestAWSServicesDataStructure:
    """Test suite for AWS_SERVICES data structure consistency"""
    
    def test_aws_services_structure_basic(self):
        """
        Feature: aws-compute-referee, Property 2: Service data structure consistency
        Basic validation of AWS_SERVICES structure
        """
        # Test that AWS_SERVICES contains exactly 4 services
        assert len(AWS_SERVICES) == 4, f"Expected 4 services, got {len(AWS_SERVICES)}"
        
        # Test that it contains the expected services
        expected_services = {"EC2", "Lambda", "Fargate", "App Runner"}
        actual_services = set(AWS_SERVICES.keys())
        assert actual_services == expected_services, f"Expected {expected_services}, got {actual_services}"
    
    @given(st.sampled_from(list(AWS_SERVICES.keys())))
    def test_service_has_all_required_attributes(self, service_name: str):
        """
        Feature: aws-compute-referee, Property 2: Service data structure consistency
        Property test: For any service in AWS_SERVICES, it should contain all four required priority dimensions
        """
        service_data = AWS_SERVICES[service_name]
        required_attributes = {
            'operational_overhead',
            'cost_sensitivity', 
            'workload_consistency',
            'setup_speed'
        }
        
        actual_attributes = set(service_data.keys())
        assert actual_attributes == required_attributes, (
            f"Service {service_name} missing attributes: "
            f"{required_attributes - actual_attributes} or has extra: "
            f"{actual_attributes - required_attributes}"
        )
    
    @given(st.sampled_from(list(AWS_SERVICES.keys())))
    def test_service_attributes_are_numerical(self, service_name: str):
        """
        Feature: aws-compute-referee, Property 2: Service data structure consistency
        Property test: For any service, all attribute values should be numerical (int or float)
        """
        service_data = AWS_SERVICES[service_name]
        
        for attr_name, attr_value in service_data.items():
            assert isinstance(attr_value, (int, float)), (
                f"Service {service_name} attribute {attr_name} has non-numerical value: "
                f"{attr_value} (type: {type(attr_value)})"
            )
    
    def test_aws_services_immutability_structure(self):
        """
        Test that AWS_SERVICES maintains its structure (this supports immutability testing)
        """
        # Store original structure
        original_keys = set(AWS_SERVICES.keys())
        original_structure = {
            service: set(attrs.keys()) 
            for service, attrs in AWS_SERVICES.items()
        }
        
        # Verify structure hasn't changed
        current_keys = set(AWS_SERVICES.keys())
        assert current_keys == original_keys, "AWS_SERVICES keys have changed"
        
        for service in AWS_SERVICES:
            current_attrs = set(AWS_SERVICES[service].keys())
            expected_attrs = original_structure[service]
            assert current_attrs == expected_attrs, (
                f"Service {service} attributes have changed. "
                f"Expected: {expected_attrs}, Got: {current_attrs}"
            )


if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v"])


class TestCompatibilityEngine:
    """Test suite for the core compatibility calculation engine"""
    
    def test_calculate_compatibility_basic(self):
        """Basic test that calculate_compatibility works with valid input"""
        test_weights = UserWeights(
            operational_overhead=50,
            cost_sensitivity=50,
            workload_consistency=50,
            setup_speed=50
        )
        
        winner, winner_score, all_scores = calculate_compatibility(test_weights)
        
        # Basic validations
        assert winner in AWS_SERVICES.keys(), f"Winner {winner} not in AWS_SERVICES"
        assert 0 <= winner_score <= 100, f"Winner score {winner_score} not in range 0-100"
        assert len(all_scores) == 4, f"Expected 4 scores, got {len(all_scores)}"
        assert winner_score == max(all_scores.values()), "Winner should have highest score"
    
    @given(
        operational_overhead=st.integers(min_value=0, max_value=100),
        cost_sensitivity=st.integers(min_value=0, max_value=100),
        workload_consistency=st.integers(min_value=0, max_value=100),
        setup_speed=st.integers(min_value=0, max_value=100)
    )
    def test_calculate_compatibility_property(self, operational_overhead, cost_sensitivity, workload_consistency, setup_speed):
        """
        Feature: aws-compute-referee, Property 4: Compatibility calculation correctness
        Property test: For any valid user weights, the function should return valid results
        """
        user_weights = UserWeights(
            operational_overhead=operational_overhead,
            cost_sensitivity=cost_sensitivity,
            workload_consistency=workload_consistency,
            setup_speed=setup_speed
        )
        
        winner, winner_score, all_scores = calculate_compatibility(user_weights)
        
        # Property: Winner should have the highest score
        assert winner_score == max(all_scores.values()), "Winner must have highest score"
        
        # Property: All scores should be valid numbers between 0-100
        for service, score in all_scores.items():
            assert 0 <= score <= 100, f"Score for {service} ({score}) not in range 0-100"
            assert isinstance(score, (int, float)), f"Score for {service} is not numeric"
        
        # Property: Winner should be one of the valid services
        assert winner in AWS_SERVICES.keys(), f"Winner {winner} not in valid services"
        
        # Property: Should return scores for all services
        assert len(all_scores) == len(AWS_SERVICES), "Should return scores for all services"