# Vocabulary Visualization App

A full-stack web application for managing and visualizing vocabulary collections through multiple interactive views.

## Overview

The Vocabulary Visualization App enables users to:
- Import vocabulary data from CSV files
- View vocabulary through multiple visualization modes (cards, word cloud, list, categories)
- Search and filter vocabulary entries
- Edit and manage vocabulary collections
- Export vocabulary data to CSV format
- Secure user authentication and session management

## Technology Stack

### Backend
- **Language**: Python 3.9+
- **Framework**: Flask 3.0
- **Database**: SQLite with SQLAlchemy ORM
- **Data Processing**: pandas
- **Authentication**: bcrypt
- **Testing**: pytest, hypothesis (property-based testing)

### Frontend
- **Language**: TypeScript
- **Framework**: React 18+
- **Build Tool**: Vite
- **Routing**: React Router
- **HTTP Client**: Axios
- **Visualizations**: D3.js, Recharts
- **Styling**: Tailwind CSS
- **Testing**: Jest, React Testing Library, fast-check (property-based testing)

## Project Structure

```
.
├── backend/
│   ├── app/                    # Application code
│   ├── config/                 # Configuration files
│   ├── tests/                  # Test suite
│   │   ├── unit/              # Unit tests
│   │   ├── property/          # Property-based tests
│   │   └── integration/       # Integration tests
│   ├── venv/                  # Python virtual environment
│   ├── requirements.txt       # Python dependencies
│   └── .env.example          # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── api/              # API client
│   │   └── types/            # TypeScript type definitions
│   ├── package.json          # Node dependencies
│   └── .env.example         # Environment variables template
└── .kiro/
    └── specs/                # Feature specifications
```

## Setup Instructions

### Backend Setup

1. **Create and activate virtual environment:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run tests:**
   ```bash
   pytest
   ```

### Frontend Setup

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

4. **Run tests:**
   ```bash
   npm test
   ```

## Development Commands

### Backend

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=app --cov-report=html

# Run property-based tests only
pytest tests/property/

# Run specific test file
pytest tests/unit/test_csv_parser.py
```

### Frontend

```bash
# Development server
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

## API Endpoints

### Authentication
- `POST /api/auth/login` - Authenticate user
- `POST /api/auth/logout` - Terminate session
- `GET /api/auth/validate` - Validate session token

### Vocabulary
- `GET /api/vocab` - Retrieve vocabulary entries
- `POST /api/vocab` - Create new entry
- `PUT /api/vocab/:id` - Update entry
- `DELETE /api/vocab/:id` - Delete entry

### CSV Operations
- `POST /api/csv/upload` - Upload and import CSV file
- `GET /api/csv/export` - Export vocabulary to CSV

### Categories
- `GET /api/categories` - Retrieve all categories
- `POST /api/categories` - Create category
- `PUT /api/categories/:id` - Update category
- `DELETE /api/categories/:id` - Delete category

## CSV File Format

The application expects CSV files with the following columns:

```csv
word,meaning,synonym,pronunciation,example
vocabulary,a body of words used in a particular language,lexicon,voh-kab-yuh-ler-ee,"She has an extensive vocabulary."
```

**Required columns:**
- `word` - The vocabulary word (max 100 characters)
- `meaning` - Definition of the word

**Optional columns:**
- `synonym` - Alternative words with similar meaning
- `pronunciation` - Phonetic pronunciation guide
- `example` - Example sentence using the word

The parser supports:
- Multiple delimiters (comma, semicolon, tab)
- Various encodings (UTF-8, UTF-16, ASCII)
- Quoted fields with embedded delimiters
- Header row detection

## Testing Strategy

The project uses a dual testing approach:

### Unit Tests
- Test specific examples and edge cases
- Verify correct behavior for known inputs
- Test error conditions and exception handling

### Property-Based Tests
- Verify universal properties across many generated inputs
- Test with 100+ random test cases per property
- Automatically find edge cases through shrinking
- Each property test references its design document property

## Contributing

1. Review the specification documents in `.kiro/specs/vocabulary-visualization-app/`
2. Follow the implementation plan in `tasks.md`
3. Write both unit tests and property-based tests for new features
4. Ensure all tests pass before submitting changes
5. Follow the existing code style and conventions

## License

To be determined.

## Contact

To be determined.
