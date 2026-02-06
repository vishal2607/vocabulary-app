"""Vocabulary service for business logic and CRUD operations."""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models.vocab_entry import VocabEntry
from app.dao.vocabulary_dao import VocabularyDAO
from app.services.csv_parser import CSVParser, ParseResult
from datetime import datetime
import html
import re
import csv
import io


class VocabularyService:
    """Service layer for vocabulary entry management.
    
    Provides business logic for CRUD operations, validation, and search
    functionality for vocabulary entries. Handles input sanitization and
    validation before delegating to the DAO layer.
    """
    
    def __init__(self, db_session: Session):
        """Initialize the service with a database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
        self.dao = VocabularyDAO(db_session)
    
    def create_entry(self, user_id: int, entry_data: Dict[str, Any]) -> VocabEntry:
        """Create a new vocabulary entry with validation.
        
        Args:
            user_id: ID of the user creating the entry
            entry_data: Dictionary containing entry fields (word, meaning, etc.)
        
        Returns:
            VocabEntry: The created entry with ID assigned
        
        Raises:
            ValueError: If validation fails (empty required fields, length violations, etc.)
            IntegrityError: If unique constraint is violated (duplicate word for user)
            SQLAlchemyError: For other database errors
        """
        # Sanitize input data
        sanitized_data = self._sanitize_entry_data(entry_data)
        
        # Create entry object
        entry = VocabEntry(
            user_id=user_id,
            word=sanitized_data.get('word', ''),
            meaning=sanitized_data.get('meaning', ''),
            synonym=sanitized_data.get('synonym'),
            pronunciation=sanitized_data.get('pronunciation'),
            example=sanitized_data.get('example'),
            category_id=sanitized_data.get('category_id')
        )
        
        # Validate entry
        validation_errors = entry.validate()
        if validation_errors:
            raise ValueError('; '.join(validation_errors))
        
        # Check for duplicate word
        existing = self.dao.find_by_word(user_id, entry.word)
        if existing:
            raise IntegrityError(
                f"Vocabulary entry with word '{entry.word}' already exists for this user",
                params=None,
                orig=None
            )
        
        try:
            # Insert entry
            entry_id = self.dao.insert(entry)
            self.db.commit()
            
            # Return the created entry
            return self.dao.find_by_id(entry_id)
        except Exception as e:
            self.db.rollback()
            raise
    
    def update_entry(self, entry_id: int, user_id: int, updates: Dict[str, Any]) -> VocabEntry:
        """Update an existing vocabulary entry with validation.
        
        Args:
            entry_id: ID of the entry to update
            user_id: ID of the user (for authorization check)
            updates: Dictionary of fields to update
        
        Returns:
            VocabEntry: The updated entry
        
        Raises:
            ValueError: If validation fails or entry not found
            PermissionError: If user doesn't own the entry
            IntegrityError: If unique constraint is violated
            SQLAlchemyError: For other database errors
        """
        # Find existing entry
        entry = self.dao.find_by_id(entry_id)
        if not entry:
            raise ValueError(f"Vocabulary entry with ID {entry_id} not found")
        
        # Check authorization
        if entry.user_id != user_id:
            raise PermissionError("You don't have permission to update this entry")
        
        # Sanitize update data
        sanitized_updates = self._sanitize_entry_data(updates)
        
        # If updating word, check for duplicates
        if 'word' in sanitized_updates and sanitized_updates['word'] != entry.word:
            existing = self.dao.find_by_word(user_id, sanitized_updates['word'])
            if existing and existing.id != entry_id:
                raise IntegrityError(
                    f"Vocabulary entry with word '{sanitized_updates['word']}' already exists for this user",
                    params=None,
                    orig=None
                )
        
        # Apply updates to entry for validation
        temp_entry = VocabEntry(
            id=entry.id,
            user_id=entry.user_id,
            word=sanitized_updates.get('word', entry.word),
            meaning=sanitized_updates.get('meaning', entry.meaning),
            synonym=sanitized_updates.get('synonym', entry.synonym),
            pronunciation=sanitized_updates.get('pronunciation', entry.pronunciation),
            example=sanitized_updates.get('example', entry.example),
            category_id=sanitized_updates.get('category_id', entry.category_id)
        )
        
        # Validate updated entry
        validation_errors = temp_entry.validate()
        if validation_errors:
            raise ValueError('; '.join(validation_errors))
        
        try:
            # Update entry
            success = self.dao.update(entry_id, sanitized_updates)
            if not success:
                raise ValueError(f"Failed to update entry with ID {entry_id}")
            
            self.db.commit()
            
            # Return updated entry
            return self.dao.find_by_id(entry_id)
        except Exception as e:
            self.db.rollback()
            raise
    
    def delete_entry(self, entry_id: int, user_id: int) -> bool:
        """Delete a vocabulary entry.
        
        Args:
            entry_id: ID of the entry to delete
            user_id: ID of the user (for authorization check)
        
        Returns:
            bool: True if entry was deleted
        
        Raises:
            ValueError: If entry not found
            PermissionError: If user doesn't own the entry
            SQLAlchemyError: For database errors
        """
        # Find existing entry
        entry = self.dao.find_by_id(entry_id)
        if not entry:
            raise ValueError(f"Vocabulary entry with ID {entry_id} not found")
        
        # Check authorization
        if entry.user_id != user_id:
            raise PermissionError("You don't have permission to delete this entry")
        
        try:
            # Delete entry
            success = self.dao.delete(entry_id)
            self.db.commit()
            return success
        except Exception as e:
            self.db.rollback()
            raise
    
    def get_entries(self, user_id: int, filters: Optional[Dict[str, Any]] = None) -> List[VocabEntry]:
        """Retrieve vocabulary entries with optional filtering.
        
        Args:
            user_id: ID of the user
            filters: Optional dictionary of filter criteria:
                - category_id: Filter by category ID (None for uncategorized)
                - word: Filter by word substring (case-insensitive)
                - meaning: Filter by meaning substring (case-insensitive)
                - synonym: Filter by synonym substring (case-insensitive)
        
        Returns:
            List[VocabEntry]: List of matching entries
        
        Raises:
            SQLAlchemyError: For database errors
        """
        try:
            # If no filters, return all entries for user
            if not filters:
                return self.dao.find_by_user(user_id)
            
            # Start with all user entries
            entries = self.dao.find_by_user(user_id)
            
            # Apply category filter if specified
            if 'category_id' in filters:
                category_id = filters['category_id']
                entries = [e for e in entries if e.category_id == category_id]
            
            # Apply field filters (case-insensitive substring matching)
            if 'word' in filters and filters['word']:
                word_filter = filters['word'].lower()
                entries = [e for e in entries if word_filter in e.word.lower()]
            
            if 'meaning' in filters and filters['meaning']:
                meaning_filter = filters['meaning'].lower()
                entries = [e for e in entries if meaning_filter in e.meaning.lower()]
            
            if 'synonym' in filters and filters['synonym']:
                synonym_filter = filters['synonym'].lower()
                entries = [e for e in entries if e.synonym and synonym_filter in e.synonym.lower()]
            
            return entries
        except Exception as e:
            raise
    
    def search_entries(self, user_id: int, query: str) -> List[VocabEntry]:
        """Search vocabulary entries across all fields with full-text search.
        
        Performs case-insensitive substring search across word, meaning,
        synonym, pronunciation, and example fields.
        
        Args:
            user_id: ID of the user
            query: Search query string
        
        Returns:
            List[VocabEntry]: List of matching entries
        
        Raises:
            SQLAlchemyError: For database errors
        """
        try:
            # Sanitize search query
            sanitized_query = self._sanitize_string(query) if query else ''
            
            # Use DAO search method
            return self.dao.search(user_id, sanitized_query)
        except Exception as e:
            raise
    
    def _sanitize_entry_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize entry data to prevent XSS and SQL injection.
        
        Args:
            data: Dictionary of entry fields
        
        Returns:
            Dict[str, Any]: Sanitized data dictionary
        """
        sanitized = {}
        
        # Sanitize string fields
        string_fields = ['word', 'meaning', 'synonym', 'pronunciation', 'example']
        for field in string_fields:
            if field in data and data[field] is not None:
                sanitized[field] = self._sanitize_string(data[field])
            elif field in data:
                sanitized[field] = None
        
        # Pass through integer fields
        if 'category_id' in data:
            sanitized['category_id'] = data['category_id']
        
        return sanitized
    
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
    
    def import_from_csv(self, user_id: int, file_content: bytes, encoding: Optional[str] = None) -> 'ImportResult':
        """Import vocabulary entries from CSV file content.
        
        Parses the CSV file using CSVParser and creates vocabulary entries
        for the user. Handles duplicates by skipping entries that already
        exist for the user.
        
        Args:
            user_id: ID of the user importing the entries
            file_content: Raw bytes of the CSV file
            encoding: Optional encoding (will be auto-detected if not provided)
        
        Returns:
            ImportResult: Object containing import statistics and any errors
        
        Raises:
            SQLAlchemyError: For database errors
        """
        # Parse CSV file
        parser = CSVParser()
        try:
            parse_result = parser.parse_csv(file_content, encoding)
        except Exception as e:
            # Return import result with error
            return ImportResult(
                imported_count=0,
                skipped_count=0,
                error_count=1,
                errors=[f"CSV parsing failed: {str(e)}"]
            )
        
        # Track import statistics
        imported_count = 0
        skipped_count = 0
        error_count = 0
        errors = []
        
        # Import each parsed entry
        for entry_data in parse_result.entries:
            try:
                # Check if word already exists for this user
                existing = self.dao.find_by_word(user_id, entry_data['word'])
                if existing:
                    skipped_count += 1
                    errors.append(f"Skipped duplicate word: '{entry_data['word']}'")
                    continue
                
                # Create entry
                entry = VocabEntry(
                    user_id=user_id,
                    word=entry_data['word'],
                    meaning=entry_data['meaning'],
                    synonym=entry_data.get('synonym'),
                    pronunciation=entry_data.get('pronunciation'),
                    example=entry_data.get('example'),
                    category_id=None  # Categories not included in CSV import
                )
                
                # Validate entry
                validation_errors = entry.validate()
                if validation_errors:
                    error_count += 1
                    errors.append(f"Validation failed for word '{entry_data['word']}': {'; '.join(validation_errors)}")
                    continue
                
                # Insert entry
                self.dao.insert(entry)
                imported_count += 1
                
            except IntegrityError as e:
                error_count += 1
                errors.append(f"Database constraint violation for word '{entry_data['word']}': {str(e)}")
                self.db.rollback()
            except Exception as e:
                error_count += 1
                errors.append(f"Failed to import word '{entry_data['word']}': {str(e)}")
                self.db.rollback()
        
        # Commit all successful imports
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            errors.append(f"Failed to commit imports: {str(e)}")
            return ImportResult(
                imported_count=0,
                skipped_count=skipped_count,
                error_count=error_count + imported_count,
                errors=errors
            )
        
        # Include parsing errors in the result
        if parse_result.errors:
            errors.extend(parse_result.errors)
            error_count += len(parse_result.errors)
        
        return ImportResult(
            imported_count=imported_count,
            skipped_count=skipped_count,
            error_count=error_count,
            errors=errors
        )
    
    def export_to_csv(self, user_id: int, entry_ids: Optional[List[int]] = None) -> str:
        """Export vocabulary entries to CSV format.
        
        Exports all entries for the user, or only specified entries if
        entry_ids is provided. Generates CSV with proper escaping for
        special characters.
        
        Args:
            user_id: ID of the user whose entries to export
            entry_ids: Optional list of specific entry IDs to export.
                      If None, exports all entries for the user.
        
        Returns:
            str: CSV content as a string with proper formatting
        
        Raises:
            ValueError: If no entries found to export
            SQLAlchemyError: For database errors
        """
        # Get entries to export
        if entry_ids:
            # Export specific entries
            entries = []
            for entry_id in entry_ids:
                entry = self.dao.find_by_id(entry_id)
                if entry and entry.user_id == user_id:
                    entries.append(entry)
        else:
            # Export all entries for user
            entries = self.dao.find_by_user(user_id)
        
        if not entries:
            raise ValueError("No vocabulary entries found to export")
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        
        # Write header row
        writer.writerow(['word', 'meaning', 'synonym', 'pronunciation', 'example'])
        
        # Write data rows
        for entry in entries:
            writer.writerow([
                entry.word or '',
                entry.meaning or '',
                entry.synonym or '',
                entry.pronunciation or '',
                entry.example or ''
            ])
        
        # Get CSV content
        csv_content = output.getvalue()
        output.close()
        
        return csv_content
    
    def generate_export_filename(self, user_id: int, filtered: bool = False) -> str:
        """Generate a descriptive filename for CSV export.
        
        Args:
            user_id: ID of the user
            filtered: Whether the export is for filtered results
        
        Returns:
            str: Filename in format 'vocab_export_YYYY-MM-DD.csv' or
                'vocab_filtered_export_YYYY-MM-DD.csv'
        """
        date_str = datetime.now().strftime('%Y-%m-%d')
        if filtered:
            return f'vocab_filtered_export_{date_str}.csv'
        return f'vocab_export_{date_str}.csv'


class ImportResult:
    """Result of CSV import operation.
    
    Attributes:
        imported_count: Number of entries successfully imported
        skipped_count: Number of entries skipped (duplicates)
        error_count: Number of entries that failed to import
        errors: List of error messages
    """
    
    def __init__(self, imported_count: int, skipped_count: int, error_count: int, errors: List[str]):
        self.imported_count = imported_count
        self.skipped_count = skipped_count
        self.error_count = error_count
        self.errors = errors
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation.
        
        Returns:
            dict: Dictionary with import statistics and errors
        """
        return {
            'imported_count': self.imported_count,
            'skipped_count': self.skipped_count,
            'error_count': self.error_count,
            'errors': self.errors
        }
