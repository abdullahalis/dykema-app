import config
from abc import ABC, abstractmethod
from supabase import create_client, Client

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
        self.supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

    def get_user_id(self):
        try:
            response = self.supabase.auth.get_user()
            return response.user.id if response else None
        except Exception:
            return None
        
    def sign_up(self, email, password):
        try:
            response = self.supabase.auth.sign_up(
                {
                    "email": email,
                    "password": password
                }
            )
            return True if response.user else False
        except Exception:
            return False
    
    def sign_in(self, email, password):
        try:
            response = self.supabase.auth.sign_in_with_password(
                {
                    "email": email,
                    "password": password
                }
            )
            return True if response.user else False
        except Exception:
            return False

    def sign_out(self):
        try:
            response = self.supabase.auth.sign_out()
            return True
        except Exception:
            return False
    
