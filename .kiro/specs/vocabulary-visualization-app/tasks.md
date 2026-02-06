# Implementation Plan: Vocabulary Visualization App

## Overview

This implementation plan breaks down the Vocabulary Visualization App into discrete coding tasks. The app consists of a Python/Flask backend with SQLite database and a React/TypeScript frontend. The implementation follows a bottom-up approach: database layer → business logic → API endpoints → frontend components → integration.

Tasks marked with `*` are optional and can be skipped for a faster MVP focused on core functionality.

## Tasks

- [x] 1. Set up project structure and development environment
  - Create backend directory structure (app/, tests/, config/)
  - Create frontend directory structure (src/components/, src/api/, src/types/)
  - Set up Python virtual environment and install dependencies (Flask, SQLAlchemy, pandas, bcrypt, pytest, hypothesis)
  - Initialize React/TypeScript project with Vite
  - Install frontend dependencies (React Router, Axios, D3.js, Recharts, Tailwind CSS, fast-check, Jest)
  - Create .gitignore and basic configuration files
  - _Requirements: All (foundational setup)_

- [ ] 2. Implement database layer and models
  - [x] 2.1 Create SQLAlchemy database models
    - Define User, VocabEntry, Category, and Session models
    - Set up relationships and constraints (foreign keys, unique constraints)
    - Create database initialization script
    - _Requirements: 2.1, 2.3, 9.5, 11.5_
  
  - [x] 2.2 Implement Data Access Objects (DAOs)
    - Write VocabularyDAO with CRUD operations (insert, update, delete, find_by_user, find_by_id, search)
    - Write UserDAO with user management operations
    - Write CategoryDAO with category operations
    - Write SessionDAO with session management operations
    - _Requirements: 2.1, 2.2, 2.3_
  
  - [ ]* 2.3 Write property test for vocabulary entry round-trip
    - **Property 11: Vocabulary Entry Round-Trip**
    - **Validates: Requirements 2.1, 2.5**
  
  - [ ]* 2.4 Write property test for user data isolation
    - **Property 12: User Data Isolation**
    - **Validates: Requirements 2.2**
  
  - [ ]* 2.5 Write unit tests for DAO edge cases
    - Test empty result sets, null handling, constraint violations
    - _Requirements: 2.1, 2.2, 2.3_

- [ ] 3. Implement CSV parsing service
  - [x] 3.1 Create CSV parser with encoding and delimiter detection
    - Implement detect_encoding() method supporting UTF-8, UTF-16, ASCII
    - Implement detect_delimiter() method for comma, semicolon, tab
    - Implement parse_csv() method with pandas
    - Handle header detection and column mapping
    - _Requirements: 1.1, 1.2, 12.1, 12.2, 12.3, 12.4, 12.5_
  
  - [x] 3.2 Add CSV parsing error handling
    - Implement validation for malformed data
    - Collect and return descriptive error messages with line numbers
    - Handle missing columns and inconsistent row lengths
    - _Requirements: 1.3, 12.3_
  
  - [x] 3.3 Implement duplicate handling logic
    - Detect duplicate words in CSV
    - Implement merge or conflict resolution strategy
    - _Requirements: 1.5_
  
  - [ ]* 3.4 Write property test for CSV parsing completeness
    - **Property 1: CSV Parsing Completeness**
    - **Validates: Requirements 1.1**
  
  - [ ]* 3.5 Write property test for CSV parsing with missing columns
    - **Property 2: CSV Parsing with Missing Columns**
    - **Validates: Requirements 1.2**
  
  - [ ]* 3.6 Write property test for CSV parsing error handling
    - **Property 3: CSV Parsing Error Handling**
    - **Validates: Requirements 1.3**
  
  - [ ]* 3.7 Write property test for CSV delimiter detection
    - **Property 6: CSV Delimiter Detection**
    - **Validates: Requirements 12.1**
  
  - [ ]* 3.8 Write property test for CSV encoding support
    - **Property 9: CSV Encoding Support**
    - **Validates: Requirements 12.4**
  
  - [ ]* 3.9 Write unit tests for CSV parsing edge cases
    - Test empty files, single row, special characters, very large files
    - _Requirements: 1.1, 1.2, 1.3, 12.1, 12.2, 12.3, 12.4, 12.5_

- [x] 4. Checkpoint - Ensure database and CSV parsing tests pass
  - Run all tests for database layer and CSV parsing
  - Verify database schema creation works correctly
  - Ask the user if questions arise

