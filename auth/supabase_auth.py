from config.services import supabase
import logging
from error_types import AuthError
from auth.base_auth import AuthManager

class SupabaseAuthManager(AuthManager):
    def __init__(self):
        self.supabase = supabase

    def get_user_id(self):
        try:
            response = self.supabase.auth.get_user()
            return response.user.id
        except Exception as e:
            logging.error(f"Auth error: {e}", exc_info=True)
            raise AuthError("Could not retrieve user ID.")
            
    def sign_up(self, email, password):
        try:
            response = self.supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password
                }
            )
            if not response.user:
                raise AuthError("Sign up failed: no user returned.")
        except Exception as e:
            logging.error(f"Auth error: {e}", exc_info=True)
            raise AuthError(f"Sign up failed. Please try again.")
    
    def sign_in(self, email, password):
        try:
            response = self.supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password
                }
            )
            if not response.user:
                raise AuthError("Sign in failed: no user returned.")
        except Exception as e:
            logging.error(f"Auth error: {e}", exc_info=True)
            raise AuthError(f"Sign in failed. Please try again")

    def sign_out(self):
        try:
            self.supabase.auth.sign_out()
        except Exception as e:
            logging.error(f"Auth error: {e}", exc_info=True)
            raise AuthError(f"Sign out failed. Please try again.")