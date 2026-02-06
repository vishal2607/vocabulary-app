# Quick Start Guide - Vocabulary Visualization App

## 🚀 Get the App Running in 5 Minutes

This guide will help you start both the backend and frontend to test the vocabulary app immediately.

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ and npm installed
- Terminal/Command prompt

## Step 1: Start the Backend (Terminal 1)

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the Flask server
python run.py
```

You should see:
```
 * Running on http://0.0.0.0:5001
 * Running on http://127.0.0.1:5001
```

✅ Backend is now running on **http://localhost:5001**

## Step 2: Start the Frontend (Terminal 2)

Open a **new terminal window** and run:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start the development server
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

✅ Frontend is now running on **http://localhost:5173**

## Step 3: Test the Application

1. **Open your browser** and go to: http://localhost:5173

2. **Register a new account:**
   - Click the "Register" tab
   - Enter a username (e.g., "testuser")
   - Enter a password (e.g., "password123")
   - Click "Register"

3. **You're in!** You should now see the main dashboard

## Step 4: Try the Features

### Add a Vocabulary Entry

1. Click the **"+ Add Entry"** button
2. Fill in the form:
   - **Word**: "serendipity" (required)
   - **Meaning**: "the occurrence of events by chance in a happy way" (required)
   - **Synonym**: "luck, fortune" (optional)
   - **Pronunciation**: "/ˌserənˈdɪpɪti/" (optional)
   - **Example**: "Finding that book was pure serendipity" (optional)
3. Click **"Add Entry"**

### Search Vocabulary

- Type in the search bar at the top right
- Results update in real-time as you type
- Search works across all fields (word, meaning, synonym, etc.)

### Edit an Entry

1. Click **"Edit"** next to any entry
2. Modify the fields
3. Click **"Update Entry"**

### Delete an Entry

1. Click **"Delete"** next to any entry
2. Confirm the deletion

### Import CSV

1. Create a CSV file with this content:
   ```csv
   word,meaning,synonym,pronunciation,example
   ephemeral,lasting for a very short time,fleeting,/ɪˈfem(ə)rəl/,The beauty of the sunset was ephemeral
   ubiquitous,present everywhere,omnipresent,/juːˈbɪkwɪtəs/,Smartphones are ubiquitous in modern society
   ```

2. Click **"Import CSV"**
3. Select your CSV file
4. See the import results

### Export CSV

1. Click **"Export CSV"**
2. A CSV file will download with all your vocabulary entries

## Troubleshooting

### Backend won't start

**Error: `ModuleNotFoundError: No module named 'flask'`**

Solution:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Error: `Address already in use`**

Solution: Another process is using port 5001. Kill it or change the port in `backend/run.py`

### Frontend won't start

**Error: `npm: command not found`**

Solution: Install Node.js from https://nodejs.org/

**Error: `Cannot find module`**

Solution:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors in Browser

If you see CORS errors in the browser console:

1. Make sure the backend is running on port 5001
2. Check that `backend/config/config.py` has:
   ```python
   CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')
   ```

### Can't Login

1. Make sure the backend is running
2. Check the browser console for errors
3. Try registering a new account
4. Clear browser localStorage and try again

## What You Can Do Now

✅ **User Authentication**: Register, login, logout
✅ **Vocabulary Management**: Add, edit, delete entries
✅ **Search**: Real-time search across all fields
✅ **CSV Import**: Upload vocabulary from CSV files
✅ **CSV Export**: Download your vocabulary as CSV
✅ **Categories**: Assign categories to entries (basic support)

## Architecture Overview

```
┌─────────────────────────────────────────┐
│  Browser (http://localhost:5173)        │
│  ┌────────────────────────────────────┐ │
│  │  React Frontend                    │ │
│  │  - Login/Register                  │ │
│  │  - Dashboard                       │ │
│  │  - Vocabulary List                 │ │
│  │  - Search & Forms                  │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
                    │
                    │ HTTP/JSON API
                    │ (Axios)
                    ▼
┌─────────────────────────────────────────┐
│  Backend (http://localhost:5001)        │
│  ┌────────────────────────────────────┐ │
│  │  Flask API                         │ │
│  │  - /api/auth/*                     │ │
│  │  - /api/vocab/*                    │ │
│  │  - /api/csv/*                      │ │
│  │  - /api/categories/*               │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  SQLite Database                   │ │
│  │  backend/data/vocabulary.db        │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## API Endpoints

The backend provides these REST API endpoints:

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `GET /api/auth/validate` - Validate session

### Vocabulary
- `GET /api/vocab` - Get all entries (with search/filter)
- `POST /api/vocab` - Create entry
- `PUT /api/vocab/:id` - Update entry
- `DELETE /api/vocab/:id` - Delete entry

### CSV
- `POST /api/csv/upload` - Import CSV
- `GET /api/csv/export` - Export CSV

### Categories
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Create category
- `PUT /api/categories/:id` - Update category
- `DELETE /api/categories/:id` - Delete category

## File Structure

```
.
├── backend/
│   ├── app/
│   │   ├── routes/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── dao/             # Database access
│   │   └── models/          # SQLAlchemy models
│   ├── data/                # SQLite database
│   ├── run.py               # Start backend
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── api/             # API client
│   │   ├── components/      # React components
│   │   ├── contexts/        # Auth context
│   │   ├── pages/           # Login, Dashboard
│   │   └── types/           # TypeScript types
│   ├── package.json         # Node dependencies
│   └── vite.config.ts       # Vite config
│
├── QUICKSTART.md            # This file
└── FRONTEND_SETUP.md        # Detailed frontend docs
```

## Next Steps

Now that you have the app running:

1. **Test all features** to ensure everything works
2. **Add more vocabulary entries** to see the list grow
3. **Try importing a CSV** with your own vocabulary
4. **Explore the code** to understand how it works

## Need Help?

- Check `FRONTEND_SETUP.md` for detailed frontend documentation
- Check `README.md` for project overview
- Review the code in `frontend/src/` and `backend/app/`

## What's NOT Included Yet

This is a **minimal but functional** implementation. The following features are not yet implemented:

- Word Cloud visualization
- Card View visualization  
- Categorized View
- Advanced filtering UI
- Sorting in list view
- Search result highlighting
- Category management UI
- Frontend tests

These can be added incrementally as needed!

---

**Enjoy your vocabulary app! 🎉**
