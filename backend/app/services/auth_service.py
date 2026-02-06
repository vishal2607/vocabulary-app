"""Authentication service for user registration, login, and session management."""
from typing import Optional, Tuple
from datetime import datetime, timedelta
import bcrypt
from sqlalchemy.orm import Session as DBSession
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.models.session import Session
from app.dao.user_dao import UserDAO
from app.dao.session_dao import SessionDAO


class AuthenticationError(Exception):
    """Exception raised for authentication failures."""
    pass


class RegistrationError(Exception):
    """Exception raised for registration failures."""
    pass


class AuthService:
    """Service for handling user authentication and session management.
    
    This service provides methods for:
    - User registration with password hashing
    - User authentication with password verification
    - Session creation and management
    - Session validation and expiration
    - User logout
    
    All password operations use bcrypt for secure hashing.
    """
    
    # Session duration constants
    DEFAULT_SESSION_HOURS = 24
    REMEMBER_ME_SESSION_DAYS = 30
    
    def __init__(self, db_session: DBSession):
        """Initialize the authentication service.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
        self.user_dao = UserDAO(db_session)
        self.session_dao = SessionDAO(db_session)
    
    def register_user(self, username: str, password: str) -> User:
        """Register a new user with hashed password.
        
        This method:
        1. Validates username and password
        2. Checks if username already exists
        3. Hashes the password using bcrypt
        4. Creates and stores the user
        
        Args:
            username: Desired username (must be unique, 1-50 characters)
            password: Plain text password (minimum 8 characters recommended)
        
        Returns:
            User: The newly created user object
        
        Raises:
            RegistrationError: If username is invalid, already exists, or password is invalid
            SQLAlchemyError: For database errors
        """
        # Validate username
        if not username or not username.strip():
            raise RegistrationError("Username cannot be empty")
        
        username = username.strip()
        
        if len(username) > 50:
            raise RegistrationError("Username cannot exceed 50 characters")
        
        # Validate password
        if not password:
            raise RegistrationError("Password cannot be empty")
        
        if len(password) < 8:
            raise RegistrationError("Password must be at least 8 characters")
        
        # Check if username already exists
        if self.user_dao.exists(username):
            raise RegistrationError(f"Username '{username}' already exists")
        
        # Hash the password
        password_hash = self._hash_password(password)
        
        # Create user object
        user = User(
            username=username,
            password_hash=password_hash
        )
        
        # Insert into database
        try:
            user_id = self.user_dao.insert(user)
            self.db.commit()
            
            # Refresh to get the created_at timestamp
            user = self.user_dao.find_by_id(user_id)
            return user
        except IntegrityError as e:
            self.db.rollback()
            raise RegistrationError(f"Failed to register user: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise
    
    def authenticate(self, username: str, password: str) -> User:
        """Authenticate a user with username and password.
        
        This method:
        1. Looks up the user by username
        2. Verifies the password against the stored hash
        3. Returns the user if authentication succeeds
        
        Args:
            username: Username to authenticate
            password: Plain text password to verify
        
        Returns:
            User: The authenticated user object
        
        Raises:
            AuthenticationError: If credentials are invalid (generic message for security)
        """
        # Validate inputs
        if not username or not password:
            raise AuthenticationError("Invalid credentials")
        
        # Find user by username
        user = self.user_dao.find_by_username(username.strip())
        
        if not user:
            # Use generic error message to prevent username enumeration
            raise AuthenticationError("Invalid credentials")
        
        # Verify password
        if not self._verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid credentials")
        
        return user
    
    def create_session(self, user_id: int, remember: bool = False) -> Session:
        """Create a new session for an authenticated user.
        
        This method:
        1. Generates a secure random session token
        2. Sets expiration time based on remember flag
        3. Creates and stores the session
        
        Args:
            user_id: ID of the authenticated user
            remember: If True, extends session duration (30 days vs 24 hours)
        
        Returns:
            Session: The newly created session object
        
        Raises:
            ValueError: If user_id is invalid
            SQLAlchemyError: For database errors
        """
        # Validate user exists
        user = self.user_dao.find_by_id(user_id)
        if not user:
            raise ValueError(f"User with ID {user_id} not found")
        
        # Generate secure token
        token = Session.generate_token()
        
        # Calculate expiration time
        if remember:
            expires_at = datetime.utcnow() + timedelta(days=self.REMEMBER_ME_SESSION_DAYS)
        else:
            expires_at = datetime.utcnow() + timedelta(hours=self.DEFAULT_SESSION_HOURS)
        
        # Create session object
        session = Session(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        
        # Insert into database
        try:
            session_id = self.session_dao.insert(session)
            self.db.commit()
            
            # Refresh to get the created_at timestamp
            session = self.session_dao.find_by_token(token)
            return session
        except Exception as e:
            self.db.rollback()
            raise
    
    def validate_session(self, session_token: str) -> Tuple[bool, Optional[User]]:
        """Validate a session token and return the associated user.
        
        This method:
        1. Looks up the session by token
        2. Checks if the session has expired
        3. Optionally extends the session expiration (activity-based extension)
        4. Returns the user if session is valid
        
        Args:
            session_token: Session token to validate
        
        Returns:
            Tuple[bool, Optional[User]]: (is_valid, user)
                - is_valid: True if session is valid and not expired
                - user: The user object if valid, None otherwise
        """
        if not session_token:
            return False, None
        
        # Find session by token
        session = self.session_dao.find_by_token(session_token)
        
        if not session:
            return False, None
        
        # Check if session has expired
        if session.is_expired():
            # Clean up expired session
            try:
                self.session_dao.delete(session.id)
                self.db.commit()
            except Exception:
                self.db.rollback()
            return False, None
        
        # Get the user
        user = self.user_dao.find_by_id(session.user_id)
        
        if not user:
            return False, None
        
        # Extend session expiration on activity (implements session activity extension)
        try:
            session.extend_expiration(hours=self.DEFAULT_SESSION_HOURS)
            self.db.commit()
        except Exception:
            # If extension fails, still return valid session
            # The session is still valid, just not extended
            self.db.rollback()
        
        return True, user
    
    def logout(self, session_token: str) -> bool:
        """Terminate a user session (logout).
        
        This method:
        1. Looks up the session by token
        2. Deletes the session from the database
        3. Returns success status
        
        Args:
            session_token: Session token to terminate
        
        Returns:
            bool: True if session was found and deleted, False if not found
        
        Raises:
            SQLAlchemyError: For database errors
        """
        if not session_token:
            return False
        
        try:
            deleted = self.session_dao.delete_by_token(session_token)
            self.db.commit()
            return deleted
        except Exception as e:
            self.db.rollback()
            raise
    
    def logout_all_sessions(self, user_id: int) -> int:
        """Terminate all sessions for a specific user.
        
        Useful for "logout from all devices" functionality or security purposes.
        
        Args:
            user_id: ID of the user whose sessions should be terminated
        
        Returns:
            int: Number of sessions terminated
        
        Raises:
            SQLAlchemyError: For database errors
        """
        try:
            count = self.session_dao.delete_by_user(user_id)
            self.db.commit()
            return count
        except Exception as e:
            self.db.rollback()
            raise
    
    def cleanup_expired_sessions(self) -> int:
        """Remove all expired sessions from the database.
        
        This is a maintenance method that should be called periodically
        (e.g., via a scheduled task) to clean up expired sessions.
        
        Returns:
            int: Number of expired sessions removed
        
        Raises:
            SQLAlchemyError: For database errors
        """
        try:
            count = self.session_dao.delete_expired()
            self.db.commit()
            return count
        except Exception as e:
            self.db.rollback()
            raise
    
    # Private helper methods
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using bcrypt.
        
        Args:
            password: Plain text password
        
        Returns:
            str: Bcrypt hashed password
        """
        # Generate salt and hash password
        salt = bcrypt.gensalt()
        password_bytes = password.encode('utf-8')
        hashed = bcrypt.hashpw(password_bytes, salt)
        
        # Return as string
        return hashed.decode('utf-8')
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against a bcrypt hash.
        
        Args:
            password: Plain text password to verify
            password_hash: Bcrypt hash to verify against
        
        Returns:
            bool: True if password matches hash, False otherwise
        """
        try:
            password_bytes = password.encode('utf-8')
            hash_bytes = password_hash.encode('utf-8')
            return bcrypt.checkpw(password_bytes, hash_bytes)
        except Exception:
            # If verification fails for any reason, return False
            return False
