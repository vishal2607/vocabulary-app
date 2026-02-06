"""Data Access Object for Category operations."""
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.category import Category


class CategoryDAO:
    """Data Access Object for category database operations.
    
    Provides CRUD operations for managing vocabulary categories.
    All methods require a database session to be passed in.
    """
    
    def __init__(self, db_session: Session):
        """Initialize the DAO with a database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
    
    def insert(self, category: Category) -> int:
        """Insert a new category into the database.
        
        Args:
            category: Category object to insert (id should be None)
        
        Returns:
            int: The ID of the newly created category
        
        Raises:
            IntegrityError: If unique constraint is violated (duplicate name for user)
            SQLAlchemyError: For other database errors
        """
        self.db.add(category)
        self.db.flush()  # Flush to get the ID without committing
        return category.id
    
    def update(self, category_id: int, fields: dict) -> bool:
        """Update specific fields of a category.
        
        Args:
            category_id: ID of the category to update
            fields: Dictionary of field names and values to update
        
        Returns:
            bool: True if category was found and updated, False if not found
        
        Raises:
            SQLAlchemyError: For database errors
        """
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return False
        
        # Update only the provided fields
        for field, value in fields.items():
            if hasattr(category, field):
                setattr(category, field, value)
        
        self.db.flush()
        return True
    
    def delete(self, category_id: int) -> bool:
        """Delete a category by ID.
        
        Note: This will set category_id to NULL for all associated vocabulary
        entries due to the SET NULL delete rule.
        
        Args:
            category_id: ID of the category to delete
        
        Returns:
            bool: True if category was found and deleted, False if not found
        
        Raises:
            SQLAlchemyError: For database errors
        """
        category = self.db.query(Category).filter(Category.id == category_id).first()
        if not category:
            return False
        
        self.db.delete(category)
        self.db.flush()
        return True
    
    def find_by_id(self, category_id: int) -> Optional[Category]:
        """Find a category by its ID.
        
        Args:
            category_id: ID of the category to find
        
        Returns:
            Optional[Category]: The category if found, None otherwise
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def find_by_user(self, user_id: int) -> List[Category]:
        """Find all categories for a specific user.
        
        Args:
            user_id: ID of the user
        
        Returns:
            List[Category]: List of categories (empty if none found)
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(Category).filter(Category.user_id == user_id).all()
    
    def find_by_name(self, user_id: int, name: str) -> Optional[Category]:
        """Find a category by name for a specific user.
        
        Args:
            user_id: ID of the user
            name: Name of the category to find
        
        Returns:
            Optional[Category]: The category if found, None otherwise
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(Category).filter(
            Category.user_id == user_id,
            Category.name == name
        ).first()
    
    def exists(self, user_id: int, name: str) -> bool:
        """Check if a category with the given name exists for a user.
        
        Args:
            user_id: ID of the user
            name: Name of the category to check
        
        Returns:
            bool: True if category exists, False otherwise
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(Category).filter(
            Category.user_id == user_id,
            Category.name == name
        ).count() > 0
