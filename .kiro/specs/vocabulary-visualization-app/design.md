# Design Document: Vocabulary Visualization App

## Overview

The Vocabulary Visualization App is a full-stack web application that enables users to manage and visualize vocabulary collections through multiple interactive views. The system consists of a Python/Flask backend for data processing and API services, a React/TypeScript frontend for user interaction, and SQLite for local data persistence.

The application follows a client-server architecture where the frontend communicates with the backend via RESTful APIs. The backend handles CSV parsing, data validation, storage operations, and authentication, while the frontend provides rich interactive visualizations and user interface components.

Key design principles:
- **Separation of concerns**: Clear boundaries between data layer, business logic, and presentation
- **Data integrity**: Validation at all entry points with transactional consistency
- **Extensibility**: Modular visualization components that can be easily extended
- **Security**: Input sanitization, secure authentication, and session management
- **Performance**: Efficient querying and caching for responsive user experience

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │           React/TypeScript Frontend                     │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │ │
│  │  │  Card    │  │   Word   │  │   List   │            │ │
│  │  │  View    │  │  Cloud   │  │   View   │  ...       │ │
│  │  └──────────┘  └──────────┘  └──────────┘            │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │        Search & Filter Components                 │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │        API Client (Axios/Fetch)                   │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                    HTTP/JSON API
                            │
┌─────────────────────────────────────────────────────────────┐
│                   Python/Flask Backend                       │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                  API Routes Layer                       │ │
│  │  /api/auth  /api/vocab  /api/csv  /api/export         │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Business Logic Layer                       │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │ │
│  │  │   CSV    │  │  Vocab   │  │   Auth   │            │ │
│  │  │  Parser  │  │ Service  │  │ Service  │            │ │
│  │  └──────────┘  └──────────┘  └──────────┘            │ │
│  └────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────┐ │
│  │                Data Access Layer                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐            │ │
│  │  │  Vocab   │  │   User   │  │ Session  │            │ │
│  │  │   DAO    │  │   DAO    │  │   DAO    │            │ │
│  │  └──────────┘  └──────────┘  └──────────┘            │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                    SQL Queries
                            │
┌─────────────────────────────────────────────────────────────┐
│                    SQLite Database                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │  users   │  │  vocab   │  │ sessions │                  │
│  └──────────┘  └──────────┘  └──────────┘                 │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Python 3.9+
- Flask 2.x (web framework)
- Flask-Login (session management)
- SQLAlchemy (ORM)
- pandas (CSV processing)
- bcrypt (password hashing)
- pytest (testing)

**Frontend:**
- React 18+ with TypeScript
- React Router (navigation)
- Axios (HTTP client)
- D3.js (word cloud visualization)
- Recharts (charts and graphs)
- Tailwind CSS (styling)
- Jest + React Testing Library (testing)

**Database:**
- SQLite (local development and personal use)

**Development Tools:**
- Vite (frontend build tool)
- ESLint + Prettier (code quality)
- pytest + coverage (backend testing)

## Components and Interfaces

### Backend Components

#### 1. CSV Parser Service

**Responsibility:** Parse CSV files and extract vocabulary entries

**Interface:**
```python
class CSVParser:
    def parse_csv(self, file_content: bytes, encoding: str = 'utf-8') -> ParseResult:
        """
        Parse CSV file content into vocabulary entries.
        
        Args:
            file_content: Raw bytes of the CSV file
            encoding: Character encoding (utf-8, utf-16, ascii)
            
        Returns:
            ParseResult containing list of VocabEntry objects and any errors
            
        Raises:
            CSVParseError: If file is malformed or unreadable
        """
        pass
    
    def detect_delimiter(self, sample: str) -> str:
        """Detect CSV delimiter from file sample"""
        pass
    
    def detect_encoding(self, file_content: bytes) -> str:
        """Detect file encoding"""
        pass
```

**Key Methods:**
- `parse_csv()`: Main parsing logic with error handling
- `detect_delimiter()`: Auto-detect comma, semicolon, or tab delimiters
- `detect_encoding()`: Detect UTF-8, UTF-16, or ASCII encoding
- `validate_row()`: Validate individual CSV rows
- `merge_duplicates()`: Handle duplicate word entries

#### 2. Vocabulary Service

**Responsibility:** Business logic for vocabulary CRUD operations