- [ ] 5. Implement authentication service
  - [x] 5.1 Create authentication service with password hashing
    - Implement register_user() with bcrypt password hashing
    - Implement authenticate() with password verification
    - Implement create_session() with token generation
    - Implement validate_session() with token validation
    - Implement logout() with session termination
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_
  
  - [x] 5.2 Implement session management logic
    - Add session expiration handling (24 hours default)
    - Add "remember me" functionality (extended expiration)
    - Add session activity extension on requests
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [ ]* 5.3 Write property test for valid credential authentication
    - **Property 39: Valid Credential Authentication**
    - **Validates: Requirements 9.1**
  
  - [ ]* 5.4 Write property test for invalid credential rejection
    - **Property 40: Invalid Credential Rejection**
    - **Validates: Requirements 9.2**
  
  - [ ]* 5.5 Write property test for password hashing
    - **Property 43: Password Hashing**
    - **Validates: Requirements 9.5**
  
  - [ ]* 5.6 Write property test for session duration
    - **Property 44: Session Duration**
    - **Validates: Requirements 10.1**
  
  - [ ]* 5.7 Write property test for expired session rejection
    - **Property 46: Expired Session Rejection**
    - **Validates: Requirements 10.3**
  
  - [ ]* 5.8 Write unit tests for authentication edge cases
    - Test rate limiting, concurrent sessions, token generation uniqueness
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 6. Implement vocabulary service
  - [x] 6.1 Create vocabulary service with CRUD operations
    - Implement create_entry() with validation
    - Implement update_entry() with validation
    - Implement delete_entry()
    - Implement get_entries() with filtering support
    - Implement search_entries() with full-text search
    - _Requirements: 7.1, 7.2, 7.3, 2.2, 3.2, 5.3_
  
  - [x] 6.2 Add input validation and sanitization
    - Validate required fields (word, meaning) are non-empty
    - Validate word length <= 100 characters
    - Sanitize inputs to prevent SQL injection and XSS
    - Enforce unique word constraint per user
    - _Requirements: 7.4, 7.5, 11.1, 11.2, 11.3, 11.5_
  
  - [x] 6.3 Implement CSV import and export methods
    - Implement import_from_csv() using CSV parser
    - Implement export_to_csv() with proper escaping
    - Add support for exporting filtered results
    - Generate descriptive filenames with dates
    - _Requirements: 1.1, 1.4, 8.1, 8.2, 8.3, 8.4, 8.5_
  
  - [ ]* 6.4 Write property test for vocabulary entry creation
    - **Property 29: Vocabulary Entry Creation**
    - **Validates: Requirements 7.1**
  
  - [ ]* 6.5 Write property test for vocabulary entry update
    - **Property 30: Vocabulary Entry Update**
    - **Validates: Requirements 7.2**
  
  - [ ]* 6.6 Write property test for vocabulary entry deletion
    - **Property 31: Vocabulary Entry Deletion**
    - **Validates: Requirements 7.3**
  
  - [ ]* 6.7 Write property test for search across all fields
    - **Property 13: Search Across All Fields**
    - **Validates: Requirements 3.2**
  
  - [ ]* 6.8 Write property test for multi-field filtering
    - **Property 14: Multi-Field Filtering**
    - **Validates: Requirements 5.3**
  
  - [ ]* 6.9 Write property test for empty field rejection
    - **Property 32: Empty Field Rejection**
    - **Validates: Requirements 7.4, 7.5**
  
  - [ ]* 6.10 Write property test for field length validation
    - **Property 33: Field Length Validation**
    - **Validates: Requirements 11.2**
  
  - [ ]* 6.11 Write property test for unique word constraint
    - **Property 36: Unique Word Constraint**
    - **Validates: Requirements 11.5**
  
  - [ ]* 6.12 Write property test for CSV export round-trip
    - **Property 37: CSV Export Round-Trip**
    - **Validates: Requirements 8.1, 8.2, 8.3**
  
  - [ ]* 6.13 Write unit tests for vocabulary service edge cases
    - Test concurrent updates, transaction rollbacks, validation errors
    - _Requirements: 7.1, 7.2, 7.3, 11.1, 11.2, 11.3, 11.4, 11.5_

