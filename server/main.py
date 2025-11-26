from src.server import create_app

info = {
    "title": "HabitFlow API",
    "summary": "Track your habits, monitor progress, and join challenges",
    "description": """
    A comprehensive REST API for tracking personal habits, managing user profiles, 
    and organizing community challenges. Built with FastAPI and SQLModel using 
    the repository pattern for clean, maintainable code.
    
    ## Features
    
    * **User Management** - Create and manage user accounts with profiles
    * **Habit Tracking** - Define habits with goals and track daily progress
    * **Challenge System** - Create and participate in group challenges
    * **Score Tracking** - Earn points for completing habit goals
    """
}

app = create_app(info)
