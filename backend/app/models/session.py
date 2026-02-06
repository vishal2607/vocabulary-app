"""Session model for user authentication and session management."""
from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from app.models.base import Base
import secrets


class Session(Base):
    """Session model for managing authenticated user sessions.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to users table
        token: Unique session token (max 255 characters)
        expires_at: Timestamp when session expires
        created_at: Timestamp when session was created
        user: Relationship to User model
    """
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='sessions')
    
    # Indexes
    __table_args__ = (
        Index('idx_session_token', 'token'),
        Index('idx_session_expires', 'expires_at'),
    )
    
    def __repr__(self):
        return f'<Session(id={self.id}, user_id={self.user_id}, expires_at={self.expires_at})>'
    
    @staticmethod
    def generate_token():
        """Generate a secure random session token.
        
        Returns:
            str: A secure random token (64 characters)
        """
        return secrets.token_urlsafe(48)  # Generates ~64 character token
    
    def is_expired(self):
        """Check if the session has expired.
        
        Returns:
            bool: True if session is expired, False otherwise
        """
        return datetime.utcnow() > self.expires_at
    
    def extend_expiration(self, hours=24):
        """Extend the session expiration time.
        
        Args:
            hours: Number of hours to extend from now (default: 24)
        """
        self.expires_at = datetime.utcnow() + timedelta(hours=hours)
    
    def to_dict(self):
        """Convert model to dictionary representation.
        
        Returns:
            dict: Dictionary with all session fields
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token': self.token,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_expired': self.is_expired(),
        }