- [ ] 7. Implement category service
  - [x] 7.1 Create category service with CRUD operations
    - Implement create_category()
    - Implement update_category()
    - Implement delete_category()
    - Implement get_categories()
    - Handle category assignment to vocabulary entries
    - _Requirements: 6.1, 6.3_
  
  - [ ]* 7.2 Write property test for category assignment persistence
    - **Property 24: Category Assignment Persistence**
    - **Validates: Requirements 6.1**
  
  - [ ]* 7.3 Write property test for category CRUD operations
    - **Property 26: Category CRUD Operations**
    - **Validates: Requirements 6.3**
  
  - [ ]* 7.4 Write unit tests for category edge cases
    - Test category deletion with assigned entries, duplicate names
    - _Requirements: 6.1, 6.3_

- [x] 8. Checkpoint - Ensure all backend services tests pass
  - Run all tests for authentication, vocabulary, and category services
  - Verify business logic correctness
  - Ask the user if questions arise

- [ ] 9. Implement Flask API endpoints
  - [x] 9.1 Create authentication endpoints
    - POST /api/auth/login (authenticate and create session)
    - POST /api/auth/logout (terminate session)
    - GET /api/auth/validate (validate session token)
    - Add authentication middleware for protected routes
    - _Requirements: 9.1, 9.2, 9.3, 9.4_
  
  - [x] 9.2 Create vocabulary endpoints
    - GET /api/vocab (retrieve entries with filters and search)
    - POST /api/vocab (create new entry)
    - PUT /api/vocab/:id (update entry)
    - DELETE /api/vocab/:id (delete entry)
    - Add request validation and error handling
    - _Requirements: 2.2, 3.2, 5.3, 7.1, 7.2, 7.3_
  
  - [x] 9.3 Create CSV endpoints
    - POST /api/csv/upload (upload and import CSV)
    - GET /api/csv/export (export entries to CSV)
    - Handle file uploads with multipart/form-data
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 8.1, 8.2, 8.3, 8.4, 8.5_
  
  - [x] 9.4 Create category endpoints
    - GET /api/categories (retrieve all categories)
    - POST /api/categories (create category)
    - PUT /api/categories/:id (update category)
    - DELETE /api/categories/:id (delete category)
    - _Requirements: 6.1, 6.3_
  
  - [x] 9.5 Add global error handling and logging
    - Implement consistent error response format
    - Add request/response logging
    - Add CORS configuration for frontend
    - _Requirements: All (cross-cutting concern)_
  
  - [ ]* 9.6 Write property test for unauthenticated access prevention
    - **Property 41: Unauthenticated Access Prevention**
    - **Validates: Requirements 9.3**
  
  - [ ]* 9.7 Write property test for logout session termination
    - **Property 42: Logout Session Termination**
    - **Validates: Requirements 9.4**
  
  - [ ]* 9.8 Write integration tests for API endpoints
    - Test complete request/response cycles for all endpoints
    - Test authentication flow, error responses, edge cases
    - _Requirements: All API-related requirements_

- [x] 10. Checkpoint - Ensure backend API tests pass
  - Run all integration tests for API endpoints
  - Test API manually with curl or Postman
  - Ask the user if questions arise

- [ ] 11. Implement TypeScript types and API client
  - [ ] 11.1 Define TypeScript interfaces
    - Create VocabEntry, User, Category, FilterCriteria interfaces
    - Create ParseResult, ImportResult interfaces
    - Create API request/response types
    - _Requirements: All (type safety)_
  
  - [ ] 11.2 Implement API client classes
    - Create VocabularyAPI class with all vocabulary endpoints
    - Create AuthAPI class with authentication endpoints
    - Create CategoryAPI class with category endpoints
    - Add error handling and response parsing
    - Configure Axios with base URL and interceptors
    - _Requirements: All API-related requirements_
  
  - [ ]* 11.3 Write unit tests for API client
    - Mock API responses and test client methods
    - Test error handling and edge cases
    - _Requirements: All API-related requirements_

