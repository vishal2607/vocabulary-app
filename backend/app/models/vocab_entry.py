"""VocabEntry model for vocabulary data."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from app.models.base import Base


class VocabEntry(Base):
    """VocabEntry model representing a single vocabulary word with its details.
    
    Attributes:
        id: Primary key
        user_id: Foreign key to users table
        word: The vocabulary word (max 100 characters, required)
        meaning: Definition or meaning of the word (required)
        synonym: Optional synonym(s) (max 255 characters)
        pronunciation: Optional pronunciation guide (max 100 characters)
        example: Optional example sentence
        category_id: Optional foreign key to categories table
        created_at: Timestamp when entry was created
        updated_at: Timestamp when entry was last updated
        user: Relationship to User model
        category: Relationship to Category model
    """
    __tablename__ = 'vocab_entries'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    word = Column(String(100), nullable=False)
    meaning = Column(Text, nullable=False)
    synonym = Column(String(255), nullable=True)
    pronunciation = Column(String(100), nullable=True)
    example = Column(Text, nullable=True)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship('User', back_populates='vocab_entries')
    category = relationship('Category', back_populates='vocab_entries')
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'word', name='uq_user_word'),
        Index('idx_vocab_user', 'user_id'),
        Index('idx_vocab_word', 'word'),
        Index('idx_vocab_category', 'category_id'),
    )
    
    def __repr__(self):
        return f'<VocabEntry(id={self.id}, word={self.word}, user_id={self.user_id})>'
    
    def validate(self):
        """Validate entry fields and return list of errors.
        
        Returns:
            list[str]: List of validation error messages, empty if valid
        """
        errors = []
        
        if not self.word or not self.word.strip():
            errors.append("Word field is required and cannot be empty")
        elif len(self.word) > 100:
            errors.append("Word exceeds 100 characters")
        
        if not self.meaning or not self.meaning.strip():
            errors.append("Meaning field is required and cannot be empty")
        
        return errors
    
    def to_dict(self):
        """Convert model to dictionary representation.
        
        Returns:
            dict: Dictionary with all entry fields
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'word': self.word,
            'meaning': self.meaning,
            'synonym': self.synonym,
            'pronunciation': self.pronunciation,
            'example': self.example,
            'category_id': self.category_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
