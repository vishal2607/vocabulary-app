# How Your Vocabulary App Works - Complete Guide

This guide explains how your app works from start to finish, in plain language for a semi-technical person.

---

## Table of Contents

1. [The Big Picture](#the-big-picture)
2. [What Happens When You Start the App](#what-happens-when-you-start-the-app)
3. [User Registration Flow](#user-registration-flow)
4. [User Login Flow](#user-login-flow)
5. [Adding a Vocabulary Entry](#adding-a-vocabulary-entry)
6. [Searching Vocabulary](#searching-vocabulary)
7. [CSV Import Flow](#csv-import-flow)
8. [How the Database Works](#how-the-database-works)
9. [How the Frontend and Backend Talk](#how-the-frontend-and-backend-talk)
10. [File-by-File Breakdown](#file-by-file-breakdown)

---

## The Big Picture

Your app has **two separate programs** running at the same time:

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR COMPUTER                         │
│                                                          │
│  ┌──────────────────┐         ┌──────────────────┐     │
│  │   FRONTEND       │         │    BACKEND       │     │
│  │   (React)        │◄───────►│    (Flask)       │     │
│  │   Port 5173      │  HTTP   │    Port 5001     │     │
│  │                  │  JSON   │                  │     │
│  │  - Login page    │         │  - API endpoints │     │
│  │  - Dashboard     │         │  - Business logic│     │
│  │  - Forms         │         │  - Database      │     │
│  └──────────────────┘         └──────────────────┘     │
│         ▲                              │                │
│         │                              ▼                │
│    Your Browser                  SQLite Database        │
│  (Chrome/Safari)                 (vocabulary.db)        │
└─────────────────────────────────────────────────────────┘
```

**Frontend (React)**: What you see and interact with in the browser
**Backend (Flask)**: The server that handles data, security, and database operations

They communicate using **HTTP requests** with **JSON data** (like sending letters back and forth).

---

## What Happens When You Start the App

### Step 1: Starting the Backend (`python run.py`)


1. **`backend/run.py`** starts
2. It imports the Flask app from `backend/app/app.py`
3. Flask initializes:
   - Loads configuration (database path, CORS settings)
   - Connects to SQLite database (`backend/data/vocabulary.db`)
   - Creates database tables if they don't exist (users, vocab_entries, categories, sessions)
   - Registers API routes (endpoints like `/api/auth/login`, `/api/vocab`, etc.)
4. Flask starts listening on **port 5001**
5. Backend is now ready to receive requests

**What's happening**: Flask is like a restaurant that just opened - the kitchen is ready, the menu is set, and it's waiting for customers (HTTP requests).

### Step 2: Starting the Frontend (`npm run dev`)

1. **Vite** (the dev server) starts
2. It reads `frontend/vite.config.ts` for configuration
3. It compiles your TypeScript/React code into JavaScript
4. It starts a web server on **port 5173**
5. It opens your browser to `http://localhost:5173`
6. Your browser loads:
   - `frontend/index.html` (the main HTML file)
   - `frontend/src/main.tsx` (the JavaScript entry point)
   - All CSS (Tailwind styles)
7. React renders the app:
   - Checks if you're logged in (looks for token in localStorage)
   - Shows login page if not logged in
   - Shows dashboard if logged in

**What's happening**: Vite is like a waiter - it serves your app to the browser and keeps refreshing it when you make changes.

---

## User Registration Flow

Let's trace what happens when you click "Register" with username "john" and password "secret123":

### Frontend Side (Browser)


**File: `frontend/src/pages/Login.tsx`**

1. You type username and password in the form
2. You click "Register" button
3. React calls the `handleRegister` function
4. This function calls `api.auth.register(username, password)`

**File: `frontend/src/api/client.ts`**

5. The API client creates an HTTP POST request:
   ```
   POST http://localhost:5001/api/auth/register
   Body: { "username": "john", "password": "secret123" }
   ```
6. Axios sends this request to the backend

### Backend Side (Server)

**File: `backend/app/routes/auth_routes.py`**

7. Flask receives the request at the `/api/auth/register` endpoint
8. It extracts username and password from the request body
9. It validates: username and password are not empty
10. It calls `auth_service.register_user(username, password)`

**File: `backend/app/services/auth_service.py`**

11. The auth service checks if username already exists (calls `user_dao.find_by_username()`)
12. If username is unique, it hashes the password using bcrypt:
    ```
    "secret123" → "$2b$12$KIXxJ..." (60-character hash)
    ```
13. It calls `user_dao.create_user(username, hashed_password)`

**File: `backend/app/dao/user_dao.py`**

14. The DAO creates a new User object
15. It adds it to the database session
16. It commits the transaction (saves to database)
17. SQLAlchemy executes SQL:
    ```sql
    INSERT INTO users (username, password_hash, created_at)
    VALUES ('john', '$2b$12$KIXxJ...', '2026-02-04 10:30:00');
    ```

**File: `backend/data/vocabulary.db`**

18. SQLite writes the new user to the database file

### Response Back to Frontend

19. The DAO returns the new User object
20. The auth service returns success
21. The route returns JSON response:
    ```json
    {
      "message": "User registered successfully",
      "user": { "id": 1, "username": "john" }
    }
    ```
22. Axios receives the response
23. The Login component shows success message
24. The form switches to the "Login" tab

**Total time**: ~50-100 milliseconds

---

## User Login Flow

When you login with username "john" and password "secret123":


### Frontend

1. You click "Login"
2. `api.auth.login(username, password, rememberMe)` is called
3. HTTP POST request sent:
   ```
   POST http://localhost:5001/api/auth/login
   Body: { "username": "john", "password": "secret123", "remember_me": false }
   ```

### Backend

4. Flask route `/api/auth/login` receives request
5. Calls `auth_service.authenticate(username, password, remember_me)`
6. Auth service:
   - Finds user by username: `user_dao.find_by_username('john')`
   - Gets user from database with hashed password
   - Verifies password using bcrypt:
     ```python
     bcrypt.checkpw("secret123", stored_hash)  # Returns True if match
     ```
   - If password matches, creates a session token:
     ```python
     token = secrets.token_urlsafe(32)  # Random string like "xK9mP2..."
     ```
   - Calculates expiration time (24 hours, or 30 days if remember_me)
   - Saves session to database:
     ```sql
     INSERT INTO sessions (user_id, token, expires_at)
     VALUES (1, 'xK9mP2...', '2026-02-05 10:30:00');
     ```
7. Returns response:
   ```json
   {
     "message": "Login successful",
     "token": "xK9mP2...",
     "user": { "id": 1, "username": "john" }
   }
   ```

### Frontend Receives Response

8. Axios receives the response
9. `AuthContext` saves the token:
   ```javascript
   localStorage.setItem('auth_token', 'xK9mP2...')
   ```
10. Sets user state in React context
11. React Router redirects to `/dashboard`
12. Dashboard page loads

**Key concept**: The token is like a movie ticket - it proves you paid (logged in) and lets you enter (access protected pages).

---

## Adding a Vocabulary Entry

When you add the word "serendipity":


### Frontend

**File: `frontend/src/pages/Dashboard.tsx`**

1. You click "+ Add Entry" button
2. A form appears (EntryForm component)
3. You fill in:
   - Word: "serendipity"
   - Meaning: "finding something good without looking for it"
   - Synonym: "luck"
   - Pronunciation: "/ˌserənˈdɪpɪti/"
   - Example: "Meeting you was pure serendipity"
4. You click "Add Entry"
5. Dashboard calls `api.vocab.create(entryData)`

**File: `frontend/src/api/client.ts`**

6. API client sends request:
   ```
   POST http://localhost:5001/api/vocab
   Headers: { Authorization: "Bearer xK9mP2..." }
   Body: {
     "word": "serendipity",
     "meaning": "finding something good without looking for it",
     "synonym": "luck",
     "pronunciation": "/ˌserənˈdɪpɪti/",
     "example": "Meeting you was pure serendipity"
   }
   ```

### Backend

**File: `backend/app/routes/vocab_routes.py`**

7. Flask receives request at `/api/vocab`
8. **Authentication middleware** checks the token:
   - Extracts token from Authorization header
   - Calls `auth_service.validate_session(token)`
   - Looks up session in database
   - Checks if session is expired
   - If valid, gets user_id from session
   - If invalid, returns 401 Unauthorized
9. Extracts vocabulary data from request body
10. Calls `vocabulary_service.create_entry(user_id, entry_data)`

**File: `backend/app/services/vocabulary_service.py`**

11. Vocabulary service validates the data:
    - Checks word is not empty
    - Checks meaning is not empty
    - Checks word length ≤ 100 characters
    - Sanitizes inputs (removes dangerous characters)
12. Checks if word already exists for this user:
    ```python
    existing = vocabulary_dao.find_by_word(user_id, "serendipity")
    ```
13. If unique, calls `vocabulary_dao.insert(user_id, entry_data)`

**File: `backend/app/dao/vocabulary_dao.py`**

14. DAO creates a VocabEntry object:
    ```python
    entry = VocabEntry(
        user_id=1,
        word="serendipity",
        meaning="finding something good without looking for it",
        synonym="luck",
        pronunciation="/ˌserənˈdɪpɪti/",
        example="Meeting you was pure serendipity",
        created_at=datetime.now()
    )
    ```
15. Adds to database session and commits
16. SQLAlchemy executes:
    ```sql
    INSERT INTO vocab_entries 
    (user_id, word, meaning, synonym, pronunciation, example, created_at)
    VALUES (1, 'serendipity', 'finding something...', 'luck', 
            '/ˌserənˈdɪpɪti/', 'Meeting you...', '2026-02-04 10:35:00');
    ```

### Response

17. Returns the new entry with its ID:
    ```json
    {
      "id": 42,
      "word": "serendipity",
      "meaning": "finding something good without looking for it",
      "synonym": "luck",
      "pronunciation": "/ˌserənˈdɪpɪti/",
      "example": "Meeting you was pure serendipity",
      "created_at": "2026-02-04T10:35:00Z"
    }
    ```
18. Frontend receives response
19. Dashboard adds the new entry to the list
20. React re-renders the VocabList component
21. You see the new word appear on screen

**Total time**: ~20-50 milliseconds

---

## Searching Vocabulary

When you type "seren" in the search box:


### Frontend

**File: `frontend/src/components/SearchBar.tsx`**

1. You type "s" → SearchBar updates state
2. You type "e" → SearchBar updates state
3. You type "r" → SearchBar updates state
4. You type "e" → SearchBar updates state
5. You type "n" → SearchBar updates state
6. **Debounce timer**: Wait 300ms to see if you keep typing
7. 300ms passes with no more typing
8. SearchBar calls `onSearch("seren")`

**File: `frontend/src/pages/Dashboard.tsx`**

9. Dashboard receives search query
10. Calls `api.vocab.getAll({ search: "seren" })`

**File: `frontend/src/api/client.ts`**

11. API client sends request:
    ```
    GET http://localhost:5001/api/vocab?search=seren
    Headers: { Authorization: "Bearer xK9mP2..." }
    ```

### Backend

**File: `backend/app/routes/vocab_routes.py`**

12. Flask receives request
13. Validates session token (checks you're logged in)
14. Extracts search query: `search = "seren"`
15. Calls `vocabulary_service.search_entries(user_id, "seren")`

**File: `backend/app/services/vocabulary_service.py`**

16. Service calls `vocabulary_dao.search(user_id, "seren")`

**File: `backend/app/dao/vocabulary_dao.py`**

17. DAO builds SQL query with LIKE operator:
    ```sql
    SELECT * FROM vocab_entries
    WHERE user_id = 1
    AND (
      word LIKE '%seren%' OR
      meaning LIKE '%seren%' OR
      synonym LIKE '%seren%' OR
      pronunciation LIKE '%seren%' OR
      example LIKE '%seren%'
    )
    ORDER BY word ASC;
    ```
18. SQLite searches through all your vocabulary entries
19. Finds matches: "serendipity" (matches in word field)

### Response

20. Returns matching entries:
    ```json
    [
      {
        "id": 42,
        "word": "serendipity",
        "meaning": "finding something good without looking for it",
        ...
      }
    ]
    ```
21. Frontend receives results
22. Dashboard updates the vocabulary list
23. VocabList component re-renders
24. You see only matching entries

**Why debounce?** Without it, typing "seren" would send 5 requests (one per letter). With debounce, it sends only 1 request after you stop typing.

---

## CSV Import Flow

When you upload a CSV file with 100 vocabulary words:


### Frontend

**File: `frontend/src/pages/Dashboard.tsx`**

1. You click "Import CSV" button
2. File picker opens
3. You select `my_vocabulary.csv`
4. Dashboard reads the file as binary data
5. Calls `api.csv.upload(file)`

**File: `frontend/src/api/client.ts`**

6. API client creates a FormData object (for file upload):
   ```javascript
   const formData = new FormData()
   formData.append('file', file)
   ```
7. Sends multipart/form-data request:
   ```
   POST http://localhost:5001/api/csv/upload
   Headers: { 
     Authorization: "Bearer xK9mP2...",
     Content-Type: "multipart/form-data"
   }
   Body: [binary file data]
   ```

### Backend

**File: `backend/app/routes/csv_routes.py`**

8. Flask receives the file upload
9. Validates session token
10. Extracts the uploaded file
11. Saves it temporarily to disk
12. Calls `vocabulary_service.import_from_csv(user_id, file_path)`

**File: `backend/app/services/vocabulary_service.py`**

13. Service calls `csv_parser.parse_csv(file_path)`

**File: `backend/app/services/csv_parser.py`**

14. CSV parser opens the file
15. **Detects encoding**: Tries UTF-8, UTF-16, ASCII
    ```python
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        encoding = chardet.detect(raw_data)['encoding']  # "utf-8"
    ```
16. **Detects delimiter**: Checks for comma, semicolon, tab
    ```python
    sample = file.read(1024)
    sniffer = csv.Sniffer()
    delimiter = sniffer.sniff(sample).delimiter  # ","
    ```
17. **Reads CSV with pandas**:
    ```python
    df = pd.read_csv(file_path, encoding='utf-8', delimiter=',')
    ```
18. **Validates columns**: Checks for required columns (word, meaning)
19. **Processes each row**:
    ```python
    for index, row in df.iterrows():
        entry = {
            'word': row['word'],
            'meaning': row['meaning'],
            'synonym': row.get('synonym', ''),
            'pronunciation': row.get('pronunciation', ''),
            'example': row.get('example', '')
        }
        entries.append(entry)
    ```
20. Returns list of 100 parsed entries

**Back to vocabulary_service.py**

21. For each entry:
    - Validates data (word not empty, length checks)
    - Checks if word already exists
    - If duplicate, decides to skip or update
    - Calls `vocabulary_dao.insert(user_id, entry)`
22. Tracks results:
    ```python
    results = {
        'total': 100,
        'imported': 95,
        'skipped': 5,  # duplicates
        'errors': []
    }
    ```

### Database Operations

23. SQLAlchemy executes 95 INSERT statements:
    ```sql
    INSERT INTO vocab_entries (user_id, word, meaning, ...)
    VALUES (1, 'ephemeral', 'lasting a short time', ...);
    
    INSERT INTO vocab_entries (user_id, word, meaning, ...)
    VALUES (1, 'ubiquitous', 'present everywhere', ...);
    
    ... (93 more)
    ```
24. All wrapped in a transaction (all succeed or all fail)

### Response

25. Returns import results:
    ```json
    {
      "message": "Import completed",
      "total": 100,
      "imported": 95,
      "skipped": 5,
      "errors": []
    }
    ```
26. Frontend shows success message: "Imported 95 entries, skipped 5 duplicates"
27. Dashboard refreshes the vocabulary list
28. You see all 95 new words

**Total time**: ~500ms - 2 seconds (depending on file size)

---

## How the Database Works


### SQLite Database Structure

Your database file (`backend/data/vocabulary.db`) contains 4 tables:

```
┌─────────────────────────────────────────────────────────┐
│                    vocabulary.db                         │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  TABLE: users                                            │
│  ┌────┬──────────┬───────────────────┬─────────────┐   │
│  │ id │ username │ password_hash     │ created_at  │   │
│  ├────┼──────────┼───────────────────┼─────────────┤   │
│  │ 1  │ john     │ $2b$12$KIXxJ...  │ 2026-02-04  │   │
│  │ 2  │ mary     │ $2b$12$9Pqrs...  │ 2026-02-04  │   │
│  └────┴──────────┴───────────────────┴─────────────┘   │
│                                                          │
│  TABLE: sessions                                         │
│  ┌────┬─────────┬──────────────┬─────────────┐         │
│  │ id │ user_id │ token        │ expires_at  │         │
│  ├────┼─────────┼──────────────┼─────────────┤         │
│  │ 1  │ 1       │ xK9mP2...    │ 2026-02-05  │         │
│  │ 2  │ 2       │ aB3nQ7...    │ 2026-02-05  │         │
│  └────┴─────────┴──────────────┴─────────────┘         │
│                                                          │
│  TABLE: vocab_entries                                    │
│  ┌────┬─────────┬──────────────┬─────────────┬───┐     │
│  │ id │ user_id │ word         │ meaning     │...│     │
│  ├────┼─────────┼──────────────┼─────────────┼───┤     │
│  │ 1  │ 1       │ serendipity  │ finding...  │...│     │
│  │ 2  │ 1       │ ephemeral    │ lasting...  │...│     │
│  │ 3  │ 2       │ ubiquitous   │ present...  │...│     │
│  └────┴─────────┴──────────────┴─────────────┴───┘     │
│                                                          │
│  TABLE: categories                                       │
│  ┌────┬─────────┬──────────┬─────────────┐             │
│  │ id │ user_id │ name     │ created_at  │             │
│  ├────┼─────────┼──────────┼─────────────┤             │
│  │ 1  │ 1       │ Academic │ 2026-02-04  │             │
│  │ 2  │ 1       │ Casual   │ 2026-02-04  │             │
│  └────┴─────────┴──────────┴─────────────┘             │
└─────────────────────────────────────────────────────────┘
```

### How SQLAlchemy Works

**SQLAlchemy** is an ORM (Object-Relational Mapper) - it translates between Python objects and database tables.

**Without SQLAlchemy** (raw SQL):
```python
cursor.execute("INSERT INTO vocab_entries (word, meaning) VALUES (?, ?)", 
               ("serendipity", "finding something good"))
```

**With SQLAlchemy** (Python objects):
```python
entry = VocabEntry(word="serendipity", meaning="finding something good")
db.session.add(entry)
db.session.commit()
```

### Database Models

**File: `backend/app/models/vocab_entry.py`**

```python
class VocabEntry(Base):
    __tablename__ = 'vocab_entries'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    word = Column(String(100), nullable=False)
    meaning = Column(Text, nullable=False)
    synonym = Column(String(200))
    pronunciation = Column(String(100))
    example = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
```

This Python class defines:
- Table name: `vocab_entries`
- Columns: id, user_id, word, meaning, etc.
- Data types: Integer, String, Text, DateTime
- Constraints: primary_key, nullable, ForeignKey

When you create a VocabEntry object, SQLAlchemy knows how to save it to the database.

### Relationships

```python
# User has many vocab entries
user.vocab_entries  # Returns list of all entries for this user

# Vocab entry belongs to one user
entry.user  # Returns the User object who owns this entry
```

SQLAlchemy handles the foreign key relationships automatically.

---

## How the Frontend and Backend Talk


### HTTP Request/Response Cycle

Every interaction follows this pattern:

```
FRONTEND                          BACKEND
   │                                 │
   │  1. User clicks button          │
   │                                 │
   │  2. React calls API function    │
   │     api.vocab.create(...)       │
   │                                 │
   │  3. Axios sends HTTP request    │
   │     POST /api/vocab             │
   ├────────────────────────────────>│
   │                                 │
   │                                 │  4. Flask receives request
   │                                 │
   │                                 │  5. Validates token
   │                                 │
   │                                 │  6. Calls service layer
   │                                 │
   │                                 │  7. Service calls DAO
   │                                 │
   │                                 │  8. DAO saves to database
   │                                 │
   │                                 │  9. Returns result
   │                                 │
   │  10. Axios receives response    │
   │<────────────────────────────────┤
   │                                 │
   │  11. React updates UI           │
   │                                 │
   │  12. User sees result           │
   │                                 │
```

### JSON Format

All data is sent as JSON (JavaScript Object Notation):

**Request**:
```json
{
  "word": "serendipity",
  "meaning": "finding something good"
}
```

**Response**:
```json
{
  "id": 42,
  "word": "serendipity",
  "meaning": "finding something good",
  "created_at": "2026-02-04T10:35:00Z"
}
```

JSON is like a universal language that both JavaScript and Python understand.

### Authentication with Tokens

Every request (except login/register) includes a token:

```
GET /api/vocab
Headers:
  Authorization: Bearer xK9mP2nQ7aB3cD4eF5gH6iJ7kL8mN9oP0
```

The backend:
1. Extracts the token
2. Looks it up in the sessions table
3. Checks if it's expired
4. Gets the user_id
5. Uses user_id for all database queries

This ensures:
- You can only see YOUR vocabulary
- You can't access other users' data
- Sessions expire after 24 hours (security)

### CORS (Cross-Origin Resource Sharing)

Your frontend (port 5173) and backend (port 5001) are on different ports, so browsers block requests by default (security feature).

**File: `backend/config/config.py`**

```python
CORS_ORIGINS = ['http://localhost:5173']
```

This tells Flask: "Allow requests from port 5173"

Without CORS configuration, you'd get errors like:
```
Access to fetch at 'http://localhost:5001/api/vocab' from origin 
'http://localhost:5173' has been blocked by CORS policy
```

---

## File-by-File Breakdown

Let me explain what each major file does:


### Backend Files

#### `backend/run.py`
**Purpose**: Entry point to start the Flask server
**What it does**:
- Imports the Flask app
- Runs it on port 5001
- Enables debug mode (shows detailed errors)

#### `backend/app/app.py`
**Purpose**: Creates and configures the Flask application
**What it does**:
- Creates Flask app instance
- Loads configuration
- Initializes database connection
- Registers all API routes (blueprints)
- Sets up CORS
- Adds error handlers

#### `backend/app/models/vocab_entry.py`
**Purpose**: Defines the VocabEntry database model
**What it does**:
- Defines table structure (columns, types, constraints)
- Defines relationships to User model
- Provides methods to convert to dictionary (for JSON responses)

#### `backend/app/dao/vocabulary_dao.py`
**Purpose**: Data Access Object - handles all database operations for vocabulary
**What it does**:
- `insert()`: Add new entry to database
- `update()`: Modify existing entry
- `delete()`: Remove entry
- `find_by_id()`: Get one entry by ID
- `find_by_user()`: Get all entries for a user
- `search()`: Search entries by keyword
- Handles database transactions (commit/rollback)

#### `backend/app/services/vocabulary_service.py`
**Purpose**: Business logic layer - validates and processes vocabulary operations
**What it does**:
- Validates input data (required fields, length limits)
- Sanitizes inputs (removes dangerous characters)
- Checks for duplicates
- Calls DAO methods
- Handles CSV import/export
- Returns formatted responses

#### `backend/app/services/csv_parser.py`
**Purpose**: Parses CSV files
**What it does**:
- Detects file encoding (UTF-8, UTF-16, etc.)
- Detects delimiter (comma, semicolon, tab)
- Reads CSV with pandas
- Validates columns
- Handles errors (malformed data, missing columns)
- Returns list of parsed entries

#### `backend/app/routes/vocab_routes.py`
**Purpose**: API endpoints for vocabulary operations
**What it does**:
- Defines routes: GET /api/vocab, POST /api/vocab, etc.
- Validates authentication token
- Extracts data from HTTP requests
- Calls service layer
- Returns JSON responses
- Handles errors (404, 400, 500)

#### `backend/app/services/auth_service.py`
**Purpose**: Handles authentication and session management
**What it does**:
- `register_user()`: Creates new user with hashed password
- `authenticate()`: Verifies username/password
- `create_session()`: Generates session token
- `validate_session()`: Checks if token is valid
- `logout()`: Deletes session

### Frontend Files

#### `frontend/src/main.tsx`
**Purpose**: Entry point for React app
**What it does**:
- Imports React and ReactDOM
- Imports root App component
- Renders App into the DOM
- Loads global CSS (Tailwind)

#### `frontend/src/App.tsx`
**Purpose**: Root component - sets up routing
**What it does**:
- Wraps app in AuthProvider (authentication context)
- Defines routes: `/login`, `/dashboard`
- Sets up protected routes (require login)
- Handles redirects

#### `frontend/src/contexts/AuthContext.tsx`
**Purpose**: Manages authentication state across the app
**What it does**:
- Stores current user and token
- Provides login/logout functions
- Validates session on app load
- Saves token to localStorage
- Makes auth state available to all components

#### `frontend/src/api/client.ts`
**Purpose**: API client - handles all HTTP requests to backend
**What it does**:
- Creates Axios instance with base URL
- Adds authentication token to all requests (interceptor)
- Defines all API methods:
  - `auth.login()`, `auth.register()`, `auth.logout()`
  - `vocab.getAll()`, `vocab.create()`, `vocab.update()`, `vocab.delete()`
  - `csv.upload()`, `csv.export()`
- Handles errors (401 → redirect to login)

#### `frontend/src/pages/Login.tsx`
**Purpose**: Login and registration page
**What it does**:
- Shows tabbed interface (Login / Register)
- Handles form input (username, password, remember me)
- Validates input (not empty)
- Calls API to login/register
- Shows error messages
- Redirects to dashboard on success

#### `frontend/src/pages/Dashboard.tsx`
**Purpose**: Main application page after login
**What it does**:
- Fetches vocabulary entries from API
- Shows SearchBar component
- Shows VocabList component
- Handles add/edit/delete operations
- Handles CSV import/export
- Shows loading states
- Shows error messages

#### `frontend/src/components/SearchBar.tsx`
**Purpose**: Search input with debouncing
**What it does**:
- Shows text input
- Debounces input (waits 300ms after typing stops)
- Calls parent's onSearch function
- Shows clear button

#### `frontend/src/components/VocabList.tsx`
**Purpose**: Displays vocabulary entries in a table
**What it does**:
- Receives entries as props
- Renders table with all fields
- Shows edit/delete buttons
- Handles empty state (no entries)
- Responsive design (mobile-friendly)

#### `frontend/src/components/EntryForm.tsx`
**Purpose**: Form for adding/editing vocabulary entries
**What it does**:
- Shows input fields for all vocabulary fields
- Validates required fields (word, meaning)
- Shows error messages
- Calls parent's onSubmit function
- Handles cancel button

#### `frontend/src/types/index.ts`
**Purpose**: TypeScript type definitions
**What it does**:
- Defines interfaces for VocabEntry, User, Category
- Defines API request/response types
- Provides type safety throughout the app

---

## Key Concepts Explained


### Layered Architecture

Your app uses a **layered architecture** - each layer has a specific job:

```
┌─────────────────────────────────────────┐
│  PRESENTATION LAYER (Frontend)          │
│  - React components                     │
│  - User interface                       │
│  - Handles user input                   │
└─────────────────────────────────────────┘
              │
              │ HTTP/JSON
              ▼
┌─────────────────────────────────────────┐
│  API LAYER (Routes)                     │
│  - Flask routes                         │
│  - HTTP request/response                │
│  - Authentication                       │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  BUSINESS LOGIC LAYER (Services)        │
│  - Validation                           │
│  - Business rules                       │
│  - Data processing                      │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  DATA ACCESS LAYER (DAOs)               │
│  - Database queries                     │
│  - CRUD operations                      │
│  - Transaction management               │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  DATABASE (SQLite)                      │
│  - Stores data                          │
│  - Enforces constraints                 │
└─────────────────────────────────────────┘
```

**Why layers?**
- **Separation of concerns**: Each layer does one thing well
- **Easier to test**: Test each layer independently
- **Easier to change**: Change one layer without affecting others
- **Reusability**: Services can be used by multiple routes

### React Component Lifecycle

When you load the Dashboard:

1. **Mount**: Component is created
   ```javascript
   useEffect(() => {
     fetchVocabulary()  // Load data from API
   }, [])  // Empty array = run once on mount
   ```

2. **Render**: Component displays UI
   ```javascript
   return (
     <div>
       <SearchBar />
       <VocabList entries={entries} />
     </div>
   )
   ```

3. **Update**: User types in search box
   - State changes: `setSearchQuery("seren")`
   - React re-renders component
   - VocabList shows filtered results

4. **Unmount**: User navigates away
   - Component is destroyed
   - Cleanup happens (cancel pending requests)

### State Management

**State** is data that changes over time:

```javascript
const [entries, setEntries] = useState([])  // List of vocabulary entries
const [loading, setLoading] = useState(false)  // Is data loading?
const [error, setError] = useState(null)  // Any errors?
const [searchQuery, setSearchQuery] = useState('')  // Search text
```

When state changes, React automatically re-renders the component.

**Example flow**:
1. User clicks "Add Entry"
2. API call succeeds
3. `setEntries([...entries, newEntry])` - Add new entry to state
4. React detects state change
5. React re-renders VocabList
6. User sees new entry

### Context API

**Context** shares state across multiple components without passing props:

```javascript
// AuthContext provides:
const { user, login, logout } = useAuth()

// Any component can access:
if (user) {
  // User is logged in
} else {
  // User is not logged in
}
```

Without context, you'd have to pass `user` through every component:
```
App → Dashboard → VocabList → EntryForm
```

With context, any component can access `user` directly.

### Async/Await

JavaScript is **asynchronous** - it doesn't wait for slow operations (like API calls):

**Without async/await** (callback hell):
```javascript
api.vocab.getAll().then(response => {
  setEntries(response.data)
}).catch(error => {
  setError(error.message)
})
```

**With async/await** (cleaner):
```javascript
try {
  const response = await api.vocab.getAll()
  setEntries(response.data)
} catch (error) {
  setError(error.message)
}
```

`await` pauses execution until the API call completes, making code easier to read.

### TypeScript Types

TypeScript adds **type checking** to JavaScript:

**JavaScript** (no types):
```javascript
function addEntry(entry) {
  // What is entry? What fields does it have?
  // You have to guess or check documentation
}
```

**TypeScript** (with types):
```typescript
interface VocabEntry {
  word: string
  meaning: string
  synonym?: string  // Optional
}

function addEntry(entry: VocabEntry) {
  // TypeScript knows entry has word and meaning
  // IDE shows autocomplete
  // Catches errors before running code
}
```

If you try to pass wrong data:
```typescript
addEntry({ word: 123 })  // ERROR: word must be string
```

TypeScript catches this error while you're coding, not when users are using your app.

---

## Common Patterns


### Error Handling

**Backend**:
```python
try:
    entry = vocabulary_dao.insert(user_id, data)
    return jsonify(entry), 201
except ValueError as e:
    return jsonify({'error': str(e)}), 400
except Exception as e:
    db.session.rollback()  # Undo database changes
    return jsonify({'error': 'Internal server error'}), 500
```

**Frontend**:
```typescript
try {
    const response = await api.vocab.create(entry)
    setEntries([...entries, response.data])
    showSuccess('Entry added!')
} catch (error) {
    if (error.response?.status === 401) {
        // Unauthorized - redirect to login
        logout()
    } else {
        showError('Failed to add entry')
    }
}
```

### Validation

**Frontend validation** (fast feedback):
```typescript
if (!word || !meaning) {
    setError('Word and meaning are required')
    return
}
if (word.length > 100) {
    setError('Word must be 100 characters or less')
    return
}
```

**Backend validation** (security):
```python
if not word or not meaning:
    raise ValueError('Word and meaning are required')
if len(word) > 100:
    raise ValueError('Word must be 100 characters or less')
```

**Why validate twice?**
- Frontend: Better user experience (instant feedback)
- Backend: Security (users can bypass frontend validation)

### Database Transactions

A **transaction** is a group of database operations that all succeed or all fail:

```python
try:
    # Start transaction
    entry1 = VocabEntry(word='word1', ...)
    entry2 = VocabEntry(word='word2', ...)
    db.session.add(entry1)
    db.session.add(entry2)
    db.session.commit()  # Save both entries
except Exception:
    db.session.rollback()  # Undo both entries
```

If entry2 fails, entry1 is also rolled back. This prevents partial data corruption.

### Debouncing

**Debouncing** delays execution until user stops typing:

```typescript
const [searchQuery, setSearchQuery] = useState('')

useEffect(() => {
    const timer = setTimeout(() => {
        // Execute search after 300ms of no typing
        performSearch(searchQuery)
    }, 300)
    
    return () => clearTimeout(timer)  // Cancel previous timer
}, [searchQuery])
```

**Without debouncing**: Typing "serendipity" sends 11 requests
**With debouncing**: Typing "serendipity" sends 1 request

### Password Hashing

**Never store passwords in plain text!**

```python
# User registers with password "secret123"
password = "secret123"

# Hash it with bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# Result: "$2b$12$KIXxJ7fG3nQ9mP2aB3cD4eF5gH6iJ7kL8mN9oP0qR1sT2uV3wX4yZ"

# Store hashed password in database
user.password_hash = hashed

# Later, when user logs in:
input_password = "secret123"
stored_hash = user.password_hash

# Verify password
if bcrypt.checkpw(input_password.encode(), stored_hash):
    # Password correct
else:
    # Password wrong
```

**Why hash?**
- If database is stolen, attackers can't see passwords
- Each password gets unique salt (prevents rainbow table attacks)
- Bcrypt is slow (makes brute-force attacks impractical)

---

## Performance Optimizations

### Database Indexing

Indexes make searches faster:

```python
class VocabEntry(Base):
    word = Column(String(100), index=True)  # Create index on word column
```

**Without index**: Search through all 10,000 entries (slow)
**With index**: SQLite uses index to find entries instantly (fast)

### React Memoization

Prevent unnecessary re-renders:

```typescript
const MemoizedVocabList = React.memo(VocabList)
```

If props don't change, React skips re-rendering.

### Lazy Loading

Load data only when needed:

```typescript
// Don't load all 10,000 entries at once
// Load 50 entries, then load more when user scrolls
```

(Not implemented yet, but could be added)

---

## Security Features

### Authentication Token

- Random 32-byte token (impossible to guess)
- Stored in localStorage (persists across page reloads)
- Sent with every request
- Expires after 24 hours

### Password Hashing

- Bcrypt with salt (unique per password)
- Slow algorithm (prevents brute-force)
- Never store plain text passwords

### SQL Injection Prevention

**Vulnerable code** (DON'T DO THIS):
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
```

Attacker could input: `admin' OR '1'='1`
Result: `SELECT * FROM users WHERE username = 'admin' OR '1'='1'`
This returns all users!

**Safe code** (SQLAlchemy does this):
```python
User.query.filter_by(username=username).first()
```

SQLAlchemy uses parameterized queries (safe from injection).

### XSS Prevention

**Cross-Site Scripting** (XSS) is when attackers inject malicious JavaScript:

**Vulnerable**:
```html
<div>{entry.word}</div>
```

If word is `<script>alert('hacked')</script>`, it executes!

**Safe** (React does this automatically):
```jsx
<div>{entry.word}</div>
```

React escapes HTML characters:
`<script>` becomes `&lt;script&gt;` (displays as text, doesn't execute)

### CORS

Only allows requests from `http://localhost:5173` (your frontend).
Blocks requests from other websites.

---

## What Happens When Things Go Wrong

### Backend Crashes

If Flask crashes:
1. You see error in terminal
2. Frontend gets network error
3. User sees "Failed to connect to server"
4. Fix the bug and restart Flask

### Database Locked

SQLite locks the database during writes:
1. User A saves entry
2. User B tries to save at same time
3. User B gets "database is locked" error
4. SQLAlchemy retries automatically
5. Usually succeeds on retry

### Token Expired

1. User's session expires (24 hours)
2. User tries to add entry
3. Backend returns 401 Unauthorized
4. Frontend detects 401
5. Redirects to login page
6. User logs in again

### Network Error

1. User's internet disconnects
2. API call fails
3. Frontend shows error message
4. User reconnects
5. User retries operation

---

## Summary

Your vocabulary app is a **full-stack web application** with:

**Frontend (React)**:
- User interface in the browser
- Handles user input and display
- Sends HTTP requests to backend
- Manages authentication state

**Backend (Flask)**:
- REST API server
- Validates and processes requests
- Manages database operations
- Handles authentication and security

**Database (SQLite)**:
- Stores all data (users, vocabulary, sessions)
- Enforces data integrity
- Provides fast queries

**Communication**:
- HTTP requests with JSON data
- Token-based authentication
- CORS for cross-origin requests

**Architecture**:
- Layered design (routes → services → DAOs → database)
- Separation of concerns
- Type safety with TypeScript
- Security best practices

Everything works together to provide a fast, secure, and user-friendly vocabulary management experience!

---

## Next Steps to Learn More

1. **Experiment**: Try modifying the code and see what happens
2. **Read the code**: Start with simple files like `models` and work up
3. **Use browser DevTools**: See network requests and responses
4. **Add console.log()**: Print variables to understand flow
5. **Break things**: Best way to learn is to fix what you broke!

**Recommended learning path**:
1. Understand one complete flow (e.g., adding an entry)
2. Trace it through all layers
3. Modify it slightly (add a new field)
4. Repeat with other features

You've built something real and functional - now explore and make it your own!