- [ ] 12. Implement authentication UI components
  - [ ] 12.1 Create login page component
    - Build login form with username, password, remember me
    - Add form validation and error display
    - Integrate with AuthAPI
    - Handle successful login (store token, redirect)
    - _Requirements: 9.1, 9.2, 10.2_
  
  - [ ] 12.2 Create authentication context and protected routes
    - Implement React context for authentication state
    - Create ProtectedRoute component
    - Add automatic redirect to login for unauthenticated users
    - Add logout functionality
    - _Requirements: 9.3, 9.4_
  
  - [ ]* 12.3 Write unit tests for authentication components
    - Test login form validation, error handling, successful login flow
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [ ] 13. Implement search and filter components
  - [ ] 13.1 Create SearchBar component
    - Build search input with real-time filtering
    - Add debouncing to prevent excessive API calls
    - Integrate with vocabulary state management
    - _Requirements: 3.2_
  
  - [ ] 13.2 Create FilterPanel component
    - Build multi-field filter controls (word, meaning, synonym, category)
    - Add clear filters functionality
    - Integrate with vocabulary state management
    - _Requirements: 5.3, 5.4, 5.5_
  
  - [ ]* 13.3 Write unit tests for search and filter components
    - Test search input, debouncing, filter controls
    - _Requirements: 3.2, 5.3, 5.4, 5.5_

- [ ] 14. Implement vocabulary entry management components
  - [ ] 14.1 Create EntryEditor component
    - Build form for creating/editing vocabulary entries
    - Add field validation (required fields, length limits)
    - Integrate with VocabularyAPI
    - Handle save and cancel actions
    - _Requirements: 7.1, 7.2, 7.4, 7.5_
  
  - [ ] 14.2 Create entry detail modal/dialog
    - Display full vocabulary entry details
    - Add edit and delete buttons
    - Handle delete confirmation
    - _Requirements: 7.2, 7.3_
  
  - [ ]* 14.3 Write unit tests for entry management components
    - Test form validation, save/cancel actions, delete confirmation
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 15. Implement Card View visualization
  - [ ] 15.1 Create CardView component
    - Build responsive grid layout for vocabulary cards
    - Display all fields (word, meaning, synonym, pronunciation, example)
    - Add click handlers for viewing/editing entries
    - Integrate with search highlighting
    - _Requirements: 3.1, 3.3, 3.5_
  
  - [ ] 15.2 Add search highlighting to cards
    - Implement text highlighting for search matches
    - Highlight matches across all fields
    - _Requirements: 3.3_
  
  - [ ] 15.3 Add empty state handling
    - Display message when no entries match search
    - _Requirements: 3.4_
  
  - [ ]* 15.4 Write property test for card view completeness
    - **Property 16: Card View Completeness**
    - **Validates: Requirements 3.1**
  
  - [ ]* 15.5 Write property test for search highlighting
    - **Property 17: Search Highlighting**
    - **Validates: Requirements 3.3**
  
  - [ ]* 15.6 Write unit tests for CardView component
    - Test rendering with various entry data, empty states, click handlers
    - _Requirements: 3.1, 3.3, 3.4, 3.5_

- [ ] 16. Implement Word Cloud visualization
  - [ ] 16.1 Create WordCloudView component
    - Integrate D3.js for word cloud rendering
    - Implement sizing based on configurable metric (frequency, length, importance)
    - Add color variation for visual distinction
    - Add click handlers to show entry details
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  
  - [ ] 16.2 Add word cloud regeneration on data changes
    - Detect vocabulary collection changes
    - Trigger word cloud regeneration
    - _Requirements: 4.5_
  
  - [ ]* 16.3 Write property test for word cloud completeness
    - **Property 18: Word Cloud Completeness**
    - **Validates: Requirements 4.1**
  
  - [ ]* 16.4 Write property test for word cloud click mapping
    - **Property 20: Word Cloud Click Mapping**
    - **Validates: Requirements 4.3**
  
  - [ ]* 16.5 Write unit tests for WordCloudView component
    - Test rendering, sizing calculations, click handlers
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ] 17. Implement List View visualization
  - [ ] 17.1 Create ListView component
    - Build sortable table with all vocabulary fields
    - Implement column sorting (ascending/descending)
    - Add sort indicators to column headers
    - Integrate with filter functionality
    - _Requirements: 5.1, 5.2, 5.3_
  
  - [ ] 17.2 Add filter restoration functionality
    - Implement clear filters button
    - Restore full list when filters cleared
    - _Requirements: 5.5_
  
  - [ ]* 17.3 Write property test for list view completeness
    - **Property 22: List View Completeness**
    - **Validates: Requirements 5.1**
  
  - [ ]* 17.4 Write property test for list sorting correctness
    - **Property 23: List Sorting Correctness**
    - **Validates: Requirements 5.2**
  
  - [ ]* 17.5 Write unit tests for ListView component
    - Test sorting, filtering, empty states
    - _Requirements: 5.1, 5.2, 5.3, 5.5_

