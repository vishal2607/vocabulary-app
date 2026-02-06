# Technology Stack

## Build System

- **Backend**: Python with pip for dependency management
- **Frontend**: Vite for fast development and optimized production builds

## Tech Stack

### Backend
- **Language**: Python 3.13
- **Framework**: Flask 3.0
- **Database**: SQLite with SQLAlchemy 2.0 ORM
- **Data Processing**: pandas 2.2
- **Authentication**: bcrypt 4.1
- **Testing**: pytest 7.4, hypothesis 6.92 (property-based testing)

### Frontend
- **Language**: TypeScript 5.2
- **Framework**: React 18.2
- **Build Tool**: Vite 5.0
- **Routing**: React Router 6.20
- **HTTP Client**: Axios 1.6
- **Visualizations**: D3.js 7.8, Recharts 2.10
- **Styling**: Tailwind CSS 3.3
- **Testing**: Jest 29.7, React Testing Library 14.1, fast-check 3.15 (property-based testing)

## Common Commands

### Backend Commands

```bash
# Activate virtual environment
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run property-based tests only
pytest tests/property/

# Run specific test file
pytest tests/unit/test_csv_parser.py
```

### Frontend Commands

```bash
# Install dependencies
cd frontend
npm install

# Development server (runs on http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run tests
npm test

# Run tests in watch mode
npm test:watch

# Run tests with coverage
npm test:coverage

# Lint code
npm run lint
```

## Dependencies

### Backend Dependencies (requirements.txt)
- Flask 3.0.0 - Web framework
- Flask-CORS 4.0.0 - CORS support
- SQLAlchemy 2.0.23 - ORM
- pandas 2.2.0 - CSV processing
- bcrypt 4.1.2 - Password hashing
- pytest 7.4.3 - Testing framework
- pytest-cov 4.1.0 - Coverage reporting
- hypothesis 6.92.2 - Property-based testing
- python-dotenv 1.0.0 - Environment variable management

### Frontend Dependencies (package.json)
- react 18.2.0 - UI framework
- react-dom 18.2.0 - React DOM rendering
- react-router-dom 6.20.1 - Routing
- axios 1.6.2 - HTTP client
- d3 7.8.5 - Data visualization
- d3-cloud 1.2.7 - Word cloud generation
- recharts 2.10.3 - Chart components
- typescript 5.2.2 - Type safety
- vite 5.0.8 - Build tool
- jest 29.7.0 - Testing framework
- @testing-library/react 14.1.2 - React testing utilities
- fast-check 3.15.0 - Property-based testing
- tailwindcss 3.3.6 - CSS framework
