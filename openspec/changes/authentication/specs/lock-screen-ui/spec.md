## ADDED Requirements

### Requirement: Lock-screen page
The system SHALL display a lock-screen page at `/login` with a password field and an unlock button.

#### Scenario: Correct password unlocks app
- **WHEN** the user enters the correct password and submits
- **THEN** the system SHALL create a session and redirect to `/` (Inicio)

#### Scenario: Wrong password shows error
- **WHEN** the user enters an incorrect password
- **THEN** the system SHALL display an inline error message without clearing the field

#### Scenario: Input disabled during backoff delay
- **WHEN** exponential backoff is active
- **THEN** the submit button and password field SHALL be disabled and a countdown SHALL be visible

### Requirement: Startup routing
The application SHALL route users to the correct page on startup based on application state.

#### Scenario: No account — wizard
- **WHEN** the app loads and no user account exists
- **THEN** the user SHALL be routed to `/first-run`

#### Scenario: Account exists, not authenticated — lock-screen
- **WHEN** the app loads and a user account exists but no active session
- **THEN** the user SHALL be routed to `/login`

#### Scenario: Active session — home
- **WHEN** the app loads and an active session exists
- **THEN** the user SHALL be routed to `/` (Inicio)
