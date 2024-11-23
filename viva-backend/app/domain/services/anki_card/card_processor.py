from abc import abstractmethod, ABC

from domain.entities.brick import Brick
from infrastructure.database.brick_repository import BrickRepository


class CardProcessor(ABC):

    """
    抽象基类用来定义处理 ANKI 卡片的模板方法
    """
    def __init__(self, anki_agent):
        self.anki_agent = anki_agent
        self.db_url = 'postgresql://root:root@localhost/root'
        self.pb_agent = BrickRepository(self.db_url)

    @abstractmethod
    def generate_card(self, brick:Brick) -> int:
        pass

    @abstractmethod
    def update_anki_id_field(self, brick, anki_id):
        pass

    """
    检错整个 pg 库，并为还没有生成被动卡片的 brick 制作卡片
    这是一个幂等的方法
    """
    def generate_cards(self):
        bricks = self.pb_agent.get_all_bricks()
        for brick in bricks:
            # 筛选出还没生成过被动卡片的
            if brick.anki_passive_id == None or brick.anki_passive_id == 0:
                # 且已经具备了生成被动卡片的字段
                if brick.ranking != None and brick.pronunciation != None:
                    anki_id = self.generate_card(brick)
                    # 成功生成 anki 卡片后才会在 pg 中注册
                    if anki_id != 0:
                        self.update_anki_id_field(brick, anki_id)

