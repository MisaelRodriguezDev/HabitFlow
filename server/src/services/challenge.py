from typing import List
from uuid import UUID
from sqlmodel import Session
from src.models.challenge import Challenge, ChallengeParticipant, ChallengeHabit
from src.schemas.challenge import (
    ChallengeCreate, ChallengeUpdate,
    ChallengeParticipantCreate, ChallengeParticipantUpdate,
    ChallengeHabitCreate
)
from src.repositories.challenge import (
    ChallengeRepository, 
    ChallengeParticipantRepository,
    ChallengeHabitRepository
)
from fastapi import HTTPException, status


class ChallengeService:
    def __init__(self, session: Session):
        self.repository = ChallengeRepository(session)
    
    def create_challenge(self, challenge_data: ChallengeCreate) -> Challenge:
        challenge = Challenge(**challenge_data.model_dump())
        return self.repository.create(challenge)
    
    def get_challenge(self, challenge_id: UUID) -> Challenge:
        challenge = self.repository.get_by_id(challenge_id)
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Challenge not found"
            )
        return challenge
    
    def get_all_challenges(self, skip: int = 0, limit: int = 100) -> List[Challenge]:
        return self.repository.get_all(skip=skip, limit=limit)
    
    def get_challenges_by_creator(self, creator_id: UUID) -> List[Challenge]:
        return self.repository.get_by_creator_id(creator_id)
    
    def get_public_challenges(self) -> List[Challenge]:
        return self.repository.get_public_challenges()
    
    def update_challenge(self, challenge_id: UUID, challenge_data: ChallengeUpdate) -> Challenge:
        challenge = self.get_challenge(challenge_id)
        return self.repository.update(challenge, challenge_data.model_dump(exclude_unset=True))
    
    def delete_challenge(self, challenge_id: UUID) -> None:
        challenge = self.get_challenge(challenge_id)
        self.repository.delete(challenge)


class ChallengeParticipantService:
    def __init__(self, session: Session):
        self.repository = ChallengeParticipantRepository(session)
    
    def create_participant(self, participant_data: ChallengeParticipantCreate) -> ChallengeParticipant:
        participant = ChallengeParticipant(**participant_data.model_dump())
        return self.repository.create(participant)
    
    def get_participant(self, participant_id: UUID) -> ChallengeParticipant:
        participant = self.repository.get_by_id(participant_id)
        if not participant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Participant not found"
            )
        return participant
    
    def get_participants_by_challenge(self, challenge_id: UUID) -> List[ChallengeParticipant]:
        return self.repository.get_by_challenge_id(challenge_id)
    
    def get_participants_by_user(self, user_id: UUID) -> List[ChallengeParticipant]:
        return self.repository.get_by_user_id(user_id)
    
    def update_participant(
        self, 
        participant_id: UUID, 
        participant_data: ChallengeParticipantUpdate
    ) -> ChallengeParticipant:
        participant = self.get_participant(participant_id)
        return self.repository.update(participant, participant_data.model_dump(exclude_unset=True))
    
    def delete_participant(self, participant_id: UUID) -> None:
        participant = self.get_participant(participant_id)
        self.repository.delete(participant)


class ChallengeHabitService:
    def __init__(self, session: Session):
        self.repository = ChallengeHabitRepository(session)
    
    def create_challenge_habit(self, challenge_habit_data: ChallengeHabitCreate) -> ChallengeHabit:
        challenge_habit = ChallengeHabit(**challenge_habit_data.model_dump())
        return self.repository.create(challenge_habit)
    
    def get_challenge_habit(self, challenge_habit_id: UUID) -> ChallengeHabit:
        challenge_habit = self.repository.get_by_id(challenge_habit_id)
        if not challenge_habit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Challenge habit not found"
            )
        return challenge_habit
    
    def get_habits_by_challenge(self, challenge_id: UUID) -> List[ChallengeHabit]:
        return self.repository.get_by_challenge_id(challenge_id)
    
    def delete_challenge_habit(self, challenge_habit_id: UUID) -> None:
        challenge_habit = self.get_challenge_habit(challenge_habit_id)
        self.repository.delete(challenge_habit)
