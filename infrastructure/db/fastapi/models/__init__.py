# Import all models here to ensure they are registered with SQLModel.metadata
from .user_model import User

# Export models for easy import
__all__ = ["User"]
