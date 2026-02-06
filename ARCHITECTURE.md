# Vocabulary Visualization App - Architecture & Workflow

## 🎯 Core Concept

The Vocabulary Visualization App is a **full-stack web application** that helps users manage and visualize their vocabulary collections through multiple interactive views. Think of it as a personal vocabulary manager with powerful visualization capabilities.

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    USER'S BROWSER                            │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              React Frontend (Port 5173)                 │ │
│  │  - Login/Register UI                                    │ │
│  │  - Vocabulary Management (Add/Edit/Delete)              │ │
│  │  - Multiple Visualization Modes                         │ │
│  │  - CSV Import/Export UI                                 │ │
│  │  - Category Management                                  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                    HTTP/JSON API Calls
                            │
┌─────────────────────────────────────────────────────────────┐
│              Flask Backend API (Port 5001)                   │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  API Routes Layer                                       │ │
│  │  - /api/auth/* (login, logout, register)               │ │
│  │  - /api/vocab/* (CRUD operations)                       │ │
│  │  - /api/csv/* (import/export)                           │ │
│  │  - /api/categories/* (category management)              │ │
│  └────────────────────────────────────────────────────────┘ │
│                            │                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Business Logic Layer (Services)                        │ │
│  │  - AuthService: User authentication & sessions          │ │
│  │  - VocabularyService: CRUD, validation, CSV ops         │ │
│  │  - CategoryService: Category management                 │ │
│  │  - CSVParser: Parse & validate CSV files                │ │
│  └────────────────────────────────────────────────────────┘ │
│                            │                                 │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Data Access Layer (DAOs)                               │ │
│  │  - UserDAO, VocabularyDAO, CategoryDAO, SessionDAO      │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                    SQL Queries (SQLAlchemy ORM)
                            │
┌─────────────────────────────────────────────────────────────┐
│              SQLite Database (Local File)                    │
│  - users: User accounts with hashed passwords               │
│  - vocab_entries: Vocabulary words with all fields          │
│  - categories: User-defined categories                       │
│  - sessions: Active user sessions with tokens               │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 User Workflow

### 1. **Authentication Flow**
```
User Opens App
    ↓
Login/Register Page
    ↓
Enter Credentials → Backend validates → Create Session Token
    ↓
Token stored in browser (localStorage/sessionStorage)
    ↓
All subsequent API calls include token in Authorization header
```

### 2. **Main Application Flow**
```
Authenticated User
    ↓
Main Dashboard with Navigation
    ├─→ View Vocabulary (4 visualization modes)
    ├─→ Add/Edit/Delete Entries
    ├─→ Import CSV File
    ├─→ Export to CSV
    ├─→ Manage Categories
    └─→ Search & Filter
```

### 3. **Vocabulary Management Flow**
```
User Action → Frontend validates → API call with auth token
    ↓
Backend receives request → Validates session → Checks authorization
    ↓
Service layer validates data → Sanitizes input → Business logic
    ↓
DAO layer executes database operation
    ↓
Response sent back to frontend → UI updates
```

## 🎨 Frontend Architecture

### Component Hierarchy
```
App (Root)
├── AuthContext (Global authentication state)
├── Router
│   ├── LoginPage
│   │   └── LoginForm
│   ├── RegisterPage
│   │   └── RegisterForm
│   └── MainApp (Protected Route)
│       ├── Navigation Bar
│       ├── SearchBar
│       ├── FilterPanel
│       └── View Container (switches between views)
│           ├── CardView (Grid of vocabulary cards)
│           ├── WordCloudView (D3.js visualization)
│           ├── ListView (Sortable table)
│           └── CategorizedView (Grouped by categories)
```

### Key Frontend Components

1. **Authentication Components**
   - `LoginPage`: User login form
   - `RegisterPage`: New user registration
   - `AuthContext`: Manages authentication state globally
   - `ProtectedRoute`: Wrapper that requires authentication

2. **Vocabulary Components**
   - `VocabCard`: Displays a single vocabulary entry
   - `EntryEditor`: Form for creating/editing entries
   - `EntryDetailModal`: Shows full entry details

3. **Visualization Components**
   - `CardView`: Responsive grid of vocabulary cards
   - `WordCloudView`: D3.js word cloud (size based on frequency/importance)
   - `ListView`: Sortable, filterable table view
   - `CategorizedView`: Entries grouped by categories

4. **Utility Components**
   - `SearchBar`: Real-time search across all fields
   - `FilterPanel`: Multi-field filtering
   - `CSVUploader`: Drag-and-drop CSV import
   - `ExportButton`: Download vocabulary as CSV

## 🔐 Security Architecture

### Authentication & Authorization
1. **Password Security**
   - Passwords hashed with bcrypt (12 rounds)
   - Never stored in plain text
   - Salted automatically by bcrypt

2. **Session Management**
   - Secure random tokens (64 characters)
   - Stored in database with expiration
   - 24-hour default, 30-day "remember me"
   - Automatic extension on activity

3. **API Security**
   - All protected endpoints require Bearer token
   - Token validated on every request
   - User authorization checked (can only access own data)
   - Input sanitization (HTML escaping, SQL injection prevention)

4. **CORS Configuration**
   - Configured to allow frontend origin
   - Credentials supported for cookies/auth

## 📊 Data Flow Examples

### Example 1: Adding a Vocabulary Entry
```
1. User fills form in EntryEditor component
2. Frontend validates (required fields, length limits)
3. POST /api/vocab with entry data + auth token
4. Backend middleware validates token → injects user
5. VocabularyService.create_entry():
   - Sanitizes input (HTML escape)
   - Validates fields (word, meaning required, word ≤ 100 chars)
   - Checks for duplicates
   - Creates VocabEntry object
6. VocabularyDAO.insert() → SQLAlchemy → Database
7. Response with created entry (includes ID, timestamps)
8. Frontend updates UI, adds entry to local state
```

### Example 2: CSV Import
```
1. User drags CSV file to CSVUploader component
2. File read as bytes in browser
3. POST /api/csv/upload with file in multipart/form-data
4. Backend CSVParser:
   - Detects encoding (UTF-8, UTF-16, ASCII)
   - Detects delimiter (comma, semicolon, tab)
   - Detects header row
   - Parses all rows
   - Validates each entry
   - Handles duplicates (merge or skip)
5. VocabularyService.import_from_csv():
   - Creates entries for each valid row
   - Skips duplicates
   - Collects errors
6. Response with import statistics (imported, skipped, errors)
7. Frontend shows results, refreshes vocabulary list
```

### Example 3: Search & Filter
```
1. User types in SearchBar → debounced (300ms delay)
2. GET /api/vocab?search=<query>
3. VocabularyService.search_entries():
   - Case-insensitive search across all fields
   - Uses SQL LIKE with wildcards
4. Returns matching entries
5. Frontend updates current view with filtered results
6. Search highlights applied to matching text
```

## 🎯 Visualization Modes

### 1. Card View
- **Purpose**: Browse vocabulary like flashcards
- **Features**: 
  - Responsive grid layout
  - Shows all fields (word, meaning, synonym, pronunciation, example)
  - Click to view details or edit
  - Search highlighting

### 2. Word Cloud
- **Purpose**: Visual overview of vocabulary
- **Features**:
  - D3.js powered visualization
  - Word size based on frequency/length/importance
  - Color-coded for visual distinction
  - Click word to see full entry
  - Regenerates on data changes

### 3. List View
- **Purpose**: Systematic organization and sorting
- **Features**:
  - Sortable columns (click header to sort)
  - All fields visible in table
  - Multi-field filtering
  - Pagination for large datasets

### 4. Categorized View
- **Purpose**: Thematic organization
- **Features**:
  - Entries grouped by categories
  - Expandable/collapsible groups
  - "Uncategorized" group for entries without category
  - Drag-and-drop to reassign categories

## 🗄️ Database Schema

### Tables & Relationships
```
users (1) ──────┬──────→ (many) vocab_entries
                │
                ├──────→ (many) categories
                │
                └──────→ (many) sessions

categories (1) ─→ (many) vocab_entries
```

### Key Constraints
- **Unique**: (user_id, word) - No duplicate words per user
- **Unique**: (user_id, category_name) - No duplicate category names per user
- **Cascade Delete**: Deleting user deletes all their data
- **Set NULL**: Deleting category sets entries to uncategorized

## 🚀 Performance Considerations

1. **Database Indexing**
   - Indexes on user_id, word, category_id
   - Fast lookups for common queries

2. **Frontend Optimization**
   - Debounced search (reduces API calls)
   - Local state management (reduces re-fetches)
   - Lazy loading for large datasets

3. **API Efficiency**
   - Single query for filtered results
   - Batch operations for CSV import
   - Pagination support for large collections

## 📝 Development Workflow

### Backend Development
```
1. Define models (SQLAlchemy)
2. Create DAOs (database operations)
3. Implement services (business logic)
4. Create API routes (Flask blueprints)
5. Add error handling & logging
6. Write tests (unit + property-based)
```

### Frontend Development
```
1. Define TypeScript types
2. Create API client (Axios)
3. Build components (React + TypeScript)
4. Implement routing (React Router)
5. Add state management (Context API)
6. Style with Tailwind CSS
7. Write tests (Jest + React Testing Library)
```

## 🔧 Technology Stack Summary

### Backend
- **Language**: Python 3.9+
- **Framework**: Flask 3.0
- **ORM**: SQLAlchemy 2.0
- **Database**: SQLite
- **Auth**: bcrypt for password hashing
- **CSV**: pandas for parsing
- **Testing**: pytest + hypothesis (property-based)

### Frontend
- **Language**: TypeScript
- **Framework**: React 18+
- **Build Tool**: Vite
- **Routing**: React Router
- **HTTP**: Axios
- **Visualization**: D3.js, Recharts
- **Styling**: Tailwind CSS
- **Testing**: Jest + fast-check (property-based)

## 📚 Key Design Principles

1. **Separation of Concerns**: Clear layers (routes → services → DAOs → database)
2. **Security First**: Input sanitization, authentication, authorization at every level
3. **Data Integrity**: Validation at all entry points, transactions for consistency
4. **User Experience**: Multiple visualization modes, real-time search, responsive design
5. **Extensibility**: Modular components, easy to add new features
6. **Testability**: Comprehensive test coverage with unit and property-based tests

## 🎓 Learning Resources

- **Flask**: https://flask.palletsprojects.com/
- **React**: https://react.dev/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **D3.js**: https://d3js.org/
- **Tailwind CSS**: https://tailwindcss.com/

---

This architecture provides a solid foundation for a scalable, maintainable, and user-friendly vocabulary management application.
