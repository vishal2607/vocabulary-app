"""Unit tests for Data Access Objects (DAOs)."""
import pytest
from datetime import datetime, timedelta
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.models.vocab_entry import VocabEntry
from app.models.category import Category
from app.models.session import Session
from app.dao.user_dao import UserDAO
from app.dao.vocabulary_dao import VocabularyDAO
from app.dao.category_dao import CategoryDAO
from app.dao.session_dao import SessionDAO


class TestUserDAO:
    """Test cases for UserDAO."""
    
    def test_insert_user(self, db_session):
        """Test inserting a new user."""
        dao = UserDAO(db_session)
        user = User(username="testuser", password_hash="hashed_password")
        
        user_id = dao.insert(user)
        db_session.commit()
        
        assert user_id is not None
        assert user.id == user_id
    
    def test_find_by_id(self, db_session):
        """Test finding a user by ID."""
        dao = UserDAO(db_session)
        user = User(username="testuser", password_hash="hashed_password")
        user_id = dao.insert(user)
        db_session.commit()
        
        found_user = dao.find_by_id(user_id)
        
        assert found_user is not None
        assert found_user.username == "testuser"
    
    def test_find_by_username(self, db_session):
        """Test finding a user by username."""
        dao = UserDAO(db_session)
        user = User(username="testuser", password_hash="hashed_password")
        dao.insert(user)
        db_session.commit()
        
        found_user = dao.find_by_username("testuser")
        
        assert found_user is not None
        assert found_user.username == "testuser"
    
    def test_find_by_username_not_found(self, db_session):
        """Test finding a non-existent user returns None."""
        dao = UserDAO(db_session)
        
        found_user = dao.find_by_username("nonexistent")
        
        assert found_user is None
    
    def test_update_user(self, db_session):
        """Test updating user fields."""
        dao = UserDAO(db_session)
        user = User(username="testuser", password_hash="old_hash")
        user_id = dao.insert(user)
        db_session.commit()
        
        result = dao.update(user_id, {"password_hash": "new_hash"})
        db_session.commit()
        
        assert result is True
        updated_user = dao.find_by_id(user_id)
        assert updated_user.password_hash == "new_hash"
    
    def test_delete_user(self, db_session):
        """Test deleting a user."""
        dao = UserDAO(db_session)
        user = User(username="testuser", password_hash="hashed_password")
        user_id = dao.insert(user)
        db_session.commit()
        
        result = dao.delete(user_id)
        db_session.commit()
        
        assert result is True
        assert dao.find_by_id(user_id) is None
    
    def test_exists(self, db_session):
        """Test checking if a user exists."""
        dao = UserDAO(db_session)
        user = User(username="testuser", password_hash="hashed_password")
        dao.insert(user)
        db_session.commit()
        
        assert dao.exists("testuser") is True
        assert dao.exists("nonexistent") is False
    
    def test_duplicate_username_raises_error(self, db_session):
        """Test that duplicate usernames raise IntegrityError."""
        dao = UserDAO(db_session)
        user1 = User(username="testuser", password_hash="hash1")
        dao.insert(user1)
        db_session.commit()
        
        user2 = User(username="testuser", password_hash="hash2")
        
        with pytest.raises(IntegrityError):
            dao.insert(user2)