**Interface:**
```python
class VocabularyService:
    def create_entry(self, user_id: int, entry: VocabEntry) -> VocabEntry:
        """Create a new vocabulary entry"""
        pass
    
    def update_entry(self, entry_id: int, updates: dict) -> VocabEntry:
        """Update an existing vocabulary entry"""
        pass
    
    def delete_entry(self, entry_id: int) -> bool:
        """Delete a vocabulary entry"""
        pass
    
    def get_entries(self, user_id: int, filters: dict = None) -> list[VocabEntry]:
        """Retrieve vocabulary entries with optional filters"""
        pass
    
    def search_entries(self, user_id: int, query: str) -> list[VocabEntry]:
        """Search vocabulary entries across all fields"""
        pass
    
    def import_from_csv(self, user_id: int, csv_data: ParseResult) -> ImportResult:
        """Import vocabulary entries from parsed CSV data"""
        pass
    
    def export_to_csv(self, user_id: int, entry_ids: list[int] = None) -> str:
        """Export vocabulary entries to CSV format"""
        pass
```

#### 3. Authentication Service

**Responsibility:** User authentication and session management

**Interface:**
```python
class AuthService:
    def register_user(self, username: str, password: str) -> User:
        """Register a new user with hashed password"""
        pass
    
    def authenticate(self, username: str, password: str) -> User:
        """Authenticate user credentials"""
        pass
    
    def create_session(self, user_id: int, remember: bool = False) -> Session:
        """Create a new user session"""
        pass
    
    def validate_session(self, session_token: str) -> User:
        """Validate session token and return user"""
        pass
    
    def logout(self, session_token: str) -> bool:
        """Terminate user session"""
        pass
```

#### 4. Data Access Objects (DAOs)

**VocabularyDAO:**
```python
class VocabularyDAO:
    def insert(self, entry: VocabEntry) -> int:
        """Insert vocabulary entry and return ID"""
        pass
    
    def update(self, entry_id: int, fields: dict) -> bool:
        """Update vocabulary entry fields"""
        pass
    
    def delete(self, entry_id: int) -> bool:
        """Delete vocabulary entry"""
        pass
    
    def find_by_user(self, user_id: int) -> list[VocabEntry]:
        """Find all entries for a user"""
        pass
    
    def find_by_id(self, entry_id: int) -> VocabEntry:
        """Find entry by ID"""
        pass
    
    def search(self, user_id: int, query: str) -> list[VocabEntry]:
        """Full-text search across all fields"""
        pass
```

### Frontend Components

#### 1. Visualization Components

**CardView Component:**
```typescript
interface CardViewProps {
  entries: VocabEntry[];
  searchQuery: string;
  onEntryClick: (entry: VocabEntry) => void;
  onEntryEdit: (entry: VocabEntry) => void;
  onEntryDelete: (entryId: number) => void;
}

const CardView: React.FC<CardViewProps> = (props) => {
  // Render vocabulary entries as cards with search highlighting
};
```

**WordCloudView Component:**
```typescript
interface WordCloudViewProps {
  entries: VocabEntry[];
  sizingMetric: 'frequency' | 'length' | 'importance';
  onWordClick: (entry: VocabEntry) => void;
}

const WordCloudView: React.FC<WordCloudViewProps> = (props) => {
  // Render D3.js word cloud visualization
};
```

**ListView Component:**
```typescript
interface ListViewProps {
  entries: VocabEntry[];
  sortColumn: string;
  sortDirection: 'asc' | 'desc';
  filters: FilterCriteria;
  onSort: (column: string) => void;
  onFilter: (filters: FilterCriteria) => void;
}

const ListView: React.FC<ListViewProps> = (props) => {
  // Render sortable, filterable table view
};
```

**CategorizedView Component:**
```typescript
interface CategorizedViewProps {
  entries: VocabEntry[];
  categories: Category[];
  onCategoryCreate: (name: string) => void;
  onCategoryEdit: (category: Category) => void;
  onCategoryDelete: (categoryId: number) => void;
}

const CategorizedView: React.FC<CategorizedViewProps> = (props) => {
  // Render entries grouped by categories
};
```

#### 2. Search and Filter Components

**SearchBar Component:**
```typescript
interface SearchBarProps {
  value: string;
  onChange: (query: string) => void;
  placeholder?: string;
}

const SearchBar: React.FC<SearchBarProps> = (props) => {
  // Real-time search input with debouncing
};
```

