from config.services import supabase
import logging
from typing import Optional
from error.error_types import AuthError
from auth.base_auth import AuthManager

class SupabaseAuthManager(AuthManager):
    """Supabase implementation of AuthManager."""

    def __init__(self):
        self.supabase = supabase

    def get_user_id(self) -> Optional[str]:
        """Return the ID of the currently signed-in user."""
        try:
            response = self.supabase.auth.get_user()
            return response.user.id if response and response.user.id else None
        except Exception as e:
            logging.error("Auth error while getting user ID", exc_info=True)
            raise AuthError("Could not retrieve user ID.") from e

    def sign_up(self, email: str, password: str) -> None:
        try:
            response = self.supabase.auth.sign_up({"email": email, "password": password})
            if not response.user:
                raise AuthError("Sign-up failed: no user returned.")
        except Exception as e:
            logging.error("Auth error during sign-up", exc_info=True)
            raise AuthError("Sign-up failed. Please try again.") from e

    def sign_in(self, email: str, password: str) -> None:
        try:
            response = self.supabase.auth.sign_in_with_password({"email": email, "password": password})
            if not response.user:
                raise AuthError("Sign-in failed: no user returned.")
        except Exception as e:
            logging.error("Auth error during sign-in", exc_info=True)
            raise AuthError("Sign-in failed. Please try again.") from e

    def sign_out(self) -> None:
        try:
            self.supabase.auth.sign_out()
        except Exception as e:
            logging.error("Auth error during sign-out", exc_info=True)
            raise AuthError("Sign-out failed. Please try again.") from e
