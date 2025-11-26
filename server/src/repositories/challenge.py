from typing import List
from uuid import UUID
from sqlmodel import Session, select
from src.models.challenge import Challenge, ChallengeParticipant, ChallengeHabit
from .base import BaseRepository


class ChallengeRepository(BaseRepository[Challenge]):
    def __init__(self, session: Session):
        super().__init__(Challenge, session)
    
    def get_by_creator_id(self, creator_id: UUID) -> List[Challenge]:
        statement = select(Challenge).where(Challenge.created_by == creator_id)
        return list(self.session.exec(statement).all())
    
    def get_public_challenges(self) -> List[Challenge]:
        statement = select(Challenge).where(Challenge.is_public == True)
        return list(self.session.exec(statement).all())


class ChallengeParticipantRepository(BaseRepository[ChallengeParticipant]):
    def __init__(self, session: Session):
        super().__init__(ChallengeParticipant, session)
    
    def get_by_challenge_id(self, challenge_id: UUID) -> List[ChallengeParticipant]:
        statement = select(ChallengeParticipant).where(
            ChallengeParticipant.challenge_id == challenge_id
        )
        return list(self.session.exec(statement).all())
    
    def get_by_user_id(self, user_id: UUID) -> List[ChallengeParticipant]:
        statement = select(ChallengeParticipant).where(
            ChallengeParticipant.user_id == user_id
        )
        return list(self.session.exec(statement).all())


class ChallengeHabitRepository(BaseRepository[ChallengeHabit]):
    def __init__(self, session: Session):
        super().__init__(ChallengeHabit, session)
    
    def get_by_challenge_id(self, challenge_id: UUID) -> List[ChallengeHabit]:
        statement = select(ChallengeHabit).where(
            ChallengeHabit.challenge_id == challenge_id
        )
        return list(self.session.exec(statement).all())
