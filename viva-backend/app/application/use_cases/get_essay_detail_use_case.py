

class GetEssayDetailUseCase:
    def __init__(self, essay_repository: EssayRepository):
        self.essay_repository = essay_repository

    def execute(self, essay_id: str, user_id: str):
        essay = self.essay_repository.get_essay_by_id(essay_id, user_id)
        return essay