# Implementation Plan: AWS Compute Referee

## Overview

This implementation plan breaks down the AWS Compute Referee application into discrete, manageable coding tasks. Each task builds incrementally toward a complete Streamlit application that helps developers choose the optimal AWS compute service based on their priorities. The implementation follows clean architecture principles with clear separation between business logic, user interface, and visualization components.

## Tasks

- [x] 1. Set up project structure and core data models
  - Create app.py as the main Streamlit application file
  - Create requirements.txt with necessary dependencies (streamlit, plotly, typing)
  - Define the AWS_SERVICES dictionary with service characteristics
  - Define TypedDict models for UserWeights and ServiceCharacteristics
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 6.5_

- [x] 1.1 Write property test for AWS_SERVICES data structure
  - **Property 2: Service data structure consistency**
  - **Validates: Requirements 2.3**

- [x] 1.2 Write property test for service attribute value ranges
  - **Property 1: Input validation and range compliance (service attributes)**
  - **Validates: Requirements 2.4**

- [x] 2. Implement core compatibility calculation logic
  - [x] 2.1 Create calculate_compatibility function with weighted difference algorithm
    - Implement pure Python function that accepts user weights dictionary
    - Calculate Euclidean distance between user preferences and service characteristics
    - Convert distances to compatibility scores (0-100 scale)
    - Return winner service name, winner score, and all scores dictionary
    - _Requirements: 3.1, 3.2, 3.3, 3.4_

  - [x] 2.2 Write property test for compatibility calculation correctness
    - **Property 4: Compatibility calculation correctness**
    - **Validates: Requirements 3.2, 3.3**

  - [x] 2.3 Write property test for calculation performance
    - **Property 5: Performance requirements**
    - **Validates: Requirements 3.5**

  - [x] 2.4 Write unit test for tie-breaking behavior
    - Test specific case where multiple services have identical scores
    - _Requirements: 3.4_

- [x] 3. Checkpoint - Ensure core logic tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 4. Implement Streamlit sidebar configurator
  - [x] 4.1 Create sidebar sliders for user priority input
    - Implement four sliders with labels: "Operational Overhead", "Cost Sensitivity", "Workload Consistency", "Setup Speed"
    - Add descriptive help text for each slider ("Managed vs. Custom", etc.)
    - Set appropriate default values and 0-100 range for all sliders
    - Return user weights as dictionary
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6_

  - [x] 4.2 Write unit tests for sidebar component structure
    - Test that exactly four sliders are created with correct labels
    - _Requirements: 1.1, 1.3, 1.4, 1.5, 1.6_

  - [x] 4.3 Write property test for input validation
    - **Property 1: Input validation and range compliance (user inputs)**
    - **Validates: Requirements 1.2**

- [x] 5. Implement winner display and metrics
  - [x] 5.1 Create winner display with st.success styling
    - Display winner service name using st.success()
    - Show compatibility score in large metric format using st.metric()
    - Ensure winner display updates when recommendations change
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

  - [x] 5.2 Write property test for display reactivity
    - **Property 6: Reactive display updates (winner display)**
    - **Validates: Requirements 4.4**

  - [x] 5.3 Write unit tests for winner display formatting
    - Test that winner name and score are displayed correctly
    - _Requirements: 4.2, 4.3_

- [x] 6. Implement radar chart visualization
  - [x] 6.1 Create radar chart using Plotly Graph Objects
    - Implement create_radar_chart function using plotly.graph_objects.Scatterpolar
    - Create two traces: "User's Ideal" (user weights) and "Winner's Stats" (service characteristics)
    - Configure radial axes for all four priority dimensions with 0-100 scale
    - Apply appropriate styling, colors, and fill areas
    - _Requirements: 5.1, 5.2, 5.3, 5.6, 5.7_

  - [x] 6.2 Integrate radar chart with Streamlit display
    - Render chart using st.plotly_chart()
    - Ensure chart updates when user weights or winner changes
    - _Requirements: 5.4, 5.5, 5.6_

  - [x] 6.3 Write property test for chart data reactivity
    - **Property 7: Chart data reactivity**
    - **Validates: Requirements 5.4, 5.5**

  - [x] 6.4 Write unit tests for chart structure
    - Test that chart contains exactly two traces with correct names
    - Test that all four axes are present with correct labels
    - _Requirements: 5.2, 5.3, 5.7_

- [x] 7. Implement main application integration and reactivity
  - [x] 7.1 Wire all components together in main application flow
    - Create main() function that orchestrates sidebar, calculation, and display
    - Implement reactive updates when slider values change
    - Ensure real-time recommendation updates
    - Add error handling and graceful degradation
    - _Requirements: 1.7, 6.1, 6.2, 6.3_

  - [x] 7.2 Write property test for end-to-end reactivity
    - **Property 6: Reactive display updates (complete system)**
    - **Validates: Requirements 1.7**

  - [x] 7.3 Write property test for system responsiveness
    - **Property 8: System responsiveness**
    - **Validates: Requirements 7.1, 7.4, 7.5**

- [x] 8. Add data immutability and architecture validation
  - [x] 8.1 Implement safeguards for AWS_SERVICES immutability
    - Add validation to ensure AWS_SERVICES dictionary remains unchanged during runtime
    - Implement defensive copying if needed
    - _Requirements: 2.5, 6.2_

  - [x] 8.2 Write property test for data immutability
    - **Property 3: Data immutability during execution**
    - **Validates: Requirements 2.5**

  - [x] 8.3 Write unit tests for architecture separation
    - Test that calculate_compatibility function has no Streamlit dependencies
    - Test that function can be called independently of UI
    - _Requirements: 6.2, 6.3_

- [x] 9. Final integration and performance optimization
  - [x] 9.1 Optimize application startup and performance
    - Ensure application initializes within 3 seconds
    - Optimize chart rendering performance
    - Add caching where appropriate using st.cache_data
    - _Requirements: 7.2, 7.3_

  - [x] 9.2 Write unit tests for startup performance
    - Test application initialization time
    - _Requirements: 7.3_

- [x] 10. Final checkpoint - Complete system validation
  - Ensure all tests pass, ask the user if questions arise.
  - Verify complete application functionality from sidebar input to chart display
  - Test error handling and edge cases
  - Validate that all requirements are met

## Notes

- All tasks are required for comprehensive development with full testing coverage
- Each task references specific requirements for traceability
- Property tests validate universal correctness properties across all inputs
- Unit tests validate specific examples, edge cases, and architectural constraints
- The implementation follows clean architecture with pure Python business logic separate from Streamlit UI components
- Checkpoints ensure incremental validation and provide opportunities for user feedback