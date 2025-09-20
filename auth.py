import config
from supabase import create_client, Client

class AuthManager:
    def __init__(self):
        self.supabase = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

    def get_user(self):
        try:
            response = self.supabase.auth.get_user()
            return response.user if response else None
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
            print(response)
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
            print(response)
            return True if response.user else False
        except Exception:
            return False

    
    def sign_out(self):
        try:
            response = self.supabase.auth.sign_out()
            print(response)
            return True
        except Exception:
            return False