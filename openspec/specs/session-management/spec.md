# session-management Specification

## Purpose
TBD - created by archiving change authentication. Update Purpose after archive.
## Requirements
### Requirement: Session created on successful login
The system SHALL create an in-memory session after successful authentication. The session SHALL NOT persist to disk.

#### Scenario: Session created
- **WHEN** authentication succeeds
- **THEN** the system SHALL record the session start time and mark the session as active

#### Scenario: Session not persisted
- **WHEN** the application restarts
- **THEN** any previous session SHALL be gone and the user SHALL be required to log in again

### Requirement: Session invalidated on logout
The system SHALL invalidate the active session when the user logs out.

#### Scenario: Logout clears session
- **WHEN** the user triggers logout
- **THEN** the session SHALL be cleared and the user SHALL be redirected to the lock-screen

### Requirement: Inactivity timeout
The system SHALL automatically invalidate the session after a configurable period of inactivity (`TLA_SESSION_TIMEOUT_MIN`, default 30 minutes).

#### Scenario: Session expires after inactivity
- **WHEN** no user interaction has occurred for longer than `TLA_SESSION_TIMEOUT_MIN` minutes
- **THEN** the session SHALL be invalidated and the user SHALL be redirected to the lock-screen

#### Scenario: Activity resets the timer
- **WHEN** the user interacts with the UI
- **THEN** the inactivity timer SHALL be reset

#### Scenario: Zero timeout disables auto-logout
- **WHEN** `TLA_SESSION_TIMEOUT_MIN` is set to 0
- **THEN** the session SHALL NOT expire automatically

### Requirement: Auth guard on protected routes
All application routes except `/login` and `/first-run` SHALL require an active session.

#### Scenario: Unauthenticated access redirected
- **WHEN** an unauthenticated request reaches a protected route
- **THEN** the system SHALL redirect to `/login`

