"""Authentication API endpoints."""
from flask import Blueprint, request, jsonify
from app.database import SessionLocal
from app.services.auth_service import AuthService, AuthenticationError, RegistrationError
from app.routes.middleware import require_auth
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and create session.
    
    POST /api/auth/login
    Request body:
        {
            "username": "string",
            "password": "string",
            "remember": boolean (optional, default: false)
        }
    
    Response (200 OK):
        {
            "user": {
                "id": int,
                "username": "string",
                "created_at": "ISO timestamp"
            },
            "token": "string"
        }
    
    Response (400 Bad Request):
        {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "string",
                "details": ["string"]
            }
        }
    
    Response (401 Unauthorized):
        {
            "error": {
                "code": "AUTHENTICATION_ERROR",
                "message": "Invalid credentials",
                "details": []
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
                'details': ['JSON body with username and password is required']
            }
        }), 400
    
    username = data.get('username')
    password = data.get('password')
    remember = data.get('remember', False)
    
    # Validate required fields
    if not username or not password:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Missing required fields',
                'details': ['username and password are required']
            }
        }), 400
    
    # Authenticate user
    db = SessionLocal()
    try:
        auth_service = AuthService(db)
        
        # Authenticate credentials
        user = auth_service.authenticate(username, password)
        
        # Create session
        session = auth_service.create_session(user.id, remember=remember)
        
        logger.info(f"User {username} logged in successfully")
        
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'created_at': user.created_at.isoformat() if user.created_at else None
            },
            'token': session.token
        }), 200
        
    except AuthenticationError as e:
        logger.warning(f"Failed login attempt for username: {username}")
        return jsonify({
            'error': {
                'code': 'AUTHENTICATION_ERROR',
                'message': str(e),
                'details': []
            }
        }), 401
    except Exception as e:
        logger.error(f"Error during login: {str(e)}")
        db.rollback()
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred during login',
                'details': []
            }
        }), 500
    finally:
        db.close()


@auth_bp.route('/logout', methods=['POST'])
@require_auth
def logout(user):
    """Terminate user session (logout).
    
    POST /api/auth/logout
    Headers:
        Authorization: Bearer <token>
    
    Response (200 OK):
        {
            "success": true,
            "message": "Logged out successfully"
        }
    
    Response (401 Unauthorized):
        {
            "error": {
                "code": "UNAUTHORIZED",
                "message": "Invalid or expired session token",
                "details": []
            }
        }
    """
    # Get token from authorization header
    auth_header = request.headers.get('Authorization')
    token = auth_header.split()[1] if auth_header else None
    
    if not token:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Session token is required',
                'details': []
            }
        }), 400
    
    # Logout (terminate session)
    db = SessionLocal()
    try:
        auth_service = AuthService(db)
        success = auth_service.logout(token)
        
        if success:
            logger.info(f"User {user.username} logged out successfully")
            return jsonify({
                'success': True,
                'message': 'Logged out successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Session not found'
            }), 200
            
    except Exception as e:
        logger.error(f"Error during logout: {str(e)}")
        db.rollback()
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred during logout',
                'details': []
            }
        }), 500
    finally:
        db.close()


@auth_bp.route('/validate', methods=['GET'])
@require_auth
def validate(user):
    """Validate session token and return user information.
    
    GET /api/auth/validate
    Headers:
        Authorization: Bearer <token>
    
    Response (200 OK):
        {
            "user": {
                "id": int,
                "username": "string",
                "created_at": "ISO timestamp"
            }
        }
    
    Response (401 Unauthorized):
        {
            "error": {
                "code": "UNAUTHORIZED",
                "message": "Invalid or expired session token",
                "details": []
            }
        }
    """
    # User is already validated by @require_auth decorator
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'created_at': user.created_at.isoformat() if user.created_at else None
        }
    }), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user.
    
    POST /api/auth/register
    Request body:
        {
            "username": "string",
            "password": "string"
        }
    
    Response (201 Created):
        {
            "user": {
                "id": int,
                "username": "string",
                "created_at": "ISO timestamp"
            },
            "message": "User registered successfully"
        }
    
    Response (400 Bad Request):
        {
            "error": {
                "code": "VALIDATION_ERROR" | "REGISTRATION_ERROR",
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
                'details': ['JSON body with username and password is required']
            }
        }), 400
    
    username = data.get('username')
    password = data.get('password')
    
    # Validate required fields
    if not username or not password:
        return jsonify({
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Missing required fields',
                'details': ['username and password are required']
            }
        }), 400
    
    # Register user
    db = SessionLocal()
    try:
        auth_service = AuthService(db)
        user = auth_service.register_user(username, password)
        
        logger.info(f"New user registered: {username}")
        
        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'created_at': user.created_at.isoformat() if user.created_at else None
            },
            'message': 'User registered successfully'
        }), 201
        
    except RegistrationError as e:
        logger.warning(f"Registration failed for username {username}: {str(e)}")
        return jsonify({
            'error': {
                'code': 'REGISTRATION_ERROR',
                'message': str(e),
                'details': []
            }
        }), 400
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        db.rollback()
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An error occurred during registration',
                'details': []
            }
        }), 500
    finally:
        db.close()