**FilterPanel Component:**
```typescript
interface FilterPanelProps {
  filters: FilterCriteria;
  onFilterChange: (filters: FilterCriteria) => void;
  onClearFilters: () => void;
}

const FilterPanel: React.FC<FilterPanelProps> = (props) => {
  // Multi-field filter controls
};
```

#### 3. Entry Management Components

**EntryEditor Component:**
```typescript
interface EntryEditorProps {
  entry?: VocabEntry;
  onSave: (entry: VocabEntry) => void;
  onCancel: () => void;
}

const EntryEditor: React.FC<EntryEditorProps> = (props) => {
  // Form for creating/editing vocabulary entries
};
```

#### 4. API Client

**VocabularyAPI:**
```typescript
class VocabularyAPI {
  async getEntries(filters?: FilterCriteria): Promise<VocabEntry[]>;
  async createEntry(entry: VocabEntry): Promise<VocabEntry>;
  async updateEntry(id: number, updates: Partial<VocabEntry>): Promise<VocabEntry>;
  async deleteEntry(id: number): Promise<void>;
  async searchEntries(query: string): Promise<VocabEntry[]>;
  async uploadCSV(file: File): Promise<ImportResult>;
  async exportCSV(entryIds?: number[]): Promise<Blob>;
}

class AuthAPI {
  async login(username: string, password: string, remember: boolean): Promise<User>;
  async logout(): Promise<void>;
  async validateSession(): Promise<User>;
}
```

## Data Models

### Database Schema

**users table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**vocab_entries table:**
```sql
CREATE TABLE vocab_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word VARCHAR(100) NOT NULL,
    meaning TEXT NOT NULL,
    synonym VARCHAR(255),
    pronunciation VARCHAR(100),
    example TEXT,
    category_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
    UNIQUE(user_id, word)
);

CREATE INDEX idx_vocab_user ON vocab_entries(user_id);
CREATE INDEX idx_vocab_word ON vocab_entries(word);
CREATE INDEX idx_vocab_category ON vocab_entries(category_id);
```

**categories table:**
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(user_id, name)
);
```

**sessions table:**
```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_session_token ON sessions(token);
CREATE INDEX idx_session_expires ON sessions(expires_at);
```

### Domain Models

**VocabEntry:**
```python
@dataclass
class VocabEntry:
    id: Optional[int]
    user_id: int
    word: str
    meaning: str
    synonym: Optional[str] = None
    pronunciation: Optional[str] = None
    example: Optional[str] = None
    category_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def validate(self) -> list[str]:
        """Validate entry fields and return list of errors"""
        errors = []
        if not self.word or not self.word.strip():
            errors.append("Word field is required")
        if len(self.word) > 100:
            errors.append("Word exceeds 100 characters")
        if not self.meaning or not self.meaning.strip():
            errors.append("Meaning field is required")
        return errors
```

**User:**
```python
@dataclass
class User:
    id: Optional[int]
    username: str
    password_hash: str
    created_at: Optional[datetime] = None
```

**Category:**
```python
@dataclass
class Category:
    id: Optional[int]
    user_id: int
    name: str
    created_at: Optional[datetime] = None
```

**ParseResult:**
```python
@dataclass
class ParseResult:
    entries: list[VocabEntry]
    errors: list[str]
    warnings: list[str]
    total_rows: int
    successful_rows: int
```

**ImportResult:**
```python
@dataclass
class ImportResult:
    imported_count: int
    skipped_count: int
    error_count: int
    errors: list[str]
```

### TypeScript Models

```typescript
interface VocabEntry {
  id?: number;
  userId: number;
  word: string;
  meaning: string;
  synonym?: string;
  pronunciation?: string;
  example?: string;
  categoryId?: number;
  createdAt?: string;
  updatedAt?: string;
}

interface User {
  id: number;
  username: string;
  createdAt: string;
}

interface Category {
  id: number;
  userId: number;
  name: string;
  createdAt: string;
}

interface FilterCriteria {
  word?: string;
  meaning?: string;
  synonym?: string;
  categoryId?: number;
}

