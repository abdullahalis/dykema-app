import pytest
import random
import logging
import warnings
from auth.supabase_auth import SupabaseAuthManager
from storage.backend.supabase_backend import SupabaseBackend
from error.error_types import AuthError, StorageError

# Suppress unnecessary warnings
logging.disable(logging.CRITICAL)
warnings.simplefilter("ignore", ResourceWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

@pytest.fixture
def auth_manager():
    auth = SupabaseAuthManager()
    yield auth
    try:
        auth.sign_out()
    except AuthError:
        pass  # ignore if already signed out

@pytest.fixture
def backend():
    return SupabaseBackend()

@pytest.fixture
def test_credentials():
    return {
        "email": "abdullahalisye@gmail.com",
        "password": "password"
    }

def test_invalid_get_id(auth_manager):
    assert auth_manager.get_user_id() is None

def test_invalid_sign_in(auth_manager):
    with pytest.raises(AuthError):
        auth_manager.sign_in("a", "b")

def test_invalid_sign_up(auth_manager):
    with pytest.raises(AuthError):
        auth_manager.sign_up("", "")

def test_valid_sign_in_and_get_id(auth_manager, test_credentials):
    auth_manager.sign_in(test_credentials["email"], test_credentials["password"])
    user_id = auth_manager.get_user_id()
    assert user_id is not None

def test_valid_sign_out(auth_manager, test_credentials):
    auth_manager.sign_in(test_credentials["email"], test_credentials["password"])
    auth_manager.sign_out()
    assert auth_manager.get_user_id() is None

def test_valid_sign_up(auth_manager):
    unique_email = f"testuser{random.randint(1000,9999)}@example.com"
    auth_manager.sign_up(unique_email, "testpassword")
    user_id = auth_manager.get_user_id()
    assert user_id is not None

def test_row_level_security(auth_manager, backend, test_credentials):
    auth_manager.sign_in(test_credentials["email"], test_credentials["password"])
    user1_id = auth_manager.get_user_id()
    auth_manager.sign_out()
    auth_manager.sign_in("example@gmail.com", "password")
    # This should raise StorageError or return empty list depending on your backend implementation
    assert backend.get_conversations(user1_id) == []
