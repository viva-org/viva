import logging

logger = logging.getLogger(__name__)

from typing import List, Dict
from domain.entities.brick import Brick
from infrastructure.database.brick_repository import BrickRepository


class BrickService:
    def __init__(self, db_url=None):
        logger.info("Initializing BrickService")
        self.repository = BrickRepository(db_url)

    def get_all_bricks(self) -> List[Brick]:
        logger.info("Getting all bricks")
        return self.repository.get_all_bricks()

    def get_brick_by_spelling(self, spelling: str) -> Brick:
        return self.repository.get_brick_by_spelling(spelling)

    def create_brick(self, brick: Brick) -> None:
        self.repository.create_brick(brick)

    def update_brick(self, brick: Brick) -> None:
        self.repository.update_brick(brick)

    def delete_brick(self, brick_id: int) -> None:
        self.repository.delete_brick(brick_id)

    def bulk_insert_bricks(self, bricks: List[Brick]) -> None:
        self.repository.bulk_insert_brick(bricks)

    def add_active_use_scenario(self, spelling: str,
        chinese_scenario: str) -> None:
        self.repository.add_active_use_scenario(spelling, chinese_scenario)

    def get_bricks_by_scenario(self, chinese_word: str) -> List[Dict]:
        return self.repository.get_bricks_by_chinese_word(chinese_word)

    def get_active_use_scenarios(self, spelling: str) -> Dict:
        brick = self.get_brick_by_spelling(spelling)
        if brick and brick.active_use_scenario:
            return brick.active_use_scenario
        return {}

    def increment_frequency(self, spelling: str, frequency_type: str) -> None:
        brick = self.get_brick_by_spelling(spelling)
        if brick:
            if frequency_type == 'spoken':
                brick.spoken_frequency = (brick.spoken_frequency or 0) + 1
            elif frequency_type == 'written':
                brick.written_frequency = (brick.written_frequency or 0) + 1
            elif frequency_type == 'listening':
                brick.listening_frequency = (brick.listening_frequency or 0) + 1
            self.update_brick(brick)

    def set_active_vocabulary(self, spelling: str, is_active: bool) -> None:
        brick = self.get_brick_by_spelling(spelling)
        if brick:
            brick.active_vocabulary = is_active
            self.update_brick(brick)

    def get_active_vocabulary(self) -> List[Brick]:
        return self.repository.session.query(Brick).filter_by(
            active_vocabulary=True).all()

    def upsert_active_use_scenario(self, spelling: str,
        chinese_scenario: str) -> None:
        # 先检查有没有这个词，没有要新建，既然主动用了，必然属于已有的 brick
        brick = self.get_brick_by_spelling(spelling)

        if not brick:
            # 如果没有找到这个词，创建一个新的 Brick
            brick = Brick(spelling=spelling)
            self.repository.create_brick(brick)

        self.repository.update_active_use_scenario(spelling, chinese_scenario)


# 示例用法
if __name__ == "__main__":
    service = BrickService()

    # 测试查询
    bricks = service.get_bricks_by_scenario('脑子里')
    for brick in bricks:
        print(brick)