interface ImportResult {
  importedCount: number;
  skippedCount: number;
  errorCount: number;
  errors: string[];
}
```

## API Endpoints

### Authentication Endpoints

**POST /api/auth/login**
- Request: `{ username: string, password: string, remember: boolean }`
- Response: `{ user: User, token: string }`
- Status: 200 OK, 401 Unauthorized

**POST /api/auth/logout**
- Request: `{ token: string }`
- Response: `{ success: boolean }`
- Status: 200 OK

**GET /api/auth/validate**
- Headers: `Authorization: Bearer <token>`
- Response: `{ user: User }`
- Status: 200 OK, 401 Unauthorized

### Vocabulary Endpoints

**GET /api/vocab**
- Headers: `Authorization: Bearer <token>`
- Query: `?search=<query>&category=<id>&sort=<field>&order=<asc|desc>`
- Response: `{ entries: VocabEntry[] }`
- Status: 200 OK, 401 Unauthorized

**POST /api/vocab**
- Headers: `Authorization: Bearer <token>`
- Request: `{ entry: VocabEntry }`
- Response: `{ entry: VocabEntry }`
- Status: 201 Created, 400 Bad Request, 401 Unauthorized

**PUT /api/vocab/:id**
- Headers: `Authorization: Bearer <token>`
- Request: `{ updates: Partial<VocabEntry> }`
- Response: `{ entry: VocabEntry }`
- Status: 200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found

**DELETE /api/vocab/:id**
- Headers: `Authorization: Bearer <token>`
- Response: `{ success: boolean }`
- Status: 200 OK, 401 Unauthorized, 404 Not Found

### CSV Endpoints

**POST /api/csv/upload**
- Headers: `Authorization: Bearer <token>`, `Content-Type: multipart/form-data`
- Request: Form data with `file` field
- Response: `{ result: ImportResult }`
- Status: 200 OK, 400 Bad Request, 401 Unauthorized

**GET /api/csv/export**
- Headers: `Authorization: Bearer <token>`
- Query: `?ids=<comma-separated-ids>` (optional, exports all if omitted)
- Response: CSV file download
- Status: 200 OK, 401 Unauthorized

### Category Endpoints

**GET /api/categories**
- Headers: `Authorization: Bearer <token>`
- Response: `{ categories: Category[] }`
- Status: 200 OK, 401 Unauthorized

**POST /api/categories**
- Headers: `Authorization: Bearer <token>`
- Request: `{ name: string }`
- Response: `{ category: Category }`
- Status: 201 Created, 400 Bad Request, 401 Unauthorized

**PUT /api/categories/:id**
- Headers: `Authorization: Bearer <token>`
- Request: `{ name: string }`
- Response: `{ category: Category }`
- Status: 200 OK, 400 Bad Request, 401 Unauthorized, 404 Not Found

**DELETE /api/categories/:id**
- Headers: `Authorization: Bearer <token>`
- Response: `{ success: boolean }`
- Status: 200 OK, 401 Unauthorized, 404 Not Found


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property Reflection

After analyzing all acceptance criteria, I identified several opportunities to consolidate redundant properties:

- **CSV Parsing Properties (1.1, 1.2, 12.1, 12.2, 12.3, 12.4, 12.5)**: These can be consolidated into comprehensive parsing properties that cover valid inputs, delimiter detection, encoding support, and error handling
- **Data Persistence (2.1, 2.5)**: Combined into a single round-trip property
- **Search and Filter (3.2, 5.3)**: Both test filtering behavior and can be unified
- **CRUD Operations (7.1, 7.2, 7.3)**: Each operation is distinct and should remain separate
- **CSV Export (8.1, 8.2, 8.3)**: Combined into a round-trip property for CSV import/export
- **Validation Properties (7.4, 7.5, 11.1, 11.2)**: Consolidated into comprehensive validation properties
- **Authentication Properties (9.1, 9.2, 9.3, 9.4)**: Each tests distinct auth behavior and should remain separate
- **Session Management (10.1, 10.2, 10.3, 10.4, 10.5)**: Each tests distinct session behavior

### CSV Parsing and Import Properties

**Property 1: CSV Parsing Completeness**

*For any* valid CSV file with the expected structure (word, meaning, synonym, pronunciation, example), parsing the file should extract all rows as vocabulary entries with correct field mapping.

**Validates: Requirements 1.1**

**Property 2: CSV Parsing with Missing Columns**

*For any* CSV file with a subset of expected columns, parsing should create vocabulary entries with available fields populated and optional fields set to null.

**Validates: Requirements 1.2**

**Property 3: CSV Parsing Error Handling**

*For any* malformed CSV file (invalid encoding, corrupted structure), the parser should reject the file and return a descriptive error message without creating partial entries.

**Validates: Requirements 1.3**

**Property 4: CSV Import Count Accuracy**

*For any* successfully parsed CSV file, the import result count should equal the number of valid entries extracted from the file.

**Validates: Requirements 1.4**

**Property 5: CSV Duplicate Handling**

*For any* CSV file containing duplicate words, the system should either merge the entries or provide a mechanism to resolve conflicts, ensuring no data loss.

**Validates: Requirements 1.5**

**Property 6: CSV Delimiter Detection**

*For any* CSV file using comma, semicolon, or tab delimiters, the parser should correctly detect the delimiter and parse all fields accurately.

**Validates: Requirements 12.1**

**Property 7: CSV Quoted Field Parsing**

*For any* CSV file with quoted fields containing embedded delimiters or newlines, the parser should correctly extract the field content without splitting on embedded delimiters.

**Validates: Requirements 12.2**

**Property 8: CSV Inconsistent Column Handling**

*For any* CSV file with rows having different column counts, the parser should handle missing values gracefully by filling with null or default values.

**Validates: Requirements 12.3**

**Property 9: CSV Encoding Support**

*For any* CSV file encoded in UTF-8, UTF-16, or ASCII, the parser should correctly detect the encoding and parse all characters without corruption.

**Validates: Requirements 12.4**

**Property 10: CSV Header Detection**

*For any* CSV file, if a header row is present, the parser should use it for column mapping; otherwise, it should use default column order (word, meaning, synonym, pronunciation, example).

**Validates: Requirements 12.5**

### Data Persistence Properties

**Property 11: Vocabulary Entry Round-Trip**

*For any* valid vocabulary entry, storing it to the database and then retrieving it should return an equivalent entry with all fields (word, meaning, synonym, pronunciation, example) preserved exactly.

**Validates: Requirements 2.1, 2.5**

**Property 12: User Data Isolation**

*For any* two different users, vocabulary entries created by one user should not be retrievable by the other user, ensuring complete data isolation.

**Validates: Requirements 2.2**

### Search and Filter Properties

**Property 13: Search Across All Fields**

*For any* search query and vocabulary collection, the search results should include all and only those entries where the query appears as a substring in any field (word, meaning, synonym, pronunciation, example).

**Validates: Requirements 3.2**

**Property 14: Multi-Field Filtering**

*For any* set of filter criteria, the filtered results should include all and only those entries that match all active filter conditions.

**Validates: Requirements 5.3**

**Property 15: Filter Clearing Restoration**

*For any* vocabulary collection with active filters, clearing all filters should restore the complete unfiltered collection.

**Validates: Requirements 5.5**

### Visualization Properties

**Property 16: Card View Completeness**

*For any* vocabulary entry displayed in card view, the rendered card should contain all non-null fields (word, meaning, synonym, pronunciation, example).

**Validates: Requirements 3.1**

**Property 17: Search Highlighting**

*For any* search query and matching vocabulary entry, the rendered card should contain highlighting markup around all occurrences of the query text.

**Validates: Requirements 3.3**

**Property 18: Word Cloud Completeness**

*For any* vocabulary collection, the generated word cloud data structure should include all entries from the collection.

**Validates: Requirements 4.1**

**Property 19: Word Cloud Sizing Correlation**

*For any* vocabulary collection and chosen sizing metric (frequency, length, importance), word sizes in the cloud should correlate monotonically with the metric values.

**Validates: Requirements 4.2**

**Property 20: Word Cloud Click Mapping**

*For any* word in the word cloud, clicking it should return the complete vocabulary entry corresponding to that word.

**Validates: Requirements 4.3**

**Property 21: Word Cloud Reactivity**

*For any* vocabulary collection, after adding or removing entries, regenerating the word cloud should reflect the current collection state.

**Validates: Requirements 4.5**

**Property 22: List View Completeness**

*For any* vocabulary collection, the list view should display all entries with all fields visible in the table.

**Validates: Requirements 5.1**

**Property 23: List Sorting Correctness**

*For any* vocabulary collection and sort column, sorting should produce a list ordered correctly by that column in the specified direction (ascending or descending).

**Validates: Requirements 5.2**

### Category Management Properties

**Property 24: Category Assignment Persistence**

*For any* vocabulary entry and category, assigning the category to the entry should persist the association such that retrieving the entry returns the correct category ID.

**Validates: Requirements 6.1**

**Property 25: Categorized Grouping**

*For any* vocabulary collection with categories, the categorized view should group entries such that all entries with the same category ID appear in the same group.

**Validates: Requirements 6.2**

**Property 26: Category CRUD Operations**

*For any* category, creating, renaming, or deleting it should correctly update the database and be reflected in subsequent queries.

**Validates: Requirements 6.3**

**Property 27: Uncategorized Default Grouping**

*For any* vocabulary entry without a category assignment, it should appear in the "Uncategorized" group in categorized view.

**Validates: Requirements 6.4**

**Property 28: Category Expansion Completeness**

*For any* category, expanding it should display all and only those vocabulary entries with that category ID.

**Validates: Requirements 6.5**

### CRUD Operation Properties

**Property 29: Vocabulary Entry Creation**

*For any* valid vocabulary entry (non-empty word and meaning), creating it should add it to the user's collection such that it appears in subsequent queries.

**Validates: Requirements 7.1**

**Property 30: Vocabulary Entry Update**

*For any* existing vocabulary entry and valid field updates, updating the entry should persist the changes such that subsequent retrieval returns the updated values.

**Validates: Requirements 7.2**

**Property 31: Vocabulary Entry Deletion**

*For any* existing vocabulary entry, deleting it should remove it from the database such that subsequent queries do not return it.

**Validates: Requirements 7.3**

### Validation Properties

**Property 32: Empty Field Rejection**

*For any* vocabulary entry where the word or meaning field contains only whitespace characters, the system should reject the entry and return a validation error.

**Validates: Requirements 7.4, 7.5**

**Property 33: Field Length Validation**

*For any* vocabulary entry where the word field exceeds 100 characters, the system should reject the entry and return a validation error.

**Validates: Requirements 11.2**

**Property 34: Input Validation Completeness**

*For any* data input (import or manual entry), the system should validate all fields against defined constraints before persisting, rejecting invalid data with descriptive errors.

**Validates: Requirements 11.1**

**Property 35: Input Sanitization**

*For any* user input containing potentially malicious content (SQL injection patterns, XSS scripts), the system should sanitize or escape the input to prevent security vulnerabilities.

**Validates: Requirements 11.3**

**Property 36: Unique Word Constraint**

*For any* user, attempting to create two vocabulary entries with the same word should be rejected, enforcing uniqueness per user.

**Validates: Requirements 11.5**

### CSV Export Properties

**Property 37: CSV Export Round-Trip**

*For any* vocabulary collection, exporting to CSV and then importing the exported CSV should produce an equivalent collection with all entries and fields preserved.

**Validates: Requirements 8.1, 8.2, 8.3**

**Property 38: CSV Export Filename Format**

*For any* CSV export operation, the generated filename should include the current date in a consistent format (e.g., vocab_export_YYYY-MM-DD.csv).

**Validates: Requirements 8.5**

### Authentication Properties

**Property 39: Valid Credential Authentication**

*For any* registered user with correct username and password, authentication should succeed and create a valid session token.

**Validates: Requirements 9.1**

**Property 40: Invalid Credential Rejection**

*For any* authentication attempt with incorrect username or password, the system should reject the attempt and return an error without creating a session.

**Validates: Requirements 9.2**

**Property 41: Unauthenticated Access Prevention**

*For any* request to protected endpoints without a valid session token, the system should reject the request with a 401 Unauthorized status.

**Validates: Requirements 9.3**

**Property 42: Logout Session Termination**

*For any* valid session, logging out should invalidate the session token such that subsequent requests with that token are rejected.

**Validates: Requirements 9.4**

**Property 43: Password Hashing**

*For any* user password, the stored value in the database should be a bcrypt hash, not the plaintext password.

**Validates: Requirements 9.5**

### Session Management Properties

**Property 44: Session Duration**

*For any* authenticated session, the session should remain valid for 24 hours from the last activity timestamp.

**Validates: Requirements 10.1**

**Property 45: Remember Me Persistence**

*For any* authentication with "remember me" enabled, the session expiration should be extended beyond the default 24 hours (e.g., 30 days).

**Validates: Requirements 10.2**

**Property 46: Expired Session Rejection**

*For any* session token with an expiration timestamp in the past, requests using that token should be rejected with a 401 Unauthorized status.

**Validates: Requirements 10.3**

**Property 47: Session Token Validation**

*For any* request to a protected endpoint, the system should validate the session token and reject invalid or missing tokens.

**Validates: Requirements 10.4**

**Property 48: Session Activity Extension**

*For any* valid session, making a request should update the expiration timestamp to extend the session by the configured duration.

**Validates: Requirements 10.5**

### Transaction Properties

**Property 49: Transaction Rollback on Failure**

*For any* database operation that fails mid-transaction, the system should rollback all changes to maintain database consistency.

**Validates: Requirements 11.4**

## Error Handling

### Error Categories

**1. Validation Errors (400 Bad Request)**
- Empty or whitespace-only required fields
- Field length violations (word > 100 characters)
- Invalid data types or formats
- Duplicate word entries for the same user

**2. Authentication Errors (401 Unauthorized)**
- Invalid credentials
- Missing session token
- Expired session token
- Invalid session token

**3. Authorization Errors (403 Forbidden)**
- Attempting to access another user's vocabulary entries
- Attempting to modify another user's categories

**4. Not Found Errors (404 Not Found)**
- Vocabulary entry ID does not exist
- Category ID does not exist
- User ID does not exist

**5. Server Errors (500 Internal Server Error)**
- Database connection failures
- Unexpected exceptions during processing
- File system errors during CSV operations

### Error Response Format

All API errors follow a consistent JSON format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable error message",
    "details": [
      "Specific validation error 1",
      "Specific validation error 2"
    ],
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Error Handling Strategies

**CSV Parsing Errors:**
- Detect encoding issues early and provide specific error messages
- Collect all parsing errors and return them together (don't fail on first error)
- Provide line numbers for malformed rows
- Suggest corrections when possible (e.g., "Expected 5 columns, found 3 on line 42")

**Database Errors:**
- Wrap all database operations in try-catch blocks
- Use transactions for multi-step operations
- Rollback on any failure to maintain consistency
- Log detailed errors server-side, return generic messages to client
- Implement retry logic for transient failures

**Authentication Errors:**
- Use generic error messages to prevent username enumeration ("Invalid credentials" not "User not found")
- Rate limit login attempts to prevent brute force attacks
- Log failed authentication attempts for security monitoring

**Validation Errors:**
- Validate all inputs before processing
- Return all validation errors at once (not just the first one)
- Provide field-specific error messages
- Sanitize error messages to prevent information leakage

## Testing Strategy

### Dual Testing Approach

The testing strategy employs both unit tests and property-based tests as complementary approaches:

**Unit Tests:**
- Specific examples demonstrating correct behavior
- Edge cases (empty collections, single-item collections, boundary values)
- Error conditions and exception handling
- Integration points between components
- UI component rendering with specific props

**Property-Based Tests:**
- Universal properties that hold for all inputs
- Comprehensive input coverage through randomization
- Minimum 100 iterations per property test
- Each test references its design document property

Both approaches are necessary for comprehensive coverage. Unit tests catch concrete bugs and document expected behavior through examples, while property tests verify general correctness across a wide input space.

### Property-Based Testing Configuration

**Library Selection:**
- **Backend (Python)**: Hypothesis - mature, well-integrated with pytest
- **Frontend (TypeScript)**: fast-check - excellent TypeScript support, integrates with Jest

**Test Configuration:**
- Minimum 100 iterations per property test (configurable higher for critical properties)
- Deterministic seed for reproducibility
- Shrinking enabled to find minimal failing examples
- Timeout of 30 seconds per property test

**Test Tagging:**
Each property-based test must include a comment tag referencing the design property:

```python
# Feature: vocabulary-visualization-app, Property 11: Vocabulary Entry Round-Trip
@given(vocab_entry())
def test_vocab_entry_round_trip(entry):
    # Test implementation
