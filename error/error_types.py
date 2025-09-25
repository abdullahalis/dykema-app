class AuthError(Exception):
    """Exception raised for authentication-related errors."""
    pass

class StorageError(Exception):
    """Exception raised for storage-related errors."""
    pass

class LLMError(Exception):
    """Exception raised for LLM-related errors."""
    pass