import config
import logging
from error_types import AuthError
from abc import ABC, abstractmethod

class AuthManager(ABC):
    @abstractmethod
    def get_user_id(self):
        pass
    
    @abstractmethod
    def sign_up(self, email, password):
        pass

    @abstractmethod
    def sign_in(self, email, password):
        pass

    @abstractmethod
    def sign_out(self):
        pass

class SupabaseAuthManager(AuthManager):
    def __init__(self):
        self.supabase = config.supabase

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
        
    def test_rls_policy(self):
        """Test if RLS policy allows select, insert, update, and delete"""
        try:
            

            # 1. Test INSERT
            convo = {"user_id": self.get_user_id(), "messages": []}
            response = self.supabase.table("conversations").insert(convo).execute()
            insert_success = response.data and len(response.data) > 0
            convo_id = response.data[0]["id"] if insert_success else None
            print(f"{'✅' if insert_success else '❌'} Insert test")

            # Bail out if insert failed (can’t continue with select/update/delete)
            if not convo_id:
                return False

            # 2. Test SELECT
            response = (
                self.supabase
                    .table("conversations")
                    .select("id")
                    .limit(1)
                    .execute()
            )
            print(f"RLS select test successful: {len(response.data)} rows returned")

            # 3. Test UPDATE
            response = (
                self.supabase
                    .table("conversations")
                    .update({"messages": ["hello"]})
                    .eq("id", convo_id)
                    .execute()
            )
            update_success = response.data and response.data[0]["messages"] == ["hello"]
            print(f"{'✅' if update_success else '❌'} Update test")

            # 4. Test DELETE
            response = (
                self.supabase
                    .table("conversations")
                    .delete()
                    .eq("id", convo_id)
                    .execute()
            )
            delete_success = response.data and response.data[0]["id"] == convo_id
            print(f"{'✅' if delete_success else '❌'} Delete test")

            return insert_success and update_success and delete_success

        except Exception as e:
            print(f"RLS test failed: {e}")
            return False

    