class TestVocabularyDAO:
    """Test cases for VocabularyDAO."""
    
    def test_insert_entry(self, db_session, test_user):
        """Test inserting a vocabulary entry."""
        dao = VocabularyDAO(db_session)
        entry = VocabEntry(
            user_id=test_user.id,
            word="test",
            meaning="a test word"
        )
        
        entry_id = dao.insert(entry)
        db_session.commit()
        
        assert entry_id is not None
        assert entry.id == entry_id
    
    def test_find_by_id(self, db_session, test_user):
        """Test finding an entry by ID."""
        dao = VocabularyDAO(db_session)
        entry = VocabEntry(user_id=test_user.id, word="test", meaning="a test word")
        entry_id = dao.insert(entry)
        db_session.commit()
        
        found_entry = dao.find_by_id(entry_id)
        
        assert found_entry is not None
        assert found_entry.word == "test"
    
    def test_find_by_user(self, db_session, test_user):
        """Test finding all entries for a user."""
        dao = VocabularyDAO(db_session)
        entry1 = VocabEntry(user_id=test_user.id, word="test1", meaning="meaning1")
        entry2 = VocabEntry(user_id=test_user.id, word="test2", meaning="meaning2")
        dao.insert(entry1)
        dao.insert(entry2)
        db_session.commit()
        
        entries = dao.find_by_user(test_user.id)
        
        assert len(entries) == 2
        assert {e.word for e in entries} == {"test1", "test2"}
    
    def test_update_entry(self, db_session, test_user):
        """Test updating entry fields."""
        dao = VocabularyDAO(db_session)
        entry = VocabEntry(user_id=test_user.id, word="test", meaning="old meaning")
        entry_id = dao.insert(entry)
        db_session.commit()
        
        result = dao.update(entry_id, {"meaning": "new meaning", "synonym": "exam"})
        db_session.commit()
        
        assert result is True
        updated_entry = dao.find_by_id(entry_id)
        assert updated_entry.meaning == "new meaning"
        assert updated_entry.synonym == "exam"
    
    def test_delete_entry(self, db_session, test_user):
        """Test deleting an entry."""
        dao = VocabularyDAO(db_session)
        entry = VocabEntry(user_id=test_user.id, word="test", meaning="meaning")
        entry_id = dao.insert(entry)
        db_session.commit()
        
        result = dao.delete(entry_id)
        db_session.commit()
        
        assert result is True
        assert dao.find_by_id(entry_id) is None
    
    def test_search_entries(self, db_session, test_user):
        """Test searching entries across all fields."""
        dao = VocabularyDAO(db_session)
        entry1 = VocabEntry(user_id=test_user.id, word="apple", meaning="a fruit")
        entry2 = VocabEntry(user_id=test_user.id, word="banana", meaning="yellow fruit")
        entry3 = VocabEntry(user_id=test_user.id, word="carrot", meaning="a vegetable")
        dao.insert(entry1)
        dao.insert(entry2)
        dao.insert(entry3)
        db_session.commit()
        
        # Search for "fruit" should return 2 entries
        results = dao.search(test_user.id, "fruit")
        assert len(results) == 2
        
        # Search for "apple" should return 1 entry
        results = dao.search(test_user.id, "apple")
        assert len(results) == 1
        assert results[0].word == "apple"
    
    def test_search_case_insensitive(self, db_session, test_user):
        """Test that search is case-insensitive."""
        dao = VocabularyDAO(db_session)
        entry = VocabEntry(user_id=test_user.id, word="Apple", meaning="A Fruit")
        dao.insert(entry)
        db_session.commit()
        
        results = dao.search(test_user.id, "apple")
        assert len(results) == 1
        
        results = dao.search(test_user.id, "FRUIT")
        assert len(results) == 1
    
    def test_search_empty_query_returns_all(self, db_session, test_user):
        """Test that empty search query returns all entries."""
        dao = VocabularyDAO(db_session)
        entry1 = VocabEntry(user_id=test_user.id, word="test1", meaning="meaning1")
        entry2 = VocabEntry(user_id=test_user.id, word="test2", meaning="meaning2")
        dao.insert(entry1)
        dao.insert(entry2)
        db_session.commit()
        
        results = dao.search(test_user.id, "")
        assert len(results) == 2
    
    def test_find_by_category(self, db_session, test_user, test_category):
        """Test finding entries by category."""
        dao = VocabularyDAO(db_session)
        entry1 = VocabEntry(user_id=test_user.id, word="test1", meaning="m1", category_id=test_category.id)
        entry2 = VocabEntry(user_id=test_user.id, word="test2", meaning="m2", category_id=test_category.id)
        entry3 = VocabEntry(user_id=test_user.id, word="test3", meaning="m3", category_id=None)
        dao.insert(entry1)
        dao.insert(entry2)
        dao.insert(entry3)
        db_session.commit()
        
        # Find entries in category
        results = dao.find_by_category(test_user.id, test_category.id)
        assert len(results) == 2
        
        # Find uncategorized entries
        results = dao.find_by_category(test_user.id, None)
        assert len(results) == 1
    
    def test_find_by_word(self, db_session, test_user):
        """Test finding an entry by exact word match."""
        dao = VocabularyDAO(db_session)
        entry = VocabEntry(user_id=test_user.id, word="test", meaning="meaning")
        dao.insert(entry)
        db_session.commit()
        
        found = dao.find_by_word(test_user.id, "test")
        assert found is not None
        assert found.word == "test"
        
        not_found = dao.find_by_word(test_user.id, "nonexistent")
        assert not_found is None
    
    def test_duplicate_word_per_user_raises_error(self, db_session, test_user):
        """Test that duplicate words for same user raise IntegrityError."""
        dao = VocabularyDAO(db_session)
        entry1 = VocabEntry(user_id=test_user.id, word="test", meaning="meaning1")
        dao.insert(entry1)
        db_session.commit()
        
        entry2 = VocabEntry(user_id=test_user.id, word="test", meaning="meaning2")
        
        with pytest.raises(IntegrityError):
            dao.insert(entry2)