```

```typescript
// Feature: vocabulary-visualization-app, Property 13: Search Across All Fields
fc.assert(
  fc.property(fc.array(vocabEntry()), fc.string(), (entries, query) => {
    // Test implementation
  }),
  { numRuns: 100 }
);
```

### Test Organization

**Backend Tests:**
```
tests/
├── unit/
│   ├── test_csv_parser.py
│   ├── test_vocabulary_service.py
│   ├── test_auth_service.py
│   └── test_dao.py
├── property/
│   ├── test_csv_properties.py
│   ├── test_persistence_properties.py
│   ├── test_search_properties.py
│   ├── test_auth_properties.py
│   └── test_validation_properties.py
└── integration/
    ├── test_api_endpoints.py
    └── test_database_integration.py
```

**Frontend Tests:**
```
src/
├── components/
│   ├── CardView/
│   │   ├── CardView.tsx
│   │   ├── CardView.test.tsx (unit)
│   │   └── CardView.properties.test.tsx (property)
│   ├── WordCloudView/
│   │   ├── WordCloudView.tsx
│   │   └── WordCloudView.test.tsx
│   └── ListView/
│       ├── ListView.tsx
│       └── ListView.test.tsx
└── api/
    ├── VocabularyAPI.ts
    └── VocabularyAPI.test.ts
