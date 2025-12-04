from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from src.core.database import create_db_and_tables
from src.core.config import CONFIG
from src.routes import user_router, habit_router, challenge_router, auth_router


def create_app(info: dict[str, str]) -> FastAPI:
    app = FastAPI(
        title=info.get("title", "HabitFlow API"),
        summary=info.get("summary", "Track your habits and join challenges"),
        description=info.get("description", "A comprehensive API for habit tracking")
    )

    create_db_and_tables()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[CONFIG.CLIENT_URL],  
        allow_credentials=True,
        allow_methods=["*"],  
        allow_headers=["*"],  
    )

    api_router = APIRouter(prefix="/api")
    api_router.include_router(user_router)
    api_router.include_router(habit_router)
    api_router.include_router(challenge_router)
    api_router.include_router(auth_router)

    @app.get("/")
    def root():
        return {
            "message": "Welcome to Habit Tracker API",
            "docs": "/docs",
            "redoc": "/redoc"
        }

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    app.include_router(api_router)

    return app
