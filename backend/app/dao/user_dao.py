"""Data Access Object for User operations."""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User


class UserDAO:
    """Data Access Object for user database operations.
    
    Provides CRUD operations and user lookup functionality.
    All methods require a database session to be passed in.
    """
    
    def __init__(self, db_session: Session):
        """Initialize the DAO with a database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
    
    def insert(self, user: User) -> int:
        """Insert a new user into the database.
        
        Args:
            user: User object to insert (id should be None)
        
        Returns:
            int: The ID of the newly created user
        
        Raises:
            IntegrityError: If unique constraint is violated (duplicate username)
            SQLAlchemyError: For other database errors
        """
        self.db.add(user)
        self.db.flush()  # Flush to get the ID without committing
        return user.id
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Find a user by their ID.
        
        Args:
            user_id: ID of the user to find
        
        Returns:
            Optional[User]: The user if found, None otherwise
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(User).filter(User.id == user_id).first()
    
    def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by their username.
        
        Args:
            username: Username to search for
        
        Returns:
            Optional[User]: The user if found, None otherwise
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(User).filter(User.username == username).first()
    
    def update(self, user_id: int, fields: dict) -> bool:
        """Update specific fields of a user.
        
        Args:
            user_id: ID of the user to update
            fields: Dictionary of field names and values to update
        
        Returns:
            bool: True if user was found and updated, False if not found
        
        Raises:
            SQLAlchemyError: For database errors
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # Update only the provided fields
        for field, value in fields.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        self.db.flush()
        return True
    
    def delete(self, user_id: int) -> bool:
        """Delete a user by ID.
        
        Note: This will cascade delete all associated vocabulary entries,
        categories, and sessions due to the CASCADE delete rules.
        
        Args:
            user_id: ID of the user to delete
        
        Returns:
            bool: True if user was found and deleted, False if not found
        
        Raises:
            SQLAlchemyError: For database errors
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        self.db.delete(user)
        self.db.flush()
        return True
    
    def exists(self, username: str) -> bool:
        """Check if a user with the given username exists.
        
        Args:
            username: Username to check
        
        Returns:
            bool: True if user exists, False otherwise
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(User).filter(User.username == username).count() > 0
