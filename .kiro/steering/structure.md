# Project Structure

## Current Organization

The Vocabulary Visualization App follows a full-stack architecture with separate backend and frontend directories.

## Conventions

### Backend (Python/Flask)
- **Source code**: Located in `backend/app/` directory
- **Test files**: Located in `backend/tests/` with subdirectories for unit, property, and integration tests
- **Configuration**: Located in `backend/config/` directory
- **Database**: SQLite database stored in `backend/data/` (gitignored)
- **Virtual environment**: `backend/venv/` (gitignored)

### Frontend (React/TypeScript)
- **Source code**: Located in `frontend/src/` directory
- **Components**: `frontend/src/components/` - React components organized by feature
- **API client**: `frontend/src/api/` - HTTP client and API integration
- **Types**: `frontend/src/types/` - TypeScript type definitions
- **Tests**: Co-located with source files using `.test.tsx` or `.test.ts` suffix
- **Build output**: `frontend/dist/` (gitignored)

### Testing Organization
- **Unit tests**: Test specific functions and components with known inputs
- **Property-based tests**: Test universal properties across many generated inputs
- **Integration tests**: Test complete workflows and API endpoints
- **Test naming**: `test_*.py` for Python, `*.test.ts(x)` for TypeScript

### Configuration Files
- **Environment variables**: `.env` files (gitignored), with `.env.example` templates
- **Python config**: `backend/config/config.py` for application settings
- **Frontend config**: `vite.config.ts`, `tsconfig.json`, `tailwind.config.js`

## Directory Layout

```
.
├── backend/                    # Python/Flask backend
│   ├── app/                   # Application code
│   │   ├── __init__.py
│   │   ├── models/           # SQLAlchemy models (to be created)
│   │   ├── services/         # Business logic (to be created)
│   │   ├── routes/           # API endpoints (to be created)
│   │   └── utils/            # Utility functions (to be created)
│   ├── config/               # Configuration
│   │   ├── __init__.py
│   │   └── config.py
│   ├── tests/                # Test suite
│   │   ├── __init__.py
│   │   ├── unit/            # Unit tests
│   │   ├── property/        # Property-based tests
│   │   └── integration/     # Integration tests
│   ├── data/                # Database files (gitignored)
│   ├── venv/                # Virtual environment (gitignored)
│   ├── requirements.txt     # Python dependencies
│   ├── pytest.ini          # Pytest configuration
│   └── .env.example        # Environment template
│
├── frontend/                  # React/TypeScript frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── api/            # API client
│   │   ├── types/          # TypeScript types
│   │   ├── App.tsx         # Main app component
│   │   ├── main.tsx        # Entry point
│   │   ├── index.css       # Global styles
│   │   ├── vite-env.d.ts   # Vite type definitions
│   │   └── setupTests.ts   # Test setup
│   ├── dist/               # Build output (gitignored)
│   ├── node_modules/       # Dependencies (gitignored)
│   ├── package.json        # Node dependencies
│   ├── vite.config.ts      # Vite configuration
│   ├── tsconfig.json       # TypeScript configuration
│   ├── tsconfig.node.json  # TypeScript config for Node
│   ├── jest.config.js      # Jest configuration
│   ├── tailwind.config.js  # Tailwind CSS configuration
│   ├── postcss.config.js   # PostCSS configuration
│   ├── .eslintrc.cjs       # ESLint configuration
│   ├── index.html          # HTML template
│   └── .env.example        # Environment template
│
├── .kiro/                     # Kiro AI assistant files
│   ├── specs/                # Feature specifications
│   │   └── vocabulary-visualization-app/
│   │       ├── requirements.md
│   │       ├── design.md
│   │       └── tasks.md
│   └── steering/             # AI guidance documents
│       ├── product.md
│       ├── structure.md
│       └── tech.md
│
├── .gitignore                # Git ignore rules
└── README.md                 # Project documentation
```

## File Naming Conventions

### Backend
- Python modules: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case()`
- Test files: `test_<module_name>.py`
- Constants: `UPPER_SNAKE_CASE`

### Frontend
- Components: `PascalCase.tsx`
- Utilities: `camelCase.ts`
- Types: `PascalCase` interfaces and types
- Test files: `<ComponentName>.test.tsx` or `<module>.test.ts`
- CSS classes: `kebab-case` (Tailwind utilities)
