import unittest

from domain.services.anki_card.card_service import CardService
from infrastructure.anki.anki_agent import AnkiAgent


class TestCardProcessor(unittest.TestCase):
    def setUp(self):
        # 初始化一个 CardProcessor 对象，并用 MagicMock 替换其 AnkiAgent
        self.card_processor = CardService()
        self.card_processor.anki_agent = AnkiAgent()

        # 假设的卡片数据，你可以根据实际情况调整这些数据
        self.mock_cards = [
            {"front": "run", "back": "ran"},
            {"front": "jump", "back": "jumped"}
        ]

    def test_active_to_positive(self):
        # 设置当调用 get_cards_by_deck 时返回模拟的卡片数据
        self.card_processor.anki_agent.get_cards_ids_by_deck.return_value = self.mock_cards

        # 调用 active_to_positive 方法
        deck_name = "odyssey"
        res = self.card_processor.active_to_positive(deck_name)

        print(res)
        # 确认 get_cards_by_deck 被正确调用
        self.card_processor.anki_agent.get_cards_ids_by_deck.assert_called_with(deck_name)


        # 这里你可以添加更多的断言来验证方法的其它行为，例如：
        # 确认卡片是否被正确转换为被动听力卡片
        # (示例缺乏具体的被动转换逻辑，你需要根据实际代码添加相关测试)

if __name__ == '__main__':
    unittest.main()