```

### Test Data Generators

**Hypothesis Strategies (Python):**
```python
from hypothesis import strategies as st

@st.composite
def vocab_entry(draw):
    return VocabEntry(
        id=None,
        user_id=draw(st.integers(min_value=1, max_value=1000)),
        word=draw(st.text(min_size=1, max_size=100, alphabet=st.characters(blacklist_categories=['Cs']))),
        meaning=draw(st.text(min_size=1, max_size=500)),
        synonym=draw(st.one_of(st.none(), st.text(max_size=255))),
        pronunciation=draw(st.one_of(st.none(), st.text(max_size=100))),
        example=draw(st.one_of(st.none(), st.text(max_size=500))),
        category_id=draw(st.one_of(st.none(), st.integers(min_value=1, max_value=100)))
    )

@st.composite
def csv_file(draw):
    entries = draw(st.lists(vocab_entry(), min_size=0, max_size=100))
    delimiter = draw(st.sampled_from([',', ';', '\t']))
    has_header = draw(st.booleans())
    encoding = draw(st.sampled_from(['utf-8', 'utf-16', 'ascii']))
    return generate_csv(entries, delimiter, has_header, encoding)
```

**fast-check Arbitraries (TypeScript):**
```typescript
import * as fc from 'fast-check';

const vocabEntry = (): fc.Arbitrary<VocabEntry> =>
  fc.record({
    id: fc.option(fc.nat(), { nil: undefined }),
    userId: fc.nat({ max: 1000 }),
    word: fc.string({ minLength: 1, maxLength: 100 }),
    meaning: fc.string({ minLength: 1, maxLength: 500 }),
    synonym: fc.option(fc.string({ maxLength: 255 }), { nil: undefined }),
    pronunciation: fc.option(fc.string({ maxLength: 100 }), { nil: undefined }),
    example: fc.option(fc.string({ maxLength: 500 }), { nil: undefined }),
    categoryId: fc.option(fc.nat({ max: 100 }), { nil: undefined }),
  });

