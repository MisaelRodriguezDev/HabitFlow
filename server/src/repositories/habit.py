from typing import List
from uuid import UUID
from datetime import date
from sqlmodel import Session, select
from src.models.habit import Habit, HabitLog
from .base import BaseRepository


class HabitRepository(BaseRepository[Habit]):
    def __init__(self, session: Session):
        super().__init__(Habit, session)
    
    def get_by_user_id(self, user_id: UUID) -> List[Habit]:
        statement = select(Habit).where(Habit.user_id == user_id)
        return list(self.session.exec(statement).all())
    
    def get_active_by_user_id(self, user_id: UUID) -> List[Habit]:
        statement = select(Habit).where(
            Habit.user_id == user_id,
            Habit.enabled == True
        )
        return list(self.session.exec(statement).all())


class HabitLogRepository(BaseRepository[HabitLog]):
    def __init__(self, session: Session):
        super().__init__(HabitLog, session)
    
    def get_by_habit_id(self, habit_id: UUID) -> List[HabitLog]:
        statement = select(HabitLog).where(HabitLog.habit_id == habit_id)
        return list(self.session.exec(statement).all())
    
    def get_by_user_id(self, user_id: UUID) -> List[HabitLog]:
        statement = select(HabitLog).where(HabitLog.user_id == user_id)
        return list(self.session.exec(statement).all())
    
    def get_by_date_range(self, habit_id: UUID, start_date: date, end_date: date) -> List[HabitLog]:
        statement = select(HabitLog).where(
            HabitLog.habit_id == habit_id,
            HabitLog.log_date >= start_date,
            HabitLog.log_date <= end_date
        )
        return list(self.session.exec(statement).all())