class TestCategoryDAO:
    """Test cases for CategoryDAO."""
    
    def test_insert_category(self, db_session, test_user):
        """Test inserting a category."""
        dao = CategoryDAO(db_session)
        category = Category(user_id=test_user.id, name="Test Category")
        
        category_id = dao.insert(category)
        db_session.commit()
        
        assert category_id is not None
        assert category.id == category_id
    
    def test_find_by_id(self, db_session, test_user):
        """Test finding a category by ID."""
        dao = CategoryDAO(db_session)
        category = Category(user_id=test_user.id, name="Test Category")
        category_id = dao.insert(category)
        db_session.commit()
        
        found_category = dao.find_by_id(category_id)
        
        assert found_category is not None
        assert found_category.name == "Test Category"
    
    def test_find_by_user(self, db_session, test_user):
        """Test finding all categories for a user."""
        dao = CategoryDAO(db_session)
        cat1 = Category(user_id=test_user.id, name="Category 1")
        cat2 = Category(user_id=test_user.id, name="Category 2")
        dao.insert(cat1)
        dao.insert(cat2)
        db_session.commit()
        
        categories = dao.find_by_user(test_user.id)
        
        assert len(categories) == 2
        assert {c.name for c in categories} == {"Category 1", "Category 2"}
    
    def test_find_by_name(self, db_session, test_user):
        """Test finding a category by name."""
        dao = CategoryDAO(db_session)
        category = Category(user_id=test_user.id, name="Test Category")
        dao.insert(category)
        db_session.commit()
        
        found = dao.find_by_name(test_user.id, "Test Category")
        
        assert found is not None
        assert found.name == "Test Category"
    
    def test_update_category(self, db_session, test_user):
        """Test updating category fields."""
        dao = CategoryDAO(db_session)
        category = Category(user_id=test_user.id, name="Old Name")
        category_id = dao.insert(category)
        db_session.commit()
        
        result = dao.update(category_id, {"name": "New Name"})
        db_session.commit()
        
        assert result is True
        updated_category = dao.find_by_id(category_id)
        assert updated_category.name == "New Name"
    
    def test_delete_category(self, db_session, test_user):
        """Test deleting a category."""
        dao = CategoryDAO(db_session)
        category = Category(user_id=test_user.id, name="Test Category")
        category_id = dao.insert(category)
        db_session.commit()
        
        result = dao.delete(category_id)
        db_session.commit()
        
        assert result is True
        assert dao.find_by_id(category_id) is None
    
    def test_exists(self, db_session, test_user):
        """Test checking if a category exists."""
        dao = CategoryDAO(db_session)
        category = Category(user_id=test_user.id, name="Test Category")
        dao.insert(category)
        db_session.commit()
        
        assert dao.exists(test_user.id, "Test Category") is True
        assert dao.exists(test_user.id, "Nonexistent") is False
    
    def test_duplicate_category_name_per_user_raises_error(self, db_session, test_user):
        """Test that duplicate category names for same user raise IntegrityError."""
        dao = CategoryDAO(db_session)
        cat1 = Category(user_id=test_user.id, name="Test")
        dao.insert(cat1)
        db_session.commit()
        
        cat2 = Category(user_id=test_user.id, name="Test")
        
        with pytest.raises(IntegrityError):
            dao.insert(cat2)


