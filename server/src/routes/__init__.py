from .user import router as user_router
from .habit import router as habit_router
from .challenge import router as challenge_router
from .auth import router as auth_router

__all__ = [
    "user_router",
    "habit_router",
    "challenge_router",
    "auth_router"
]
