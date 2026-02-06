"""User model for authentication and data ownership."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.models.base import Base


class User(Base):
    """User model representing an authenticated user.
    
    Attributes:
        id: Primary key
        username: Unique username for login (max 50 characters)
        password_hash: Bcrypt hashed password (max 255 characters)
        created_at: Timestamp when user was created
        vocab_entries: Relationship to user's vocabulary entries
        categories: Relationship to user's categories
        sessions: Relationship to user's active sessions
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    vocab_entries = relationship(
        'VocabEntry',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )
    categories = relationship(
        'Category',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )
    sessions = relationship(
        'Session',
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<User(id={self.id}, username={self.username})>'
