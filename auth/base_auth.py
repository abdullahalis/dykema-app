from abc import ABC, abstractmethod

class AuthManager(ABC):
    @abstractmethod
    def get_user_id(self) -> str:
        pass
    
    @abstractmethod
    def sign_up(self, email: str, password: str) -> None:
        pass

    @abstractmethod
    def sign_in(self, email: str, password: str) -> None:
        pass

    @abstractmethod
    def sign_out(self) -> None:
        pass