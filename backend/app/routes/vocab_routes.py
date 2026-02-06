"""Vocabulary API endpoints."""
from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.services.vocabulary_service import VocabularyService
from app.routes.middleware import require_auth
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

vocab_bp = Blueprint('vocab', __name__)


@vocab_bp.route('', methods=['GET'])
@require_auth
def get_entries(user):
    """Retrieve vocabulary entries with optional filtering and search.
    
    GET /api/vocab?search=<query>&category=<id>&word=<filter>&meaning=<filter>&synonym=<filter>
    Headers:
        Authorization: Bearer <token>
    
    Query parameters:
        - search: Search query across all fields (optional)
        - category: Filter by category ID (optional)
        - word: Filter by word substring (optional)
        - meaning: Filter by meaning substring (optional)
        - synonym: Filter by synonym substring (optional)
    
    Response (200 OK):
        {
            "entries": [
                {
                    "id": int,
                    "user_id": int,
                    "word": "string",
                    "meaning": "string",
                    "synonym": "string" | null,
                    "pronunciation": "string" | null,
                    "example": "string" | null,
                    "category_id": int | null,
                    "created_at": "ISO timestamp",
                    "updated_at": "ISO timestamp"
                }
            ],
            "count": int
        }
    """
    db = SessionLocal()
    try:
        vocab_service = VocabularyService(db)
        
        # Check if search query is provided
        search_query = request.args.get('search')
        
        if search_query:
            # Perform full-text search
            entries = vocab_service.search_entries(user.id, search_query)
        else:
            # Build filters from query parameters
            filters = {}
            
            if request.args.get('category'):
                try:
                    category_id = int(request.args.get('category'))
                    filters['category_id'] = category_id
                except ValueError:
                    return jsonify({
                        'error': {
                            'code': 'VALIDATION_ERROR',
                            'message': 'Invalid category ID',
                            'details': ['category must be an integer']
                        }
                    }), 400
            
            if request.args.get('word'):
                filters['word'] = request.args.get('word')
            
            if request.args.get('meaning'):
                filters['meaning'] = request.args.get('meaning')
            
            if request.args.get('synonym'):
                filters['synonym'] = request.args.get('synonym')
            
            # Get entries with filters
            entries = vocab_service.get_entries(user.id, filters if filters else None)
        
        # Convert entries to dictionaries
        entries_data = [
            {
                'id': entry.id,
                'user_id': entry.user_id,
                'word': entry.word,
                'meaning': entry.meaning,
                'synonym': entry.synonym,
                'pronunciation': entry.pronunciation,
                'example': entry.example,
                'category_id': entry.category_id,
                'created_at': entry.created_at.isoformat() if entry.created_at else None,
                'updated_at': entry.updated_at.isoformat() if entry.updated_at else None
            }
            for entry in entries
        ]
        
        return jsonify({
            'entries': entries_data,
            'count': len(entries_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving vocabulary entries: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while retrieving entries',
                'details': []
            }
        }), 500
    finally:
        db.close()


@vocab_bp.route('', methods=['POST'])
@require_auth
def create_entry(user):
    """Create a new vocabulary entry.
    
    POST /api/vocab
    Headers:
        Authorization: Bearer <token>
    Request body:
        {
            "word": "string" (required),
            "meaning": "string" (required),
            "synonym": "string" (optional),
            "pronunciation": "string" (optional),
            "example": "string" (optional),
            "category_id": int (optional)
        }
    
    Response (201 Created):
        {
            "entry": {
                "id": int,
                "user_id": int,
                "word": "string",
                "meaning": "string",
                "synonym": "string" | null,
                "pronunciation": "string" | null,
                "example": "string" | null,
                "category_id": int | null,
                "created_at": "ISO timestamp",
                "updated_at": "ISO timestamp"
            }
        }
    
    Response (400 Bad Request):
        {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "string",
                "details": ["string"]
            }
        }
    """
    # Parse request body
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Request body is required',
                'details': ['JSON body with entry data is required']
            }
        }), 400
    
    db = SessionLocal()
    try:
        vocab_service = VocabularyService(db)
        
        # Create entry
        entry = vocab_service.create_entry(user.id, data)
        
        logger.info(f"User {user.username} created vocabulary entry: {entry.word}")
        
        return jsonify({
            'entry': {
                'id': entry.id,
                'user_id': entry.user_id,
                'word': entry.word,
                'meaning': entry.meaning,
                'synonym': entry.synonym,
                'pronunciation': entry.pronunciation,
                'example': entry.example,
                'category_id': entry.category_id,
                'created_at': entry.created_at.isoformat() if entry.created_at else None,
                'updated_at': entry.updated_at.isoformat() if entry.updated_at else None
            }
        }), 201
        
    except ValueError as e:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': str(e),
                'details': []
            }
        }), 400
    except IntegrityError as e:
        return jsonify({
            'error': {
                'code': 'DUPLICATE_ERROR',
                'message': str(e),
                'details': []
            }
        }), 400
    except Exception as e:
        logger.error(f"Error creating vocabulary entry: {str(e)}")
        db.rollback()
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while creating the entry',
                'details': []
            }
        }), 500
    finally:
        db.close()


