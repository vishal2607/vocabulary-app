"""Unit tests for database models."""
import pytest
from datetime import datetime, timedelta
from app.models import User, VocabEntry, Category, Session
from app.database import init_db, reset_db, SessionLocal


@pytest.fixture(scope='function')
def db_session():
    """Create a fresh database session for each test."""
    reset_db()
    session = SessionLocal()
    yield session
    session.close()


class TestUserModel:
    """Tests for User model."""
    
    def test_create_user(self, db_session):
        """Test creating a user."""
        user = User(
            username='testuser',
            password_hash='hashed_password_123'
        )
        db_session.add(user)
        db_session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.password_hash == 'hashed_password_123'
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)
    
    def test_user_unique_username(self, db_session):
        """Test that usernames must be unique."""
        user1 = User(username='testuser', password_hash='hash1')
        user2 = User(username='testuser', password_hash='hash2')
        
        db_session.add(user1)
        db_session.commit()
        
        db_session.add(user2)
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()


class TestVocabEntryModel:
    """Tests for VocabEntry model."""
    
    def test_create_vocab_entry(self, db_session):
        """Test creating a vocabulary entry."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        entry = VocabEntry(
            user_id=user.id,
            word='hello',
            meaning='a greeting',
            synonym='hi',
            pronunciation='heh-loh',
            example='Hello, how are you?'
        )
        db_session.add(entry)
        db_session.commit()
        
        assert entry.id is not None
        assert entry.word == 'hello'
        assert entry.meaning == 'a greeting'
        assert entry.synonym == 'hi'
        assert entry.pronunciation == 'heh-loh'
        assert entry.example == 'Hello, how are you?'
        assert entry.created_at is not None
        assert entry.updated_at is not None
    
    def test_vocab_entry_validation(self, db_session):
        """Test vocabulary entry validation."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        # Valid entry
        valid_entry = VocabEntry(
            user_id=user.id,
            word='test',
            meaning='a test'
        )
        assert valid_entry.validate() == []
        
        # Empty word
        empty_word = VocabEntry(
            user_id=user.id,
            word='',
            meaning='a test'
        )
        errors = empty_word.validate()
        assert len(errors) > 0
        assert any('word' in err.lower() for err in errors)
        
        # Empty meaning
        empty_meaning = VocabEntry(
            user_id=user.id,
            word='test',
            meaning=''
        )
        errors = empty_meaning.validate()
        assert len(errors) > 0
        assert any('meaning' in err.lower() for err in errors)
        
        # Word too long
        long_word = VocabEntry(
            user_id=user.id,
            word='a' * 101,
            meaning='a test'
        )
        errors = long_word.validate()
        assert len(errors) > 0
        assert any('100 characters' in err for err in errors)
    
    def test_vocab_entry_unique_per_user(self, db_session):
        """Test that words must be unique per user."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        entry1 = VocabEntry(user_id=user.id, word='hello', meaning='greeting 1')
        entry2 = VocabEntry(user_id=user.id, word='hello', meaning='greeting 2')
        
        db_session.add(entry1)
        db_session.commit()
        
        db_session.add(entry2)
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()
    
    def test_vocab_entry_cascade_delete(self, db_session):
        """Test that deleting a user deletes their vocab entries."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        entry = VocabEntry(user_id=user.id, word='hello', meaning='greeting')
        db_session.add(entry)
        db_session.commit()
        
        entry_id = entry.id
        
        # Delete user
        db_session.delete(user)
        db_session.commit()
        
        # Entry should be deleted
        deleted_entry = db_session.query(VocabEntry).filter_by(id=entry_id).first()
        assert deleted_entry is None
    
    def test_vocab_entry_to_dict(self, db_session):
        """Test converting vocab entry to dictionary."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        entry = VocabEntry(
            user_id=user.id,
            word='hello',
            meaning='a greeting'
        )
        db_session.add(entry)
        db_session.commit()
        
        entry_dict = entry.to_dict()
        assert entry_dict['id'] == entry.id
        assert entry_dict['user_id'] == user.id
        assert entry_dict['word'] == 'hello'
        assert entry_dict['meaning'] == 'a greeting'
        assert 'created_at' in entry_dict
        assert 'updated_at' in entry_dict


class TestCategoryModel:
    """Tests for Category model."""
    
    def test_create_category(self, db_session):
        """Test creating a category."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        category = Category(
            user_id=user.id,
            name='Animals'
        )
        db_session.add(category)
        db_session.commit()
        
        assert category.id is not None
        assert category.name == 'Animals'
        assert category.user_id == user.id
        assert category.created_at is not None
    
    def test_category_unique_per_user(self, db_session):
        """Test that category names must be unique per user."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        cat1 = Category(user_id=user.id, name='Animals')
        cat2 = Category(user_id=user.id, name='Animals')
        
        db_session.add(cat1)
        db_session.commit()
        
        db_session.add(cat2)
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()
    
    def test_category_cascade_delete(self, db_session):
        """Test that deleting a user deletes their categories."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        category = Category(user_id=user.id, name='Animals')
        db_session.add(category)
        db_session.commit()
        
        category_id = category.id
        
        # Delete user
        db_session.delete(user)
        db_session.commit()
        
        # Category should be deleted
        deleted_cat = db_session.query(Category).filter_by(id=category_id).first()
        assert deleted_cat is None
    
    def test_category_set_null_on_delete(self, db_session):
        """Test that deleting a category sets vocab entries category_id to NULL."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        category = Category(user_id=user.id, name='Animals')
        db_session.add(category)
        db_session.commit()
        
        entry = VocabEntry(
            user_id=user.id,
            word='cat',
            meaning='a feline animal',
            category_id=category.id
        )
        db_session.add(entry)
        db_session.commit()
        
        entry_id = entry.id
        
        # Delete category
        db_session.delete(category)
        db_session.commit()
        
        # Entry should still exist but category_id should be NULL
        updated_entry = db_session.query(VocabEntry).filter_by(id=entry_id).first()
        assert updated_entry is not None
        assert updated_entry.category_id is None


class TestSessionModel:
    """Tests for Session model."""
    
    def test_create_session(self, db_session):
        """Test creating a session."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        token = Session.generate_token()
        session = Session(
            user_id=user.id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        db_session.add(session)
        db_session.commit()
        
        assert session.id is not None
        assert session.user_id == user.id
        assert session.token == token
        assert session.expires_at is not None
        assert session.created_at is not None
    
    def test_generate_token(self):
        """Test token generation."""
        token1 = Session.generate_token()
        token2 = Session.generate_token()
        
        assert len(token1) > 0
        assert len(token2) > 0
        assert token1 != token2  # Should be unique
    
    def test_is_expired(self, db_session):
        """Test session expiration check."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        # Not expired
        valid_session = Session(
            user_id=user.id,
            token=Session.generate_token(),
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        assert not valid_session.is_expired()
        
        # Expired
        expired_session = Session(
            user_id=user.id,
            token=Session.generate_token(),
            expires_at=datetime.utcnow() - timedelta(hours=1)
        )
        assert expired_session.is_expired()
    
    def test_extend_expiration(self, db_session):
        """Test extending session expiration."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        session = Session(
            user_id=user.id,
            token=Session.generate_token(),
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )
        
        old_expiration = session.expires_at
        session.extend_expiration(hours=24)
        
        assert session.expires_at > old_expiration
        # Should be approximately 24 hours from now
        time_diff = session.expires_at - datetime.utcnow()
        assert 23 <= time_diff.total_seconds() / 3600 <= 25  # Allow some margin
    
    def test_session_cascade_delete(self, db_session):
        """Test that deleting a user deletes their sessions."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        session = Session(
            user_id=user.id,
            token=Session.generate_token(),
            expires_at=datetime.utcnow() + timedelta(hours=24)
        )
        db_session.add(session)
        db_session.commit()
        
        session_id = session.id
        
        # Delete user
        db_session.delete(user)
        db_session.commit()
        
        # Session should be deleted
        deleted_session = db_session.query(Session).filter_by(id=session_id).first()
        assert deleted_session is None


class TestRelationships:
    """Tests for model relationships."""
    
    def test_user_vocab_entries_relationship(self, db_session):
        """Test User to VocabEntry relationship."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        entry1 = VocabEntry(user_id=user.id, word='hello', meaning='greeting')
        entry2 = VocabEntry(user_id=user.id, word='goodbye', meaning='farewell')
        db_session.add_all([entry1, entry2])
        db_session.commit()
        
        # Access entries through relationship
        assert user.vocab_entries.count() == 2
        words = [e.word for e in user.vocab_entries.all()]
        assert 'hello' in words
        assert 'goodbye' in words
    
    def test_user_categories_relationship(self, db_session):
        """Test User to Category relationship."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        cat1 = Category(user_id=user.id, name='Animals')
        cat2 = Category(user_id=user.id, name='Plants')
        db_session.add_all([cat1, cat2])
        db_session.commit()
        
        # Access categories through relationship
        assert user.categories.count() == 2
        names = [c.name for c in user.categories.all()]
        assert 'Animals' in names
        assert 'Plants' in names
    
    def test_category_vocab_entries_relationship(self, db_session):
        """Test Category to VocabEntry relationship."""
        user = User(username='testuser', password_hash='hash')
        db_session.add(user)
        db_session.commit()
        
        category = Category(user_id=user.id, name='Animals')
        db_session.add(category)
        db_session.commit()
        
        entry1 = VocabEntry(
            user_id=user.id,
            word='cat',
            meaning='feline',
            category_id=category.id
        )
        entry2 = VocabEntry(
            user_id=user.id,
            word='dog',
            meaning='canine',
            category_id=category.id
        )
        db_session.add_all([entry1, entry2])
        db_session.commit()
        
        # Access entries through category relationship
        assert category.vocab_entries.count() == 2
        words = [e.word for e in category.vocab_entries.all()]
        assert 'cat' in words
        assert 'dog' in words
