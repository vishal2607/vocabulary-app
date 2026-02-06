"""Category API endpoints."""
from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.services.category_service import CategoryService
from app.routes.middleware import require_auth
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)

category_bp = Blueprint('categories', __name__)


@category_bp.route('', methods=['GET'])
@require_auth
def get_categories(user):
    """Retrieve all categories for the authenticated user.
    
    GET /api/categories
    Headers:
        Authorization: Bearer <token>
    
    Response (200 OK):
        {
            "categories": [
                {
                    "id": int,
                    "user_id": int,
                    "name": "string",
                    "created_at": "ISO timestamp"
                }
            ],
            "count": int
        }
    """
    db = SessionLocal()
    try:
        category_service = CategoryService(db)
        
        # Get all categories for user
        categories = category_service.get_categories(user.id)
        
        # Convert to dictionaries
        categories_data = [
            {
                'id': category.id,
                'user_id': category.user_id,
                'name': category.name,
                'created_at': category.created_at.isoformat() if category.created_at else None
            }
            for category in categories
        ]
        
        return jsonify({
            'categories': categories_data,
            'count': len(categories_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving categories: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while retrieving categories',
                'details': []
            }
        }), 500
    finally:
        db.close()


@category_bp.route('', methods=['POST'])
@require_auth
def create_category(user):
    """Create a new category.
    
    POST /api/categories
    Headers:
        Authorization: Bearer <token>
    Request body:
        {
            "name": "string" (required)
        }
    
    Response (201 Created):
        {
            "category": {
                "id": int,
                "user_id": int,
                "name": "string",
                "created_at": "ISO timestamp"
            }
        }
    
    Response (400 Bad Request):
        {
            "error": {
                "code": "VALIDATION_ERROR" | "DUPLICATE_ERROR",
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
                'details': ['JSON body with category name is required']
            }
        }), 400
    
    name = data.get('name')
    
    if not name:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Category name is required',
                'details': ['name field is required']
            }
        }), 400
    
    db = SessionLocal()
    try:
        category_service = CategoryService(db)
        
        # Create category
        category = category_service.create_category(user.id, name)
        
        logger.info(f"User {user.username} created category: {category.name}")
        
        return jsonify({
            'category': {
                'id': category.id,
                'user_id': category.user_id,
                'name': category.name,
                'created_at': category.created_at.isoformat() if category.created_at else None
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
        logger.error(f"Error creating category: {str(e)}")
        db.rollback()
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while creating the category',
                'details': []
            }
        }), 500
    finally:
        db.close()


@category_bp.route('/<int:category_id>', methods=['PUT'])
@require_auth
def update_category(user, category_id):
    """Update an existing category.
    
    PUT /api/categories/<id>
    Headers:
        Authorization: Bearer <token>
    Request body:
        {
            "name": "string" (required)
        }
    
    Response (200 OK):
        {
            "category": {
                "id": int,
                "user_id": int,
                "name": "string",
                "created_at": "ISO timestamp"
            }
        }
    
    Response (400 Bad Request / 404 Not Found):
        {
            "error": {
                "code": "VALIDATION_ERROR" | "NOT_FOUND" | "DUPLICATE_ERROR",
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
                'details': ['JSON body with category name is required']
            }
        }), 400
    
    name = data.get('name')
    
    if not name:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Category name is required',
                'details': ['name field is required']
            }
        }), 400
    
    db = SessionLocal()
    try:
        category_service = CategoryService(db)
        
        # Update category
        category = category_service.update_category(category_id, user.id, name)
        
        logger.info(f"User {user.username} updated category {category_id}")
        
        return jsonify({
            'category': {
                'id': category.id,
                'user_id': category.user_id,
                'name': category.name,
                'created_at': category.created_at.isoformat() if category.created_at else None
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
        logger.error(f"Error updating category {category_id}: {str(e)}")
        db.rollback()
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while updating the category',
                'details': []
            }
        }), 500
    finally:
        db.close()


@category_bp.route('/<int:category_id>', methods=['DELETE'])
@require_auth
def delete_category(user, category_id):
    """Delete a category.
    
    DELETE /api/categories/<id>
    Headers:
        Authorization: Bearer <token>
    
    Note: Vocabulary entries assigned to this category will be set to uncategorized.
    
    Response (200 OK):
        {
            "success": true,
            "message": "Category deleted successfully"
        }
    
    Response (404 Not Found):
        {
            "error": {
                "code": "NOT_FOUND",
                "message": "Category not found",
                "details": []
            }
        }
    """
    db = SessionLocal()
    try:
        category_service = CategoryService(db)
        
        # Delete category
        success = category_service.delete_category(category_id, user.id)
        
        if success:
            logger.info(f"User {user.username} deleted category {category_id}")
            return jsonify({
                'success': True,
                'message': 'Category deleted successfully'
            }), 200
        else:
            return jsonify({
                'error': {
                    'code': 'NOT_FOUND',
                    'message': 'Category not found',
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
        logger.error(f"Error deleting category {category_id}: {str(e)}")
        db.rollback()
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while deleting the category',
                'details': []
            }
        }), 500
    finally:
        db.close()


@category_bp.route('/<int:category_id>/entries', methods=['GET'])
@require_auth
def get_category_entries(user, category_id):
    """Get all vocabulary entries in a specific category.
    
    GET /api/categories/<id>/entries
    Headers:
        Authorization: Bearer <token>
    
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
                    "category_id": int,
                    "created_at": "ISO timestamp",
                    "updated_at": "ISO timestamp"
                }
            ],
            "count": int
        }
    """
    db = SessionLocal()
    try:
        category_service = CategoryService(db)
        
        # Get entries for category
        entries = category_service.get_entries_by_category(user.id, category_id)
        
        # Convert to dictionaries
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
        logger.error(f"Error retrieving entries for category {category_id}: {str(e)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred while retrieving entries',
                'details': []
            }
        }), 500
    finally:
        db.close()