- [ ] 18. Implement Categorized View visualization
  - [ ] 18.1 Create CategorizedView component
    - Display vocabulary entries grouped by categories
    - Implement expandable/collapsible category groups
    - Show "Uncategorized" group for entries without categories
    - Add category management UI (create, rename, delete)
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [ ]* 18.2 Write property test for categorized grouping
    - **Property 25: Categorized Grouping**
    - **Validates: Requirements 6.2**
  
  - [ ]* 18.3 Write property test for uncategorized default grouping
    - **Property 27: Uncategorized Default Grouping**
    - **Validates: Requirements 6.4**
  
  - [ ]* 18.4 Write property test for category expansion completeness
    - **Property 28: Category Expansion Completeness**
    - **Validates: Requirements 6.5**
  
  - [ ]* 18.5 Write unit tests for CategorizedView component
    - Test grouping, expansion, category management
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 19. Implement CSV import/export UI
  - [ ] 19.1 Create CSV upload component
    - Build file upload interface
    - Add drag-and-drop support
    - Display upload progress and results
    - Show import confirmation with entry count
    - Handle and display parsing errors
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  
  - [ ] 19.2 Create CSV export functionality
    - Add export button to main UI
    - Provide option to export all or filtered entries
    - Trigger file download with descriptive filename
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
  
  - [ ]* 19.3 Write unit tests for CSV import/export components
    - Test file upload, error display, export functionality
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 20. Implement main application layout and routing
  - [ ] 20.1 Create main app layout
    - Build navigation bar with view mode selector
    - Add logout button
    - Create responsive layout container
    - _Requirements: All (UI structure)_
  
  - [ ] 20.2 Set up React Router
    - Configure routes for login, main app, different views
    - Implement view mode switching (cards, word cloud, list, categories)
    - Add protected route wrapper
    - _Requirements: All (navigation)_
  
  - [ ] 20.3 Implement vocabulary state management
    - Create React context or state management for vocabulary data
    - Handle loading states and error states
    - Implement data fetching and caching
    - _Requirements: 2.2, 2.4_
  
  - [ ]* 20.4 Write integration tests for main app
    - Test navigation, view switching, state management
    - _Requirements: All (integration)_

- [ ] 21. Checkpoint - Ensure all frontend tests pass
  - Run all frontend unit and property tests
  - Test UI manually in browser
  - Verify all visualizations render correctly
  - Ask the user if questions arise

- [ ] 22. Integrate frontend and backend
  - [ ] 22.1 Configure frontend to connect to backend API
    - Set up API base URL configuration
    - Configure CORS on backend
    - Test authentication flow end-to-end
    - _Requirements: All (integration)_
  
  - [ ] 22.2 Test complete user workflows
    - Test login → view vocabulary → search → edit → logout
    - Test CSV upload → view imported data → export
    - Test category creation → assignment → categorized view
    - _Requirements: All (integration)_
  
  - [ ] 22.3 Add loading states and error handling throughout UI
    - Show loading spinners during API calls
    - Display user-friendly error messages
    - Handle network errors gracefully
    - _Requirements: All (UX)_
  
  - [ ]* 22.4 Write end-to-end integration tests
    - Test complete user workflows with real backend
    - _Requirements: All (integration)_

- [ ] 23. Final checkpoint - Complete testing and validation
  - Run complete test suite (backend + frontend)
  - Verify all requirements are met
  - Test with sample vocabulary data
  - Ensure all tests pass
  - Ask the user if questions arise

- [ ] 24. Add documentation and deployment preparation
  - [ ] 24.1 Create README with setup instructions
    - Document installation steps
    - Document how to run backend and frontend
    - Document API endpoints
    - Add sample CSV format
    - _Requirements: All (documentation)_
  
  - [ ] 24.2 Add environment configuration
    - Create .env.example files for backend and frontend
    - Document required environment variables
    - Add configuration for database path, secret keys, API URLs
    - _Requirements: All (configuration)_
  
  - [ ]* 24.3 Create Docker configuration (optional)
    - Create Dockerfile for backend
    - Create Dockerfile for frontend
    - Create docker-compose.yml for local development
    - _Requirements: All (deployment)_

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP delivery
- Each task references specific requirements for traceability
- Property-based tests validate universal correctness properties across many generated inputs
- Unit tests validate specific examples, edge cases, and error conditions
- Checkpoints ensure incremental validation and provide opportunities to address issues early
- The implementation follows a layered approach: data → logic → API → UI → integration
- Local development is prioritized; AWS deployment can be added later as optional tasks
