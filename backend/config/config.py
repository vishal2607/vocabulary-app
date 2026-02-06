"""Application configuration."""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Database configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', str(BASE_DIR / 'data' / 'vocabulary.db'))
SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Security configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
BCRYPT_LOG_ROUNDS = int(os.getenv('BCRYPT_LOG_ROUNDS', '12'))

# Session configuration
SESSION_DURATION_HOURS = int(os.getenv('SESSION_DURATION_HOURS', '24'))
REMEMBER_ME_DURATION_DAYS = int(os.getenv('REMEMBER_ME_DURATION_DAYS', '30'))

# CORS configuration
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173').split(',')

# File upload configuration
MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', str(10 * 1024 * 1024)))  # 10MB default
ALLOWED_EXTENSIONS = {'csv', 'txt'}

# Query performance
QUERY_TIMEOUT_MS = int(os.getenv('QUERY_TIMEOUT_MS', '500'))
