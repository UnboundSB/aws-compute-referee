# Requirements Document

## Introduction

The AWS Compute Referee is a sophisticated Decision Support System built with Streamlit that helps developers choose the optimal AWS Compute service (EC2, Lambda, Fargate, App Runner) based on their specific requirements and priorities. The system uses a weighted scoring algorithm to analyze user preferences and provide data-driven recommendations with visual comparisons.

## Glossary

- **AWS_Compute_Referee**: The main Streamlit application system
- **Sidebar_Configurator**: The user interface component for inputting priorities
- **Logic_Engine**: The core Python calculation system for service compatibility scoring
- **Visualization_Engine**: The component responsible for displaying results and charts
- **User_Weights**: The priority values (0-100) input by users for each criterion
- **Compatibility_Score**: The calculated numerical score for each AWS service
- **Winner**: The AWS service with the highest compatibility score

## Requirements

### Requirement 1: Priority Input Interface

**User Story:** As a developer, I want to specify my priorities for different aspects of AWS compute services, so that I can get personalized recommendations.

#### Acceptance Criteria

1. THE Sidebar_Configurator SHALL display exactly four sliders in the sidebar
2. WHEN a user interacts with sliders, THE Sidebar_Configurator SHALL accept values from 0 to 100 for each priority
3. THE Sidebar_Configurator SHALL label the first slider "Operational Overhead" with description "Managed vs. Custom"
4. THE Sidebar_Configurator SHALL label the second slider "Cost Sensitivity" with description "Budget vs. Performance"
5. THE Sidebar_Configurator SHALL label the third slider "Workload Consistency" with description "Spiky vs. Steady"
6. THE Sidebar_Configurator SHALL label the fourth slider "Setup Speed" with description "Instant vs. Planned"
7. WHEN slider values change, THE AWS_Compute_Referee SHALL update recommendations in real-time

### Requirement 2: Service Data Management

**User Story:** As a system architect, I want the application to maintain accurate AWS service characteristics, so that recommendations are based on current service capabilities.

#### Acceptance Criteria

1. THE Logic_Engine SHALL define AWS service attributes in a Python dictionary called AWS_SERVICES
2. THE AWS_SERVICES dictionary SHALL contain exactly four services: EC2, Lambda, Fargate, and App Runner
3. FOR EACH service in AWS_SERVICES, THE Logic_Engine SHALL store numerical values for all four priority dimensions
4. THE Logic_Engine SHALL ensure all service attribute values are within the range 0-100
5. THE AWS_SERVICES dictionary SHALL remain immutable during application runtime

### Requirement 3: Compatibility Calculation

**User Story:** As a developer, I want the system to calculate which AWS service best matches my priorities, so that I can make informed decisions.

#### Acceptance Criteria

1. THE Logic_Engine SHALL implement a function called calculate_compatibility that accepts User_Weights as input
2. WHEN calculate_compatibility is called, THE Logic_Engine SHALL compute Compatibility_Score for each AWS service using weighted difference algorithm
3. THE Logic_Engine SHALL return the service with the highest Compatibility_Score as the Winner
4. WHEN multiple services have identical scores, THE Logic_Engine SHALL return the first service encountered
5. THE calculate_compatibility function SHALL complete execution within 100 milliseconds for any valid input

### Requirement 4: Results Display

**User Story:** As a developer, I want to see the recommended AWS service prominently displayed, so that I can quickly identify the best option.

#### Acceptance Criteria

1. WHEN a Winner is determined, THE Visualization_Engine SHALL display it using st.success() styling
2. THE Visualization_Engine SHALL show the Winner's name in a large metric readout format
3. THE Visualization_Engine SHALL display the Winner's Compatibility_Score alongside the service name
4. WHEN the Winner changes, THE Visualization_Engine SHALL update the display immediately
5. THE Visualization_Engine SHALL ensure the Winner display is visually distinct from other interface elements

### Requirement 5: Radar Chart Visualization

**User Story:** As a developer, I want to see a visual comparison between my ideal requirements and the recommended service, so that I can understand how well the recommendation matches my needs.

#### Acceptance Criteria

1. THE Visualization_Engine SHALL create a radar chart using Plotly Graph Objects
2. THE radar chart SHALL display exactly two data series: "User's Ideal" and "Winner's Stats"
3. THE radar chart SHALL show all four priority dimensions as axes: Operational Overhead, Cost Sensitivity, Workload Consistency, and Setup Speed
4. WHEN User_Weights change, THE Visualization_Engine SHALL update the "User's Ideal" series in real-time
5. WHEN the Winner changes, THE Visualization_Engine SHALL update the "Winner's Stats" series immediately
6. THE Visualization_Engine SHALL render the radar chart using st.plotly_chart()
7. THE radar chart SHALL use a scale from 0 to 100 for all axes

### Requirement 6: Application Architecture

**User Story:** As a system architect, I want the application to follow clean architecture principles, so that it is maintainable and extensible.

#### Acceptance Criteria

1. THE AWS_Compute_Referee SHALL separate user interface logic from business logic
2. THE Logic_Engine SHALL contain pure Python functions with no Streamlit dependencies
3. THE calculate_compatibility function SHALL be testable independently of the Streamlit interface
4. THE AWS_Compute_Referee SHALL organize code into logical sections: configuration, calculation, and visualization
5. WHEN the application starts, THE AWS_Compute_Referee SHALL initialize all components without errors

### Requirement 7: Performance and Responsiveness

**User Story:** As a developer, I want the application to respond quickly to my input changes, so that I can efficiently explore different scenarios.

#### Acceptance Criteria

1. WHEN any slider value changes, THE AWS_Compute_Referee SHALL update all displays within 200 milliseconds
2. THE AWS_Compute_Referee SHALL maintain responsive performance with concurrent user interactions
3. WHEN the application loads, THE AWS_Compute_Referee SHALL display the initial interface within 3 seconds
4. THE radar chart SHALL render completely within 500 milliseconds of data updates
5. THE AWS_Compute_Referee SHALL handle rapid slider movements without display lag or errors