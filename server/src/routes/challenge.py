from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from src.core.database import get_session
from src.schemas.challenge import (
    ChallengeCreate, ChallengeUpdate, ChallengeRead,
    ChallengeParticipantCreate, ChallengeParticipantUpdate, ChallengeParticipantRead,
    ChallengeHabitCreate, ChallengeHabitRead
)
from src.services.challenge import (
    ChallengeService, 
    ChallengeParticipantService,
    ChallengeHabitService
)

router = APIRouter(prefix="/challenges", tags=["challenges"])


@router.post("", response_model=ChallengeRead, status_code=status.HTTP_201_CREATED)
def create_challenge(challenge_data: ChallengeCreate, session: Session = Depends(get_session)):
    service = ChallengeService(session)
    return service.create_challenge(challenge_data)


@router.get("", response_model=List[ChallengeRead])
def get_challenges(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    service = ChallengeService(session)
    return service.get_all_challenges(skip=skip, limit=limit)


@router.get("/public", response_model=List[ChallengeRead])
def get_public_challenges(session: Session = Depends(get_session)):
    service = ChallengeService(session)
    return service.get_public_challenges()


@router.get("/creator/{creator_id}", response_model=List[ChallengeRead])
def get_challenges_by_creator(creator_id: UUID, session: Session = Depends(get_session)):
    service = ChallengeService(session)
    return service.get_challenges_by_creator(creator_id)


@router.get("/{challenge_id}", response_model=ChallengeRead)
def get_challenge(challenge_id: UUID, session: Session = Depends(get_session)):
    service = ChallengeService(session)
    return service.get_challenge(challenge_id)


@router.patch("/{challenge_id}", response_model=ChallengeRead)
def update_challenge(
    challenge_id: UUID, 
    challenge_data: ChallengeUpdate, 
    session: Session = Depends(get_session)
):
    service = ChallengeService(session)
    return service.update_challenge(challenge_id, challenge_data)


@router.delete("/{challenge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_challenge(challenge_id: UUID, session: Session = Depends(get_session)):
    service = ChallengeService(session)
    service.delete_challenge(challenge_id)


@router.post("/participants", response_model=ChallengeParticipantRead, status_code=status.HTTP_201_CREATED)
def create_participant(
    participant_data: ChallengeParticipantCreate, 
    session: Session = Depends(get_session)
):
    service = ChallengeParticipantService(session)
    return service.create_participant(participant_data)


@router.get("/participants/{participant_id}", response_model=ChallengeParticipantRead)
def get_participant(participant_id: UUID, session: Session = Depends(get_session)):
    service = ChallengeParticipantService(session)
    return service.get_participant(participant_id)


@router.get("/{challenge_id}/participants", response_model=List[ChallengeParticipantRead])
def get_participants_by_challenge(challenge_id: UUID, session: Session = Depends(get_session)):
    service = ChallengeParticipantService(session)
    return service.get_participants_by_challenge(challenge_id)


@router.get("/user/{user_id}/participations", response_model=List[ChallengeParticipantRead])
def get_participants_by_user(user_id: UUID, session: Session = Depends(get_session)):
    service = ChallengeParticipantService(session)
    return service.get_participants_by_user(user_id)


@router.patch("/participants/{participant_id}", response_model=ChallengeParticipantRead)
def update_participant(
    participant_id: UUID, 
    participant_data: ChallengeParticipantUpdate, 
    session: Session = Depends(get_session)
):
    service = ChallengeParticipantService(session)
    return service.update_participant(participant_id, participant_data)


@router.delete("/participants/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_participant(participant_id: UUID, session: Session = Depends(get_session)):
    service = ChallengeParticipantService(session)
    service.delete_participant(participant_id)


@router.post("/habits", response_model=ChallengeHabitRead, status_code=status.HTTP_201_CREATED)
def create_challenge_habit(
    challenge_habit_data: ChallengeHabitCreate, 
    session: Session = Depends(get_session)
):
    service = ChallengeHabitService(session)
    return service.create_challenge_habit(challenge_habit_data)


@router.get("/habits/{challenge_habit_id}", response_model=ChallengeHabitRead)
def get_challenge_habit(challenge_habit_id: UUID, session: Session = Depends(get_session)):
    service = ChallengeHabitService(session)
    return service.get_challenge_habit(challenge_habit_id)


@router.get("/{challenge_id}/habits", response_model=List[ChallengeHabitRead])
def get_habits_by_challenge(challenge_id: UUID, session: Session = Depends(get_session)):
    service = ChallengeHabitService(session)
    return service.get_habits_by_challenge(challenge_id)


@router.delete("/habits/{challenge_habit_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_challenge_habit(challenge_habit_id: UUID, session: Session = Depends(get_session)):
    service = ChallengeHabitService(session)
    service.delete_challenge_habit(challenge_habit_id)
