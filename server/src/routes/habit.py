from typing import List
from uuid import UUID
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from src.core.database import get_session
from src.schemas.habit import (
    HabitCreate, HabitUpdate, HabitRead,
    HabitLogCreate, HabitLogUpdate, HabitLogRead
)
from src.services.habit import HabitService, HabitLogService

router = APIRouter(prefix="/habits", tags=["habits"])


@router.post("", response_model=HabitRead, status_code=status.HTTP_201_CREATED)
def create_habit(habit_data: HabitCreate, session: Session = Depends(get_session)):
    service = HabitService(session)
    return service.create_habit(habit_data)


@router.get("", response_model=List[HabitRead])
def get_habits(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    service = HabitService(session)
    return service.get_all_habits(skip=skip, limit=limit)


@router.get("/user/{user_id}", response_model=List[HabitRead])
def get_habits_by_user(
    user_id: UUID, 
    active_only: bool = Query(False),
    session: Session = Depends(get_session)
):
    service = HabitService(session)
    if active_only:
        return service.get_active_habits_by_user(user_id)
    return service.get_habits_by_user(user_id)


@router.get("/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: UUID, session: Session = Depends(get_session)):
    service = HabitService(session)
    return service.get_habit(habit_id)


@router.patch("/{habit_id}", response_model=HabitRead)
def update_habit(
    habit_id: UUID, 
    habit_data: HabitUpdate, 
    session: Session = Depends(get_session)
):
    service = HabitService(session)
    return service.update_habit(habit_id, habit_data)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit(habit_id: UUID, session: Session = Depends(get_session)):
    service = HabitService(session)
    service.delete_habit(habit_id)


@router.post("/logs", response_model=HabitLogRead, status_code=status.HTTP_201_CREATED)
def create_habit_log(log_data: HabitLogCreate, session: Session = Depends(get_session)):
    service = HabitLogService(session)
    return service.create_log(log_data)


@router.get("/logs/{log_id}", response_model=HabitLogRead)
def get_habit_log(log_id: UUID, session: Session = Depends(get_session)):
    service = HabitLogService(session)
    return service.get_log(log_id)


@router.get("/{habit_id}/logs", response_model=List[HabitLogRead])
def get_logs_by_habit(
    habit_id: UUID,
    start_date: date = Query(None),
    end_date: date = Query(None),
    session: Session = Depends(get_session)
):
    service = HabitLogService(session)
    if start_date and end_date:
        return service.get_logs_by_date_range(habit_id, start_date, end_date)
    return service.get_logs_by_habit(habit_id)


@router.get("/user/{user_id}/logs", response_model=List[HabitLogRead])
def get_logs_by_user(user_id: UUID, session: Session = Depends(get_session)):
    service = HabitLogService(session)
    return service.get_logs_by_user(user_id)


@router.patch("/logs/{log_id}", response_model=HabitLogRead)
def update_habit_log(
    log_id: UUID, 
    log_data: HabitLogUpdate, 
    session: Session = Depends(get_session)
):
    service = HabitLogService(session)
    return service.update_log(log_id, log_data)


@router.delete("/logs/{log_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_habit_log(log_id: UUID, session: Session = Depends(get_session)):
    service = HabitLogService(session)
    service.delete_log(log_id)
