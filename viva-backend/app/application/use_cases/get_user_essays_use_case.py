from typing import List, Dict
from infrastructure.repositories.essay_repository import EssayRepository
from domain.entities.entities import Essay

class GetUserEssaysUseCase:
    def __init__(self, essay_repository: EssayRepository):
        self.essay_repository = essay_repository

    def execute(self, user_id: str) -> List[Dict]:
        return self.essay_repository.get_essays_by_user_id(user_id)