from typing import List
from uuid import UUID
from datetime import date
from sqlmodel import Session
from src.models.habit import Habit, HabitLog
from src.schemas.habit import HabitCreate, HabitUpdate, HabitLogCreate, HabitLogUpdate
from src.repositories.habit import HabitRepository, HabitLogRepository
from fastapi import HTTPException, status


class HabitService:
    def __init__(self, session: Session):
        self.repository = HabitRepository(session)
    
    def create_habit(self, habit_data: HabitCreate) -> Habit:
        habit = Habit(**habit_data.model_dump())
        return self.repository.create(habit)
    
    def get_habit(self, habit_id: UUID) -> Habit:
        habit = self.repository.get_by_id(habit_id)
        if not habit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Habit not found"
            )
        return habit
    
    def get_all_habits(self, skip: int = 0, limit: int = 100) -> List[Habit]:
        return self.repository.get_all(skip=skip, limit=limit)
    
    def get_habits_by_user(self, user_id: UUID) -> List[Habit]:
        return self.repository.get_by_user_id(user_id)
    
    def get_active_habits_by_user(self, user_id: UUID) -> List[Habit]:
        return self.repository.get_active_by_user_id(user_id)
    
    def update_habit(self, habit_id: UUID, habit_data: HabitUpdate) -> Habit:
        habit = self.get_habit(habit_id)
        return self.repository.update(habit, habit_data.model_dump(exclude_unset=True))
    
    def delete_habit(self, habit_id: UUID) -> None:
        habit = self.get_habit(habit_id)
        self.repository.delete(habit)


class HabitLogService:
    def __init__(self, session: Session):
        self.repository = HabitLogRepository(session)
    
    def create_log(self, log_data: HabitLogCreate) -> HabitLog:
        log = HabitLog(**log_data.model_dump())
        return self.repository.create(log)
    
    def get_log(self, log_id: UUID) -> HabitLog:
        log = self.repository.get_by_id(log_id)
        if not log:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Habit log not found"
            )
        return log
    
    def get_logs_by_habit(self, habit_id: UUID) -> List[HabitLog]:
        return self.repository.get_by_habit_id(habit_id)
    
    def get_logs_by_user(self, user_id: UUID) -> List[HabitLog]:
        return self.repository.get_by_user_id(user_id)
    
    def get_logs_by_date_range(
        self, 
        habit_id: UUID, 
        start_date: date, 
        end_date: date
    ) -> List[HabitLog]:
        return self.repository.get_by_date_range(habit_id, start_date, end_date)
    
    def update_log(self, log_id: UUID, log_data: HabitLogUpdate) -> HabitLog:
        log = self.get_log(log_id)
        return self.repository.update(log, log_data.model_dump(exclude_unset=True))
    
    def delete_log(self, log_id: UUID) -> None:
        log = self.get_log(log_id)
        self.repository.delete(log)
