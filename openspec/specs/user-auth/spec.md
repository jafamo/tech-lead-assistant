# user-auth Specification

## Purpose
TBD - created by archiving change authentication. Update Purpose after archive.
## Requirements
### Requirement: Create user account
The system SHALL allow creating exactly one user account with username and password. If an account already exists, creation SHALL be rejected.

#### Scenario: Successful account creation
- **WHEN** no user exists in the database AND valid username and password are provided
- **THEN** the system SHALL hash the password with bcrypt (cost ≥ 12) and store the user record

#### Scenario: Duplicate account rejected
- **WHEN** a user account already exists
- **THEN** the system SHALL raise an error and NOT create a second account

#### Scenario: Weak password rejected
- **WHEN** a password shorter than 8 characters is provided
- **THEN** the system SHALL reject it with a descriptive error message

### Requirement: Verify password
The system SHALL verify a plaintext password against the stored bcrypt hash.

#### Scenario: Correct password accepted
- **WHEN** the provided password matches the stored hash
- **THEN** the system SHALL return success

#### Scenario: Wrong password rejected
- **WHEN** the provided password does NOT match the stored hash
- **THEN** the system SHALL return failure and increment the failed attempt counter

### Requirement: Exponential backoff on failed attempts
The system SHALL enforce an exponential delay after consecutive failed login attempts.

#### Scenario: Delay after third failure
- **WHEN** 3 or more consecutive failed attempts have occurred
- **THEN** the system SHALL wait `2^(attempts-3)` seconds (1s, 2s, 4s…) before allowing the next attempt, up to a maximum of 32 seconds

#### Scenario: Counter resets on success
- **WHEN** authentication succeeds
- **THEN** the failed attempt counter SHALL be reset to zero

### Requirement: Change password
The system SHALL allow changing the password when the current password is provided and correct.

#### Scenario: Successful password change
- **WHEN** the current password is correct AND the new password meets minimum requirements
- **THEN** the system SHALL re-hash and store the new password

#### Scenario: Wrong current password blocks change
- **WHEN** the current password provided is incorrect
- **THEN** the system SHALL reject the change and NOT modify the stored hash

