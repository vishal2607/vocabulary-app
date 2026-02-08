"""
Elastic Beanstalk entry point
EB looks for 'application' variable in application.py
"""
import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from app.app import create_app

# Create Flask application
application = create_app()

if __name__ == '__main__':
    application.run()
