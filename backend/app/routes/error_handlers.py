"""Global error handlers for Flask application."""
from flask import jsonify
from werkzeug.exceptions import HTTPException
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    """Register global error handlers for the Flask application.
    
    Args:
        app: Flask application instance
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify({
            'error': {
                'code': 'BAD_REQUEST',
                'message': 'Bad request',
                'details': [str(error.description)] if hasattr(error, 'description') else [],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        """Handle 401 Unauthorized errors."""
        return jsonify({
            'error': {
                'code': 'UNAUTHORIZED',
                'message': 'Unauthorized access',
                'details': [str(error.description)] if hasattr(error, 'description') else [],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 Forbidden errors."""
        return jsonify({
            'error': {
                'code': 'FORBIDDEN',
                'message': 'Access forbidden',
                'details': [str(error.description)] if hasattr(error, 'description') else [],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': 'Resource not found',
                'details': [str(error.description)] if hasattr(error, 'description') else [],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        """Handle 405 Method Not Allowed errors."""
        return jsonify({
            'error': {
                'code': 'METHOD_NOT_ALLOWED',
                'message': 'Method not allowed',
                'details': [str(error.description)] if hasattr(error, 'description') else [],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        }), 405
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Handle 413 Request Entity Too Large errors."""
        return jsonify({
            'error': {
                'code': 'REQUEST_TOO_LARGE',
                'message': 'Request entity too large',
                'details': ['The uploaded file exceeds the maximum allowed size'],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        }), 413
    
    @app.errorhandler(415)
    def unsupported_media_type(error):
        """Handle 415 Unsupported Media Type errors."""
        return jsonify({
            'error': {
                'code': 'UNSUPPORTED_MEDIA_TYPE',
                'message': 'Unsupported media type',
                'details': [str(error.description)] if hasattr(error, 'description') else [],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        }), 415
    
    @app.errorhandler(500)
    def internal_server_error(error):
        """Handle 500 Internal Server Error."""
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An internal server error occurred',
                'details': [],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        }), 500
    
    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle all other HTTP exceptions."""
        logger.warning(f"HTTP exception: {error.code} - {error.description}")
        return jsonify({
            'error': {
                'code': error.name.upper().replace(' ', '_'),
                'message': error.description,
                'details': [],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        }), error.code
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle unexpected errors."""
        logger.error(f"Unexpected error: {str(error)}", exc_info=True)
        return jsonify({
            'error': {
                'code': 'INTERNAL_ERROR',
                'message': 'An unexpected error occurred',
                'details': [],
                'timestamp': datetime.utcnow().isoformat() + 'Z'
            }
        }), 500
    
    # Request logging middleware
    @app.before_request
    def log_request():
        """Log incoming requests."""
        from flask import request
        logger.info(f"{request.method} {request.path} - {request.remote_addr}")
    
    @app.after_request
    def log_response(response):
        """Log outgoing responses."""
        from flask import request
        logger.info(
            f"{request.method} {request.path} - "
            f"Status: {response.status_code} - "
            f"Size: {response.content_length or 0} bytes"
        )
        return response
