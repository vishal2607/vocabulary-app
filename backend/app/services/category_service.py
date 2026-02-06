"""Category service for business logic and CRUD operations."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.category import Category
from app.dao.category_dao import CategoryDAO
from app.dao.vocabulary_dao import VocabularyDAO
import html


class CategoryService:
    """Service layer for category management.
    
    Provides business logic for CRUD operations, validation, and category
    assignment functionality. Handles input sanitization and validation
    before delegating to the DAO layer.
    """
    
    def __init__(self, db_session: Session):
        """Initialize the service with a database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
        self.dao = CategoryDAO(db_session)
        self.vocab_dao = VocabularyDAO(db_session)
    
    def create_category(self, user_id: int, name: str) -> Category:
        """Create a new category with validation.
        
        Args:
            user_id: ID of the user creating the category
            name: Name of the category
        
        Returns:
            Category: The created category with ID assigned
        
        Raises:
            ValueError: If validation fails (empty name, length violations, etc.)
            IntegrityError: If unique constraint is violated (duplicate name for user)
            SQLAlchemyError: For other database errors
        """
        # Sanitize input
        sanitized_name = self._sanitize_string(name)
        
        # Validate name
        validation_errors = self._validate_category_name(sanitized_name)
        if validation_errors:
            raise ValueError('; '.join(validation_errors))
        
        # Check for duplicate name
        existing = self.dao.find_by_name(user_id, sanitized_name)
        if existing:
            raise IntegrityError(
                f"Category with name '{sanitized_name}' already exists for this user",
                params=None,
                orig=None
            )
        
        try:
            # Create category
            category = Category(
                user_id=user_id,
                name=sanitized_name
            )
            
            # Insert category
            category_id = self.dao.insert(category)
            self.db.commit()
            
            # Return the created category
            return self.dao.find_by_id(category_id)
        except Exception as e:
            self.db.rollback()
            raise
    
    def update_category(self, category_id: int, user_id: int, name: str) -> Category:
        """Update an existing category with validation.
        
        Args:
            category_id: ID of the category to update
            user_id: ID of the user (for authorization check)
            name: New name for the category
        
        Returns:
            Category: The updated category
        
        Raises:
            ValueError: If validation fails or category not found
            PermissionError: If user doesn't own the category
            IntegrityError: If unique constraint is violated
            SQLAlchemyError: For other database errors
        """
        # Find existing category
        category = self.dao.find_by_id(category_id)
        if not category:
            raise ValueError(f"Category with ID {category_id} not found")
        
        # Check authorization
        if category.user_id != user_id:
            raise PermissionError("You don't have permission to update this category")
        
        # Sanitize input
        sanitized_name = self._sanitize_string(name)
        
        # Validate name
        validation_errors = self._validate_category_name(sanitized_name)
        if validation_errors:
            raise ValueError('; '.join(validation_errors))
        
        # Check for duplicate name (excluding current category)
        existing = self.dao.find_by_name(user_id, sanitized_name)
        if existing and existing.id != category_id:
            raise IntegrityError(
                f"Category with name '{sanitized_name}' already exists for this user",
                params=None,
                orig=None
            )
        
        try:
            # Update category
            success = self.dao.update(category_id, {'name': sanitized_name})
            if not success:
                raise ValueError(f"Failed to update category with ID {category_id}")
            
            self.db.commit()
            
            # Return updated category
            return self.dao.find_by_id(category_id)
        except Exception as e:
            self.db.rollback()
            raise
    
    def delete_category(self, category_id: int, user_id: int) -> bool:
        """Delete a category.
        
        When a category is deleted, all vocabulary entries assigned to it
        will have their category_id set to NULL (uncategorized) due to the
        ON DELETE SET NULL constraint.
        
        Args:
            category_id: ID of the category to delete
            user_id: ID of the user (for authorization check)
        
        Returns:
            bool: True if category was deleted
        
        Raises:
            ValueError: If category not found
            PermissionError: If user doesn't own the category
            SQLAlchemyError: For database errors
        """
        # Find existing category
        category = self.dao.find_by_id(category_id)
        if not category:
            raise ValueError(f"Category with ID {category_id} not found")
        
        # Check authorization
        if category.user_id != user_id:
            raise PermissionError("You don't have permission to delete this category")
        
        try:
            # Delete category (vocabulary entries will be set to NULL automatically)
            success = self.dao.delete(category_id)
            self.db.commit()
            return success
        except Exception as e:
            self.db.rollback()
            raise
    
    def get_categories(self, user_id: int) -> List[Category]:
        """Retrieve all categories for a user.
        
        Args:
            user_id: ID of the user
        
        Returns:
            List[Category]: List of categories (empty if none found)
        
        Raises:
            SQLAlchemyError: For database errors
        """
        try:
            return self.dao.find_by_user(user_id)
        except Exception as e:
            raise
    
    def get_category(self, category_id: int, user_id: int) -> Category:
        """Retrieve a specific category.
        
        Args:
            category_id: ID of the category to retrieve
            user_id: ID of the user (for authorization check)
        
        Returns:
            Category: The requested category
        
        Raises:
            ValueError: If category not found
            PermissionError: If user doesn't own the category
            SQLAlchemyError: For database errors
        """
        category = self.dao.find_by_id(category_id)
        if not category:
            raise ValueError(f"Category with ID {category_id} not found")
        
        # Check authorization
        if category.user_id != user_id:
            raise PermissionError("You don't have permission to access this category")
        
        return category
    
    def assign_category_to_entry(self, entry_id: int, user_id: int, category_id: Optional[int]) -> bool:
        """Assign a category to a vocabulary entry.
        
        Args:
            entry_id: ID of the vocabulary entry
            user_id: ID of the user (for authorization check)
            category_id: ID of the category to assign (None to uncategorize)
        
        Returns:
            bool: True if assignment was successful
        
        Raises:
            ValueError: If entry or category not found
            PermissionError: If user doesn't own the entry or category
            SQLAlchemyError: For database errors
        """
        # Find the vocabulary entry
        entry = self.vocab_dao.find_by_id(entry_id)
        if not entry:
            raise ValueError(f"Vocabulary entry with ID {entry_id} not found")
        
        # Check authorization for entry
        if entry.user_id != user_id:
            raise PermissionError("You don't have permission to modify this entry")
        
        # If category_id is provided, verify it exists and belongs to user
        if category_id is not None:
            category = self.dao.find_by_id(category_id)
            if not category:
                raise ValueError(f"Category with ID {category_id} not found")
            
            # Check authorization for category
            if category.user_id != user_id:
                raise PermissionError("You don't have permission to use this category")
        
        try:
            # Update the entry's category_id
            success = self.vocab_dao.update(entry_id, {'category_id': category_id})
            if not success:
                raise ValueError(f"Failed to assign category to entry with ID {entry_id}")
            
            self.db.commit()
            return success
        except Exception as e:
            self.db.rollback()
            raise
    
    def get_entries_by_category(self, user_id: int, category_id: Optional[int]) -> List:
        """Get all vocabulary entries in a specific category.
        
        Args:
            user_id: ID of the user
            category_id: ID of the category (None for uncategorized entries)
        
        Returns:
            List[VocabEntry]: List of vocabulary entries in the category
        
        Raises:
            ValueError: If category not found (when category_id is not None)
            PermissionError: If user doesn't own the category
            SQLAlchemyError: For database errors
        """
        # If category_id is provided, verify it exists and belongs to user
        if category_id is not None:
            category = self.dao.find_by_id(category_id)
            if not category:
                raise ValueError(f"Category with ID {category_id} not found")
            
            # Check authorization
            if category.user_id != user_id:
                raise PermissionError("You don't have permission to access this category")
        
        try:
            return self.vocab_dao.find_by_category(user_id, category_id)
        except Exception as e:
            raise
    
    def _validate_category_name(self, name: str) -> List[str]:
        """Validate category name.
        
        Args:
            name: Category name to validate
        
        Returns:
            List[str]: List of validation error messages (empty if valid)
        """
        errors = []
        
        # Check if name is empty or whitespace only
        if not name or not name.strip():
            errors.append("Category name is required and cannot be empty")
        
        # Check length (max 100 characters as per schema)
        if len(name) > 100:
            errors.append("Category name cannot exceed 100 characters")
        
        return errors
    
    def _sanitize_string(self, value: str) -> str:
        """Sanitize a string value to prevent XSS attacks.
        
        Args:
            value: String to sanitize
        
        Returns:
            str: Sanitized string with HTML entities escaped
        """
        if not isinstance(value, str):
            return str(value)
        
        # Escape HTML entities to prevent XSS
        sanitized = html.escape(value)
        
        # Remove any null bytes
        sanitized = sanitized.replace('\x00', '')
        
        return sanitized
