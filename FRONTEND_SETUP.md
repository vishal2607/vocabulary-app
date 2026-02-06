# Frontend Setup Guide

## What's Been Created

A minimal but functional frontend has been implemented with the following components:

### ✅ Completed Components

1. **TypeScript Types** (`frontend/src/types/index.ts`)
   - VocabEntry, User, Category interfaces
   - API request/response types
   - Error handling types

2. **API Client** (`frontend/src/api/client.ts`)
   - Axios-based HTTP client
   - Authentication token management
   - All backend endpoints integrated:
     - Auth: login, register, logout, validate
     - Vocabulary: CRUD operations, search
     - Categories: CRUD operations
     - CSV: upload and export

3. **Authentication Context** (`frontend/src/contexts/AuthContext.tsx`)
   - React context for user state management
   - Session validation on app load
   - Login/logout functionality

4. **Pages**
   - **Login** (`frontend/src/pages/Login.tsx`): Login and registration forms
   - **Dashboard** (`frontend/src/pages/Dashboard.tsx`): Main vocabulary management interface

5. **Components**
   - **ProtectedRoute** (`frontend/src/components/ProtectedRoute.tsx`): Route guard for authentication
   - **SearchBar** (`frontend/src/components/SearchBar.tsx`): Debounced search input
   - **EntryForm** (`frontend/src/components/EntryForm.tsx`): Add/edit vocabulary entries
   - **VocabList** (`frontend/src/components/VocabList.tsx`): Table view of vocabulary entries

6. **Routing** (`frontend/src/App.tsx`)
   - React Router setup with protected routes
   - Automatic redirect to login for unauthenticated users

## Features Implemented

✅ User authentication (login/register)
✅ Session management with token storage
✅ Add/edit/delete vocabulary entries
✅ Real-time search across all fields
✅ CSV import/export
✅ Category support
✅ Form validation
✅ Error handling
✅ Responsive design with Tailwind CSS

## Setup Instructions

### Prerequisites

- Node.js 18+ and npm installed
- Backend server running on http://localhost:5001

### Installation Steps

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm run dev
   ```

4. **Open browser:**
   Navigate to http://localhost:5173

## Testing the Application

### 1. Start the Backend

First, ensure the backend is running:

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python run.py
```

The backend should be running on http://localhost:5001

### 2. Start the Frontend

In a new terminal:

```bash
cd frontend
npm run dev
```

The frontend will be available at http://localhost:5173

### 3. Test the Flow

1. **Register a new user:**
   - Open http://localhost:5173
   - Click "Register" tab
   - Enter username and password
   - Click "Register"

2. **Add vocabulary entries:**
   - Click "+ Add Entry"
   - Fill in word and meaning (required)
   - Optionally add synonym, pronunciation, example, category
   - Click "Add Entry"

3. **Search vocabulary:**
   - Type in the search bar
   - Results update in real-time

4. **Edit/Delete entries:**
   - Click "Edit" to modify an entry
   - Click "Delete" to remove an entry

5. **Import CSV:**
   - Click "Import CSV"
   - Select a CSV file with columns: word, meaning, synonym, pronunciation, example
   - View import results

6. **Export CSV:**
   - Click "Export CSV"
   - File downloads automatically

## API Configuration

The frontend is configured to connect to the backend at:
```
http://localhost:5001/api
```

If your backend runs on a different port, update `frontend/src/api/client.ts`:

```typescript
const API_BASE_URL = 'http://localhost:YOUR_PORT/api';
```

## Project Structure

```
frontend/src/
├── api/
│   └── client.ts           # API client with all endpoints
├── components/
│   ├── EntryForm.tsx       # Add/edit form
│   ├── ProtectedRoute.tsx  # Auth guard
│   ├── SearchBar.tsx       # Search input
│   └── VocabList.tsx       # Table view
├── contexts/
│   └── AuthContext.tsx     # Auth state management
├── pages/
│   ├── Dashboard.tsx       # Main app page
│   └── Login.tsx           # Login/register page
├── types/
│   └── index.ts            # TypeScript types
├── App.tsx                 # Router setup
├── main.tsx                # Entry point
└── index.css               # Global styles
```

## What's NOT Included (Future Enhancements)

The following features from the spec are not yet implemented (keeping it minimal):

- ❌ Word Cloud visualization
- ❌ Card View visualization
- ❌ Categorized View
- ❌ Advanced filtering (multi-field)
- ❌ Sorting in list view
- ❌ Search result highlighting
- ❌ Category management UI
- ❌ Tests

These can be added incrementally as needed.

## Troubleshooting

### CORS Errors

If you see CORS errors in the browser console, ensure the backend has CORS enabled for http://localhost:5173:

```python
# backend/app/__init__.py
from flask_cors import CORS
CORS(app, origins=['http://localhost:5173'])
```

### 401 Unauthorized

If you get 401 errors:
1. Check that you're logged in
2. Clear localStorage and log in again
3. Verify the backend session is valid

### Connection Refused

If the frontend can't connect to the backend:
1. Verify backend is running on port 5001
2. Check the API_BASE_URL in `frontend/src/api/client.ts`
3. Ensure no firewall is blocking the connection

## Next Steps

1. Install dependencies: `npm install`
2. Start dev server: `npm run dev`
3. Test the application with the backend
4. Add more features as needed (word cloud, card view, etc.)

## Notes

- The frontend uses localStorage to persist authentication tokens
- All API calls include the Bearer token automatically
- Form validation is done client-side before API calls
- Error messages from the backend are displayed to users
