"""
Elastic Beanstalk entry point
EB looks for 'application' variable in application.py
"""
from app.app import create_app

# Create Flask application
application = create_app()

if __name__ == '__main__':
    application.run()
