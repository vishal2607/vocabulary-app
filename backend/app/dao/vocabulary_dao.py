"""Data Access Object for VocabEntry operations."""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.vocab_entry import VocabEntry


class VocabularyDAO:
    """Data Access Object for vocabulary entry database operations.
    
    Provides CRUD operations and search functionality for vocabulary entries.
    All methods require a database session to be passed in.
    """
    
    def __init__(self, db_session: Session):
        """Initialize the DAO with a database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
    
    def insert(self, entry: VocabEntry) -> int:
        """Insert a new vocabulary entry into the database.
        
        Args:
            entry: VocabEntry object to insert (id should be None)
        
        Returns:
            int: The ID of the newly created entry
        
        Raises:
            IntegrityError: If unique constraint is violated (duplicate word for user)
            SQLAlchemyError: For other database errors
        """
        self.db.add(entry)
        self.db.flush()  # Flush to get the ID without committing
        return entry.id
    
    def update(self, entry_id: int, fields: dict) -> bool:
        """Update specific fields of a vocabulary entry.
        
        Args:
            entry_id: ID of the entry to update
            fields: Dictionary of field names and values to update
        
        Returns:
            bool: True if entry was found and updated, False if not found
        
        Raises:
            SQLAlchemyError: For database errors
        """
        entry = self.db.query(VocabEntry).filter(VocabEntry.id == entry_id).first()
        if not entry:
            return False
        
        # Update only the provided fields
        for field, value in fields.items():
            if hasattr(entry, field):
                setattr(entry, field, value)
        
        self.db.flush()
        return True
    
    def delete(self, entry_id: int) -> bool:
        """Delete a vocabulary entry by ID.
        
        Args:
            entry_id: ID of the entry to delete
        
        Returns:
            bool: True if entry was found and deleted, False if not found
        
        Raises:
            SQLAlchemyError: For database errors
        """
        entry = self.db.query(VocabEntry).filter(VocabEntry.id == entry_id).first()
        if not entry:
            return False
        
        self.db.delete(entry)
        self.db.flush()
        return True
    
    def find_by_user(self, user_id: int) -> List[VocabEntry]:
        """Find all vocabulary entries for a specific user.
        
        Args:
            user_id: ID of the user
        
        Returns:
            List[VocabEntry]: List of vocabulary entries (empty if none found)
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(VocabEntry).filter(VocabEntry.user_id == user_id).all()
    
    def find_by_id(self, entry_id: int) -> Optional[VocabEntry]:
        """Find a vocabulary entry by its ID.
        
        Args:
            entry_id: ID of the entry to find
        
        Returns:
            Optional[VocabEntry]: The entry if found, None otherwise
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(VocabEntry).filter(VocabEntry.id == entry_id).first()
    
    def search(self, user_id: int, query: str) -> List[VocabEntry]:
        """Search vocabulary entries across all text fields.
        
        Performs case-insensitive substring search across word, meaning,
        synonym, pronunciation, and example fields.
        
        Args:
            user_id: ID of the user whose entries to search
            query: Search query string
        
        Returns:
            List[VocabEntry]: List of matching entries (empty if none found)
        
        Raises:
            SQLAlchemyError: For database errors
        """
        if not query:
            return self.find_by_user(user_id)
        
        # Case-insensitive search across all text fields
        search_pattern = f"%{query}%"
        return self.db.query(VocabEntry).filter(
            VocabEntry.user_id == user_id,
            or_(
                VocabEntry.word.ilike(search_pattern),
                VocabEntry.meaning.ilike(search_pattern),
                VocabEntry.synonym.ilike(search_pattern),
                VocabEntry.pronunciation.ilike(search_pattern),
                VocabEntry.example.ilike(search_pattern)
            )
        ).all()
    
    def find_by_category(self, user_id: int, category_id: Optional[int]) -> List[VocabEntry]:
        """Find all vocabulary entries in a specific category.
        
        Args:
            user_id: ID of the user
            category_id: ID of the category (None for uncategorized entries)
        
        Returns:
            List[VocabEntry]: List of vocabulary entries in the category
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(VocabEntry).filter(
            VocabEntry.user_id == user_id,
            VocabEntry.category_id == category_id
        ).all()
    
    def find_by_word(self, user_id: int, word: str) -> Optional[VocabEntry]:
        """Find a vocabulary entry by exact word match for a user.
        
        Args:
            user_id: ID of the user
            word: The exact word to search for
        
        Returns:
            Optional[VocabEntry]: The entry if found, None otherwise
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(VocabEntry).filter(
            VocabEntry.user_id == user_id,
            VocabEntry.word == word
        ).first()
