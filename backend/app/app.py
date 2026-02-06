"""Flask application factory and configuration."""
from flask import Flask
from flask_cors import CORS
from config.config import CORS_ORIGINS, SECRET_KEY
from app.database import init_db
import logging


def create_app():
    """Create and configure the Flask application.
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max upload
    
    # Enable CORS
    CORS(app, origins=CORS_ORIGINS, supports_credentials=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize database
    with app.app_context():
        init_db()
    
    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.vocab_routes import vocab_bp
    from app.routes.csv_routes import csv_bp
    from app.routes.category_routes import category_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(vocab_bp, url_prefix='/api/vocab')
    app.register_blueprint(csv_bp, url_prefix='/api/csv')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    
    # Register error handlers
    from app.routes.error_handlers import register_error_handlers
    register_error_handlers(app)
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return {'status': 'healthy', 'message': 'Vocabulary Visualization API is running'}, 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
