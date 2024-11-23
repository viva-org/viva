from domain.entities.brick import Brick
from domain.entities.card_type import CardType
from domain.services.anki_card.card_processor import CardProcessor
from infrastructure.anki.anki_agent import AnkiAgent


class PassiveCardService(CardProcessor):

    def __init__(self, anki_agent):
        super().__init__(anki_agent)
        self.deck_name = CardType.PASSIVE.deck_name
        self.note_type = CardType.PASSIVE.note_type

    def generate_card(self, brick:Brick):
        res = self.anki_agent.add_card_to_anki(self.deck_name, self.note_type, brick)
        anki_id = res.get("result", 0)
        return anki_id

    def update_anki_id_field(self, brick, anki_id):
        brick.anki_passive_id = anki_id
        self.pb_agent.update_brick(brick)

    def regenerate_cards(self):
        cards = self.anki_agent.get_suspended_flag1_cards("viva")
        for card in cards:
            spelling = card['fields']["spelling"]['value']
            brick = self.pb_agent.get_brick_by_spelling(spelling)
            # 重新生成 pronunciation
            brick.pronunciation = None
            brick.update_fields()
            # 更新 pg 和 anki
            self.pb_agent.update_brick(brick)
            self.anki_agent.upsert_card_to_anki("viva", self.note_type, brick)

if __name__ == "__main__":
    cardProcessor = PassiveCardService(AnkiAgent())
    cardProcessor.regenerate_cards()
    # db_url = 'postgresql://root:root@localhost/root'
    # repo = BrickRepository(db_url)
    # brick = repo.get_brick_by_spelling("nice")
    # anki_agent = AnkiAgent()
    # print(brick)
    # res = anki_agent.add_card_to_anki("viva",  brick)
    # print(res)
