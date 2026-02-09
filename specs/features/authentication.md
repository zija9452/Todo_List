# Authentication Feature Specification

**Feature**: Secure user authentication and authorization for task management
**Gherkin Acceptance Criteria**:

```gherkin
Feature: User Authentication and Authorization
  Scenario: User accesses protected task endpoints
    Given I am a logged-in user with a valid JWT token
    When I make an API request to a protected endpoint
    Then my JWT token is validated and my identity verified

  Scenario: User attempts unauthorized access
    Given I am logged in with valid credentials
    When I attempt to access another user's tasks
    Then I receive a 403 Forbidden error

  Scenario: Unauthenticated access attempt
    Given I am not logged in or have an invalid JWT token
    When I attempt to access protected resources
    Then I receive a 401 Unauthorized error
```