@vocab_bp.route('/<int:entry_id>', methods=['PUT'])
@require_auth
def update_entry(user, entry_id):
    """Update an existing vocabulary entry.
    
    PUT /api/vocab/<id>
    Headers:
        Authorization: Bearer <token>
    Request body:
        {
            "word": "string" (optional),
            "meaning": "string" (optional),
            "synonym": "string" (optional),
            "pronunciation": "string" (optional),
            "example": "string" (optional),
            "category_id": int (optional)
        }
    
    Response (200 OK):
        {
            "entry": {
                "id": int,
                "user_id": int,
                "word": "string",
                "meaning": "string",
                "synonym": "string" | null,
                "pronunciation": "string" | null,
                "example": "string" | null,
                "category_id": int | null,
                "created_at": "ISO timestamp",
                "updated_at": "ISO timestamp"
            }
        }
    
    Response (400 Bad Request / 404 Not Found):
        {
            "error": {
                "code": "VALIDATION_ERROR" | "NOT_FOUND",
                "message": "string",
                "details": ["string"]
            }
        }
    """
    # Parse request body
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Request body is required',
                'details': ['JSON body with update data is required']
            }
        }), 400
    
    db = SessionLocal()
    try:
        vocab_service = VocabularyService(db)
        
        # Update entry
        entry = vocab_service.update_entry(entry_id, user.id, data)
        
        logger.info(f"User {user.username} updated vocabulary entry {entry_id}")
        
        return jsonify({
            'entry': {
                'id': entry.id,
                'user_id': entry.user_id,
                'word': entry.word,
                'meaning': entry.meaning,
                'synonym': entry.synonym,
                'pronunciation': entry.pronunciation,
                'example': entry.example,
                'category_id': entry.category_id,
                'created_at': entry.created_at.isoformat() if entry.created_at else None,
                'updated_at': entry.updated_at.isoformat() if entry.updated_at else None
            }
        }), 200
        
    except ValueError as e:
        error_msg = str(e)
        if 'not found' in error_msg.lower():
            return jsonify({
                'error': {
                    'code': 'NOT_FOUND',
                    'message': error_msg,
                    'details': []
                }
            }), 404
        else:
            return jsonify({
                'error': {
                    'code': 'VALIDATION_ERROR',
                    'message': error_msg,
                    'details': []
                }
            }), 400
    except PermissionError as e:
        return jsonify({
            'error': {
                'code': 'FORBIDDEN',
                'message': str(e),
                'details': []
            }
        }), 403
    except IntegrityError as e:
        return jsonify({
            'error': {
                'code': 'DUPLICATE_ERROR',
                'message': str(e),
                'details': []
            }
        }), 400
    except Exception as e:
        logger.error(f"Error updating vocabulary entry {entry_id}: {str(e)}")
        db.rollback()
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while updating the entry',
                'details': []
            }
        }), 500
    finally:
        db.close()


@vocab_bp.route('/<int:entry_id>', methods=['DELETE'])
@require_auth
def delete_entry(user, entry_id):
    """Delete a vocabulary entry.
    
    DELETE /api/vocab/<id>
    Headers:
        Authorization: Bearer <token>
    
    Response (200 OK):
        {
            "success": true,
            "message": "Entry deleted successfully"
        }
    
    Response (404 Not Found):
        {
            "error": {
                "code": "NOT_FOUND",
                "message": "Entry not found",
                "details": []
            }
        }
    """
    db = SessionLocal()
    try:
        vocab_service = VocabularyService(db)
        
        # Delete entry
        success = vocab_service.delete_entry(entry_id, user.id)
        
        if success:
            logger.info(f"User {user.username} deleted vocabulary entry {entry_id}")
            return jsonify({
                'success': True,
                'message': 'Entry deleted successfully'
            }), 200
        else:
            return jsonify({
                'error': {
                    'code': 'NOT_FOUND',
                    'message': 'Entry not found',
                    'details': []
                }
            }), 404
        
    except ValueError as e:
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': str(e),
                'details': []
            }
        }), 404
    except PermissionError as e:
        return jsonify({
            'error': {
                'code': 'FORBIDDEN',
                'message': str(e),
                'details': []
            }
        }), 403
    except Exception as e:
        logger.error(f"Error deleting vocabulary entry {entry_id}: {str(e)}")
        db.rollback()
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while deleting the entry',
                'details': []
            }
        }), 500
    finally:
        db.close()
