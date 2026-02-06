# Requirements Document

## Introduction

The Vocabulary Visualization App is a web-based application that enables users to manage, visualize, and interact with vocabulary collections. The system imports vocabulary data from CSV files, provides multiple visualization modes for exploring words, and allows users to edit and export their vocabulary collections. The application is designed for personal use with authentication to protect user data.

## Glossary

- **System**: The Vocabulary Visualization App web application
- **User**: An authenticated individual accessing the application
- **Vocabulary_Entry**: A single word record containing word, meaning, synonym, pronunciation, and example
- **CSV_File**: A comma-separated values file containing vocabulary data
- **Visualization_Mode**: A specific way of displaying vocabulary data (cards, word cloud, list, categories)
- **Search_Query**: User input text for filtering vocabulary entries
- **Filter_Criteria**: Conditions applied to narrow down displayed vocabulary entries
- **Session**: An authenticated user's active connection to the system

## Requirements

### Requirement 1: CSV File Import

**User Story:** As a user, I want to upload CSV files containing vocabulary data, so that I can import my existing vocabulary collections into the system.

#### Acceptance Criteria

1. WHEN a user uploads a valid CSV file with columns (word, meaning, synonym, pronunciation, example), THE System SHALL parse the file and extract all vocabulary entries
2. WHEN a user uploads a CSV file with missing optional columns, THE System SHALL parse available columns and create entries with partial data
3. IF a CSV file contains malformed data or invalid encoding, THEN THE System SHALL return a descriptive error message and reject the upload
4. WHEN a CSV file is successfully parsed, THE System SHALL display a confirmation showing the number of entries imported
5. WHEN duplicate words exist in an uploaded CSV file, THE System SHALL merge entries or prompt the user to choose which to keep

### Requirement 2: Vocabulary Storage and Retrieval

**User Story:** As a user, I want my vocabulary data stored reliably, so that I can access it across sessions without data loss.

#### Acceptance Criteria

1. WHEN a vocabulary entry is created or imported, THE System SHALL persist it to the database immediately
2. WHEN a user logs in, THE System SHALL retrieve all vocabulary entries associated with that user
3. THE System SHALL maintain data integrity ensuring no vocabulary entry is lost during normal operations
4. WHEN the database is queried, THE System SHALL return results within 500ms for collections up to 1000 words
5. THE System SHALL store vocabulary entries with all fields (word, meaning, synonym, pronunciation, example) preserving original formatting

### Requirement 3: Searchable Card View

**User Story:** As a user, I want to view vocabulary as searchable cards, so that I can quickly find and review specific words.

#### Acceptance Criteria

1. WHEN a user selects card view mode, THE System SHALL display vocabulary entries as individual cards showing all fields
2. WHEN a user types in the search box, THE System SHALL filter displayed cards in real-time to match the search query against any field
3. WHEN search results are displayed, THE System SHALL highlight matching text within the cards
4. WHEN no vocabulary entries match the search query, THE System SHALL display a message indicating no results found
5. THE System SHALL display cards in a responsive grid layout that adapts to different screen sizes

### Requirement 4: Word Cloud Visualization

**User Story:** As a user, I want to see my vocabulary as a word cloud, so that I can visualize word frequency and importance.

#### Acceptance Criteria

1. WHEN a user selects word cloud mode, THE System SHALL generate a visual word cloud from all vocabulary entries
2. THE System SHALL size words in the cloud based on a configurable metric (frequency, length, or user-defined importance)
3. WHEN a user clicks on a word in the cloud, THE System SHALL display the full vocabulary entry details
4. THE System SHALL render the word cloud with visually distinct colors and readable font sizes
5. WHEN the vocabulary collection changes, THE System SHALL regenerate the word cloud to reflect current data

### Requirement 5: Filterable List View

**User Story:** As a user, I want to view vocabulary as a filterable list, so that I can sort and organize words systematically.

#### Acceptance Criteria

1. WHEN a user selects list view mode, THE System SHALL display vocabulary entries in a tabular format with sortable columns
2. WHEN a user clicks a column header, THE System SHALL sort the list by that column in ascending or descending order
3. WHEN a user applies filters, THE System SHALL display only entries matching all active filter criteria
4. THE System SHALL provide filter options for each field (word, meaning, synonym, pronunciation, example)
5. WHEN filters are cleared, THE System SHALL restore the full vocabulary list

### Requirement 6: Categorized View

