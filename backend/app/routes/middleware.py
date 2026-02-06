"""Authentication middleware for protected routes."""
from functools import wraps
from flask import request, jsonify
from app.database import SessionLocal
from app.services.auth_service import AuthService


def require_auth(f):
    """Decorator to require authentication for a route.
    
    Validates the session token from the Authorization header
    and injects the authenticated user into the route function.
    
    Usage:
        @app.route('/api/protected')
        @require_auth
        def protected_route(user):
            # user is the authenticated User object
            return {'message': f'Hello {user.username}'}
    
    Args:
        f: The route function to wrap
    
    Returns:
        Wrapped function that validates authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Missing authorization header',
                    'details': ['Authorization header is required']
                }
            }), 401
        
        # Extract token from "Bearer <token>" format
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Invalid authorization header format',
                    'details': ['Expected format: Bearer <token>']
                }
            }), 401
        
        token = parts[1]
        
        # Validate session token
        db = SessionLocal()
        try:
            auth_service = AuthService(db)
            is_valid, user = auth_service.validate_session(token)
            
            if not is_valid or not user:
                return jsonify({
                    'error': {
                        'code': 'UNAUTHORIZED',
                        'message': 'Invalid or expired session token',
                        'details': ['Please log in again']
                    }
                }), 401
            
            # Inject user into route function
            return f(user, *args, **kwargs)
        finally:
            db.close()
    
    return decorated_function
