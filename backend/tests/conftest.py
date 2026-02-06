"""Pytest configuration and fixtures for tests."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.models.base import Base
from app.models.user import User
from app.models.category import Category


# Create in-memory SQLite database for testing
@pytest.fixture(scope='function')
def db_engine():
    """Create a test database engine."""
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope='function')
def db_session(db_engine):
    """Create a test database session."""
    SessionLocal = sessionmaker(bind=db_engine)
    session = scoped_session(SessionLocal)
    
    yield session
    
    session.rollback()
    session.close()


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(username="testuser", password_hash="hashed_password")
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture
def test_category(db_session, test_user):
    """Create a test category."""
    category = Category(user_id=test_user.id, name="Test Category")
    db_session.add(category)
    db_session.commit()
    return category
