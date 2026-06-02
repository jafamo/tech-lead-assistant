# first-run-wizard Specification

## Purpose
TBD - created by archiving change authentication. Update Purpose after archive.
## Requirements
### Requirement: Detect first run
The system SHALL detect whether a user account exists on startup and route accordingly.

#### Scenario: No account exists — show wizard
- **WHEN** the application starts AND no user record exists in the database
- **THEN** the system SHALL display the first-run wizard instead of the lock-screen

#### Scenario: Account exists — show lock-screen
- **WHEN** the application starts AND a user record exists
- **THEN** the system SHALL display the lock-screen

### Requirement: Wizard step 1 — create account
The wizard SHALL collect username and password and create the user account.

#### Scenario: Valid credentials accepted
- **WHEN** the user provides a non-empty username and a password of at least 8 characters
- **THEN** the system SHALL create the account and proceed to step 2

#### Scenario: Password confirmation mismatch
- **WHEN** the password and confirmation fields do not match
- **THEN** the system SHALL display an error and NOT proceed

### Requirement: Wizard step 2 — confirm data root
The wizard SHALL show the current `TLA_DATA_ROOT` value and allow the user to confirm or change it.

#### Scenario: User confirms existing data root
- **WHEN** the user confirms the path shown
- **THEN** the system SHALL use that path and proceed

#### Scenario: User selects a new path
- **WHEN** the user provides a different path via the folder picker
- **THEN** the system SHALL update the runtime setting and proceed

### Requirement: FDE recommendation banner
After completing the wizard, the system SHALL display a one-time banner recommending Full Disk Encryption.

#### Scenario: Banner shown after first run
- **WHEN** the wizard completes successfully
- **THEN** the system SHALL display a banner mentioning BitLocker (Windows), LUKS (Linux), or FileVault (macOS) before navigating to Inicio

#### Scenario: Banner not shown on subsequent runs
- **WHEN** the application starts and a user account already exists
- **THEN** the FDE banner SHALL NOT be displayed

### Requirement: Initialize data root after wizard
After the wizard completes, the system SHALL call `InitializeDataRoot` and `PublishSchema`.

#### Scenario: Data root initialized
- **WHEN** the wizard completes
- **THEN** the system SHALL create the full data_root directory structure and publish the schema