**User Story:** As a user, I want to group vocabulary by categories, so that I can organize words thematically.

#### Acceptance Criteria

1. WHEN a user assigns a category to vocabulary entries, THE System SHALL store the category association
2. WHEN a user selects categorized view mode, THE System SHALL display vocabulary entries grouped by their assigned categories
3. THE System SHALL allow users to create, rename, and delete categories
4. WHEN a vocabulary entry has no category, THE System SHALL place it in an "Uncategorized" group
5. WHEN a user expands a category, THE System SHALL display all vocabulary entries within that category

### Requirement 7: Vocabulary Entry Management

**User Story:** As a user, I want to create, edit, and delete vocabulary entries, so that I can maintain an accurate and current vocabulary collection.

#### Acceptance Criteria

1. WHEN a user creates a new vocabulary entry with a word and meaning, THE System SHALL add it to the collection
2. WHEN a user edits an existing vocabulary entry, THE System SHALL update the stored data and reflect changes immediately in all views
3. WHEN a user deletes a vocabulary entry, THE System SHALL remove it from the database and all visualizations
4. IF a user attempts to create a vocabulary entry with an empty word field, THEN THE System SHALL reject the entry and display a validation error
5. THE System SHALL validate that required fields (word, meaning) contain non-whitespace content before saving

### Requirement 8: CSV Export

**User Story:** As a user, I want to export my vocabulary collection to CSV format, so that I can back up my data or use it in other applications.

#### Acceptance Criteria

1. WHEN a user requests a CSV export, THE System SHALL generate a CSV file containing all vocabulary entries with proper formatting
2. THE System SHALL include all fields (word, meaning, synonym, pronunciation, example) in the exported CSV file
3. WHEN special characters or commas exist in vocabulary data, THE System SHALL properly escape them in the CSV output
4. WHEN a user exports filtered or searched results, THE System SHALL provide an option to export only visible entries or all entries
5. THE System SHALL trigger a file download with a descriptive filename including the export date

### Requirement 9: User Authentication

**User Story:** As a user, I want to log in with credentials, so that my vocabulary data remains private and secure.

#### Acceptance Criteria

1. WHEN a user provides valid credentials, THE System SHALL authenticate the user and create a session
2. IF a user provides invalid credentials, THEN THE System SHALL reject the login attempt and display an error message
3. WHEN a user is not authenticated, THE System SHALL redirect them to the login page and prevent access to vocabulary features
4. WHEN a user logs out, THE System SHALL terminate the session and clear authentication tokens
5. THE System SHALL store passwords using secure hashing algorithms (bcrypt or equivalent)

### Requirement 10: Session Management

**User Story:** As a user, I want my session to remain active while I work, so that I don't have to repeatedly log in.

#### Acceptance Criteria

1. WHEN a user successfully authenticates, THE System SHALL maintain the session for 24 hours of inactivity
2. WHEN a user closes the browser, THE System SHALL preserve the session if "remember me" was selected
3. WHEN a session expires, THE System SHALL redirect the user to the login page
4. THE System SHALL validate session tokens on every request to protected resources
5. WHEN a user activity occurs, THE System SHALL extend the session expiration time

### Requirement 11: Data Integrity and Validation

**User Story:** As a system administrator, I want data validation at all entry points, so that the database maintains consistent and valid data.

#### Acceptance Criteria

1. WHEN data is imported or entered, THE System SHALL validate all fields against defined constraints
2. THE System SHALL reject vocabulary entries where the word field exceeds 100 characters
3. THE System SHALL sanitize user input to prevent SQL injection and XSS attacks
4. WHEN database operations fail, THE System SHALL rollback transactions to maintain consistency
5. THE System SHALL enforce unique constraints on word entries per user to prevent duplicates

### Requirement 12: CSV Parsing Robustness

**User Story:** As a user, I want the system to handle various CSV formats gracefully, so that I can import files from different sources.

#### Acceptance Criteria

1. WHEN a CSV file uses different delimiters (comma, semicolon, tab), THE System SHALL detect and parse correctly
2. WHEN a CSV file contains quoted fields with embedded delimiters, THE System SHALL parse the fields correctly
3. WHEN a CSV file has inconsistent column counts across rows, THE System SHALL handle missing values gracefully
4. THE System SHALL support UTF-8, UTF-16, and ASCII encodings for CSV files
5. WHEN a CSV file contains a header row, THE System SHALL use it to map columns; otherwise use default column order

