"""Category model for organizing vocabulary entries."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.models.base import Base


class Category(Base):
    """Category model for grouping vocabulary entries thematically.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to users table
        name: Category name (max 100 characters, required)
        created_at: Timestamp when category was created
        user: Relationship to User model
        vocab_entries: Relationship to VocabEntry models in this category
    """
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='categories')
    vocab_entries = relationship('VocabEntry', back_populates='category', lazy='dynamic')
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_user_category_name'),
        Index('idx_category_user', 'user_id'),
    )
    
    def __repr__(self):
        return f'<Category(id={self.id}, name={self.name}, user_id={self.user_id})>'
    
    def to_dict(self):
        """Convert model to dictionary representation.
        
        Returns:
            dict: Dictionary with all category fields
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
