"""Database initialization and session management."""
import os
from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.engine import Engine
from config.config import SQLALCHEMY_DATABASE_URI, DATABASE_PATH
from app.models.base import Base
from app.models import User, VocabEntry, Category, Session


# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    echo=False,  # Set to True for SQL query logging
    connect_args={'check_same_thread': False}  # Needed for SQLite
)

# Enable foreign key constraints for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    """Enable foreign key constraints for SQLite connections."""
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create scoped session for thread-safe access
db_session = scoped_session(SessionLocal)


def init_db():
    """Initialize the database by creating all tables.
    
    This function:
    1. Creates the data directory if it doesn't exist
    2. Creates all tables defined in the models
    3. Ensures foreign key constraints are enabled
    
    Should be called once at application startup.
    """
    # Ensure data directory exists
    db_path = Path(DATABASE_PATH)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized at: {DATABASE_PATH}")


def drop_db():
    """Drop all tables from the database.
    
    WARNING: This will delete all data!
    Should only be used in testing or development.
    """
    Base.metadata.drop_all(bind=engine)
    print("All tables dropped")


def get_db():
    """Get a database session.
    
    This is a generator function that yields a database session
    and ensures it's properly closed after use.
    
    Usage:
        with get_db() as db:
            # Use db session
            pass
    
    Or in Flask/FastAPI:
        db = next(get_db())
        try:
            # Use db
        finally:
            db.close()
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def reset_db():
    """Reset the database by dropping and recreating all tables.
    
    WARNING: This will delete all data!
    Should only be used in testing or development.
    """
    drop_db()
    init_db()


if __name__ == '__main__':
    """Run this script directly to initialize the database."""
    print("Initializing database...")
    init_db()
    print("Database initialization complete!")