const searchQuery = (): fc.Arbitrary<string> =>
  fc.string({ minLength: 0, maxLength: 50 });
```

### Critical Test Scenarios

**CSV Parsing:**
- Valid CSV with all columns
- CSV with missing optional columns
- CSV with various delimiters (comma, semicolon, tab)
- CSV with quoted fields containing delimiters
- CSV with different encodings (UTF-8, UTF-16, ASCII)
- CSV with special characters (quotes, newlines, unicode)
- Malformed CSV (inconsistent columns, invalid encoding)
- Empty CSV file
- Very large CSV files (1000+ entries)

**Search and Filter:**
- Search matching in different fields
- Search with special characters
- Search with unicode characters
- Case-insensitive search
- Empty search query (should return all)
- Multiple simultaneous filters
- Filter combinations (AND logic)

**Authentication and Sessions:**
- Valid login credentials
- Invalid username
- Invalid password
- Session expiration
- Session extension on activity
- Remember me functionality
- Concurrent sessions
- Session token validation

**Data Integrity:**
- Concurrent updates to same entry
- Transaction rollback on failure
- Unique constraint enforcement
- Foreign key constraint enforcement
- Cascade deletion (user deletion removes entries)

### Continuous Integration

**Test Execution:**
- Run all unit tests on every commit
- Run property tests on every pull request
- Run integration tests before deployment
- Generate coverage reports (target: 80%+ coverage)

**Performance Benchmarks:**
- Query performance for 1000+ entries
- CSV parsing performance for large files
- Search response time
- API endpoint response times

