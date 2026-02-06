"""Data Access Object for Session operations."""
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session as DBSession
from app.models.session import Session


class SessionDAO:
    """Data Access Object for session database operations.
    
    Provides CRUD operations and session management functionality.
    All methods require a database session to be passed in.
    """
    
    def __init__(self, db_session: DBSession):
        """Initialize the DAO with a database session.
        
        Args:
            db_session: SQLAlchemy database session
        """
        self.db = db_session
    
    def insert(self, session: Session) -> int:
        """Insert a new session into the database.
        
        Args:
            session: Session object to insert (id should be None)
        
        Returns:
            int: The ID of the newly created session
        
        Raises:
            IntegrityError: If unique constraint is violated (duplicate token)
            SQLAlchemyError: For other database errors
        """
        self.db.add(session)
        self.db.flush()  # Flush to get the ID without committing
        return session.id
    
    def find_by_token(self, token: str) -> Optional[Session]:
        """Find a session by its token.
        
        Args:
            token: Session token to search for
        
        Returns:
            Optional[Session]: The session if found, None otherwise
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(Session).filter(Session.token == token).first()
    
    def find_by_user(self, user_id: int) -> List[Session]:
        """Find all sessions for a specific user.
        
        Args:
            user_id: ID of the user
        
        Returns:
            List[Session]: List of sessions (empty if none found)
        
        Raises:
            SQLAlchemyError: For database errors
        """
        return self.db.query(Session).filter(Session.user_id == user_id).all()
    
    def find_active_by_user(self, user_id: int) -> List[Session]:
        """Find all active (non-expired) sessions for a specific user.
        
        Args:
            user_id: ID of the user
        
        Returns:
            List[Session]: List of active sessions (empty if none found)
        
        Raises:
            SQLAlchemyError: For database errors
        """
        now = datetime.utcnow()
        return self.db.query(Session).filter(
            Session.user_id == user_id,
            Session.expires_at > now
        ).all()
    
    def delete(self, session_id: int) -> bool:
        """Delete a session by ID.
        
        Args:
            session_id: ID of the session to delete
        
        Returns:
            bool: True if session was found and deleted, False if not found
        
        Raises:
            SQLAlchemyError: For database errors
        """
        session = self.db.query(Session).filter(Session.id == session_id).first()
        if not session:
            return False
        
        self.db.delete(session)
        self.db.flush()
        return True
    
    def delete_by_token(self, token: str) -> bool:
        """Delete a session by its token.
        
        Args:
            token: Session token
        
        Returns:
            bool: True if session was found and deleted, False if not found
        
        Raises:
            SQLAlchemyError: For database errors
        """
        session = self.db.query(Session).filter(Session.token == token).first()
        if not session:
            return False
        
        self.db.delete(session)
        self.db.flush()
        return True
    
    def delete_expired(self) -> int:
        """Delete all expired sessions from the database.
        
        Returns:
            int: Number of sessions deleted
        
        Raises:
            SQLAlchemyError: For database errors
        """
        now = datetime.utcnow()
        expired_sessions = self.db.query(Session).filter(Session.expires_at <= now).all()
        count = len(expired_sessions)
        
        for session in expired_sessions:
            self.db.delete(session)
        
        self.db.flush()
        return count
    
    def delete_by_user(self, user_id: int) -> int:
        """Delete all sessions for a specific user.
        
        Args:
            user_id: ID of the user
        
        Returns:
            int: Number of sessions deleted
        
        Raises:
            SQLAlchemyError: For database errors
        """
        sessions = self.db.query(Session).filter(Session.user_id == user_id).all()
        count = len(sessions)
        
        for session in sessions:
            self.db.delete(session)
        
        self.db.flush()
        return count
    
    def update_expiration(self, token: str, expires_at: datetime) -> bool:
        """Update the expiration time of a session.
        
        Args:
            token: Session token
            expires_at: New expiration datetime
        
        Returns:
            bool: True if session was found and updated, False if not found
        
        Raises:
            SQLAlchemyError: For database errors
        """
        session = self.db.query(Session).filter(Session.token == token).first()
        if not session:
            return False
        
        session.expires_at = expires_at
        self.db.flush()
        return True