class TestSessionDAO:
    """Test cases for SessionDAO."""
    
    def test_insert_session(self, db_session, test_user):
        """Test inserting a session."""
        dao = SessionDAO(db_session)
        token = Session.generate_token()
        session = Session(
            user_id=test_user.id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        
        session_id = dao.insert(session)
        db_session.commit()
        
        assert session_id is not None
        assert session.id == session_id
    
    def test_find_by_token(self, db_session, test_user):
        """Test finding a session by token."""
        dao = SessionDAO(db_session)
        token = Session.generate_token()
        session = Session(
            user_id=test_user.id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        dao.insert(session)
        db_session.commit()
        
        found_session = dao.find_by_token(token)
        
        assert found_session is not None
        assert found_session.token == token
    
    def test_find_by_user(self, db_session, test_user):
        """Test finding all sessions for a user."""
        dao = SessionDAO(db_session)
        token1 = Session.generate_token()
        token2 = Session.generate_token()
        session1 = Session(user_id=test_user.id, token=token1, expires_at=datetime.utcnow() + timedelta(hours=24))
        session2 = Session(user_id=test_user.id, token=token2, expires_at=datetime.utcnow() + timedelta(hours=24))
        dao.insert(session1)
        dao.insert(session2)
        db_session.commit()
        
        sessions = dao.find_by_user(test_user.id)
        
        assert len(sessions) == 2
    
    def test_find_active_by_user(self, db_session, test_user):
        """Test finding only active sessions for a user."""
        dao = SessionDAO(db_session)
        
        # Create active session
        active_token = Session.generate_token()
        active_session = Session(
            user_id=test_user.id,
            token=active_token,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        
        # Create expired session
        expired_token = Session.generate_token()
        expired_session = Session(
            user_id=test_user.id,
            token=expired_token,
            expires_at=datetime.utcnow() - timedelta(hours=1)
        )
        
        dao.insert(active_session)
        dao.insert(expired_session)
        db_session.commit()
        
        active_sessions = dao.find_active_by_user(test_user.id)
        
        assert len(active_sessions) == 1
        assert active_sessions[0].token == active_token
    
    def test_delete_by_token(self, db_session, test_user):
        """Test deleting a session by token."""
        dao = SessionDAO(db_session)
        token = Session.generate_token()
        session = Session(user_id=test_user.id, token=token, expires_at=datetime.utcnow() + timedelta(hours=24))
        dao.insert(session)
        db_session.commit()
        
        result = dao.delete_by_token(token)
        db_session.commit()
        
        assert result is True
        assert dao.find_by_token(token) is None
    
    def test_delete_expired(self, db_session, test_user):
        """Test deleting all expired sessions."""
        dao = SessionDAO(db_session)
        
        # Create expired sessions
        for i in range(3):
            token = Session.generate_token()
            session = Session(
                user_id=test_user.id,
                token=token,
                expires_at=datetime.utcnow() - timedelta(hours=1)
            )
            dao.insert(session)
        
        # Create active session
        active_token = Session.generate_token()
        active_session = Session(
            user_id=test_user.id,
            token=active_token,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        dao.insert(active_session)
        db_session.commit()
        
        deleted_count = dao.delete_expired()
        db_session.commit()
        
        assert deleted_count == 3
        remaining_sessions = dao.find_by_user(test_user.id)
        assert len(remaining_sessions) == 1
    
    def test_delete_by_user(self, db_session, test_user):
        """Test deleting all sessions for a user."""
        dao = SessionDAO(db_session)
        
        for i in range(3):
            token = Session.generate_token()
            session = Session(user_id=test_user.id, token=token, expires_at=datetime.utcnow() + timedelta(hours=24))
            dao.insert(session)
        db_session.commit()
        
        deleted_count = dao.delete_by_user(test_user.id)
        db_session.commit()
        
        assert deleted_count == 3
        assert len(dao.find_by_user(test_user.id)) == 0
    
    def test_update_expiration(self, db_session, test_user):
        """Test updating session expiration time."""
        dao = SessionDAO(db_session)
        token = Session.generate_token()
        old_expiration = datetime.utcnow() + timedelta(hours=1)
        session = Session(user_id=test_user.id, token=token, expires_at=old_expiration)
        dao.insert(session)
        db_session.commit()
        
        new_expiration = datetime.utcnow() + timedelta(hours=48)
        result = dao.update_expiration(token, new_expiration)
        db_session.commit()
        
        assert result is True
        updated_session = dao.find_by_token(token)
        assert updated_session.expires_at == new_expiration
