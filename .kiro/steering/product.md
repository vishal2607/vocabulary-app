# Product Overview

The Vocabulary Visualization App is a full-stack web application that enables users to manage and visualize vocabulary collections through multiple interactive views.

## Purpose

To provide a comprehensive tool for vocabulary learning and management that allows users to:
- Import vocabulary data from CSV files
- Visualize vocabulary through multiple interactive modes
- Search, filter, and organize vocabulary entries
- Edit and maintain vocabulary collections
- Export vocabulary data for backup or external use

## Key Features

### 1. CSV Import/Export
- Upload CSV files with vocabulary data
- Support for multiple delimiters and encodings
- Robust error handling and validation
- Export vocabulary to CSV format with proper escaping

### 2. Multiple Visualization Modes
- **Card View**: Searchable cards displaying all vocabulary fields
- **Word Cloud**: Visual representation with configurable sizing metrics
- **List View**: Sortable, filterable table view
- **Categorized View**: Vocabulary grouped by user-defined categories

### 3. Search and Filter
- Real-time search across all fields
- Multi-field filtering
- Search result highlighting
- Filter combinations with AND logic

### 4. Vocabulary Management
- Create, edit, and delete vocabulary entries
- Assign categories to entries
- Manage categories (create, rename, delete)
- Input validation and sanitization

### 5. User Authentication
- Secure login with bcrypt password hashing
- Session management with configurable duration
- "Remember me" functionality
- Protected routes and API endpoints

### 6. Data Integrity
- SQLite database with SQLAlchemy ORM
- Transaction support with rollback on failure
- Unique constraints and foreign key relationships
- Input validation at all entry points

## Target Users

- **Language Learners**: Individuals studying new languages who need to organize and review vocabulary
- **Students**: Students building vocabulary for academic purposes
- **Teachers**: Educators creating vocabulary lists for their students
- **Writers**: Authors and content creators managing specialized terminology
- **Personal Use**: Anyone wanting to organize and visualize their vocabulary knowledge

## Technical Highlights

- **Full-stack TypeScript/Python**: Type-safe frontend with robust backend
- **Property-Based Testing**: Comprehensive test coverage using hypothesis and fast-check
- **Responsive Design**: Tailwind CSS for mobile-friendly interface
- **RESTful API**: Clean API design with consistent error handling
- **Local-First**: SQLite database for personal use without external dependencies
