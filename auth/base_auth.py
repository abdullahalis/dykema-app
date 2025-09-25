from abc import ABC, abstractmethod
from typing import Optional

class AuthManager(ABC):
    """Abstract base class for authentication managers."""

    @abstractmethod
    def get_user_id(self) -> Optional[str]:
        """Return the currently signed-in user's ID, or None if not signed in."""
        pass

    @abstractmethod
    def sign_up(self, email: str, password: str) -> None:
        """Register a new user with the given email and password."""
        pass

    @abstractmethod
    def sign_in(self, email: str, password: str) -> None:
        """Sign in a user with the given email and password."""
        pass

    @abstractmethod
    def sign_out(self) -> None:
        """Sign out the current user."""
        pass
