import re

from domain.entities.card_type import CardType
from infrastructure.anki.anki_agent import AnkiAgent
from infrastructure.database.brick_repository import BrickRepository


class CardService:
    """
    这个类用来处理 ANKI 卡片，本质是对 anki 的 sqlite 数据库的读写

    属性：

    """

    def __init__(self, anki_agent):
        self.anki_agent = anki_agent
        db_url = 'postgresql://root:root@localhost/root'
        self.pb_agent = BrickRepository(db_url)

    def active_to_positive(self, deck_name):
        """
        将已有的主动词汇卡片翻转为被动听力卡片

        """
        new_deck_name = deck_name + "_reverse"
        if not self.anki_agent.is_deck_exists(new_deck_name):
            self.anki_agent.create_deck(new_deck_name)
        card_id_list = self.anki_agent.get_cards_ids_by_deck(deck_name)
        cards = self.anki_agent.get_cards_info(card_id_list)
        for card in cards:
            front_value = card['fields']['Front']['value']
            back_value = card['fields']['Back']['value']
            # 提取单词发音
            sound_pattern = re.search(r'\[sound:([^\]]+)\]', back_value)
            sound_info = sound_pattern.group(1) if sound_pattern else "default_sound.mp3"  # 默认音频文件
            print("Sound file:", sound_info if sound_pattern else "No sound file found in the back content.")

            # 提取单词的拼写
            word_spelling = re.split(r'\[sound:', back_value)[0]

            # 制作新的被动词汇卡片
            new_front_value = r'[sound:{}]'.format(sound_info)
            new_back_value = front_value + ' ' + word_spelling.strip()
            res = self.anki_agent.add_card_to_anki(new_deck_name, new_front_value, new_back_value)
            print(res)

    def make_sentences_for_positive(self, deck_name="odyssey__reverse"):
        """
        将已有的主动词汇卡片翻转为被动听力卡片

        """
        new_deck_name = deck_name + "_reverse"
        if not self.anki_agent.is_deck_exists(new_deck_name):
            self.anki_agent.create_deck(new_deck_name)
        card_id_list = self.anki_agent.get_cards_ids_by_deck(deck_name)
        cards = self.anki_agent.get_cards_info(card_id_list)
        for card in cards:
            front_value = card['fields']['Front']['value']
            back_value = card['fields']['Back']['value']


    def mark_rank_for_active_card(self, writing_deck_name="odyssey"):
        card_id_list = self.anki_agent.get_cards_ids_by_deck(writing_deck_name)
        cards = self.anki_agent.get_cards_info(card_id_list)
        for card in cards:
            front_value = card['fields']['Front']['value']
            back_value = card['fields']['Back']['value']
            # 提取单词的拼写
            word_spelling = self.extract_word_from_back_of_active_card(back_value)
            rank = self.word_rank_dict.get(word_spelling.lower(), 66666)
            if rank == 66666:
                print("【"+ word_spelling +"】" + " failed")
            else:
                print("【"+ word_spelling +"】" + str(rank))
            # 制作新的被动词汇卡片
            self.anki_agent.update_note_tag(int(card["cardId"]), "r"+str(rank))
        return None

    def get_cards_ids_by_deck(self, deck_name):
        card_id_list = self.anki_agent.get_cards_ids_by_deck(deck_name)
        return card_id_list

    def get_words_from_active_deck(self, writing_deck_name="odyssey"):
        card_id_list = self.anki_agent.get_cards_ids_by_deck(writing_deck_name)
        cards = self.anki_agent.get_cards_info(card_id_list)
        with open("../active_words.txt", "w") as f:
            for card in cards:
                back_value = card['fields']['Back']['value']
                word = self.extract_word_from_back_of_active_card(back_value)
                f.write(word+"\n")
                print(word)


    def mark_rank_for_positive_card(self, listening_deck_name="odyssey_reverse"):
        card_id_list = self.anki_agent.get_cards_ids_by_deck(listening_deck_name)
        cards = self.anki_agent.get_cards_info(card_id_list)
        for card in cards:
            front_value = card['fields']['Front']['value']
            back_value = card['fields']['Back']['value']
            # 提取单词的拼写
            word_spelling = self.extract_word_from_front_of_positive_card(front_value).strip()
            rank = self.word_rank_dict.get(word_spelling.lower(), 66666)
            if rank == 66666:
                print("【"+ word_spelling +"】" + " failed")
            else:
                print("【"+ word_spelling +"】" + str(rank))
            # 将 rank 打到 tag
            self.anki_agent.update_note_tag(int(card["cardId"]), "r"+str(rank))
        return None

    def extract_word_from_back_of_active_card(self, back_value):
        # 查找 '[sound:' 之前的所有文本
        match = re.search(r'(.*)\[sound:', back_value)
        if match:
            # 获取 '[sound:' 前的文本
            text_before_sound = match.group(1)
            # 从这部分文本中提取所有单词
            words = re.findall(r'\b\w+\b', text_before_sound)
        words_before_sound = words[:-1]
        connected_words = ' '.join(words_before_sound)
        return connected_words.strip()



    def extract_word_from_front_of_positive_card(self, front_value):
        # 使用正则表达式匹配 [sound: 后和 .mp3 前的字符
        match = re.search(r'\[sound:(.*?)\.mp3\]', front_value)
        if match:
            sound_name = match.group(1)  # 提取匹配到的第一组括号中的内容
            return sound_name
        else:
            return "null"

    """将 anki 中的卡片 id 存到对应的数据库字段中
        
    """
    def register_anki_to_db(self):
        card_id_list = self.anki_agent.get_cards_ids_by_deck("odyssey")
        for id in card_id_list:
            spelling = self.get_word_spell(id, CardType.ACTIVE)
            brick = self.pb_agent.get_brick_by_spelling(spelling)
            brick.anki_active_id = id
            self.pb_agent.update_brick(brick)

    def get_word_spell(self, id, card_type):
        if card_type == CardType.ACTIVE:
            ids = list()
            ids.append(id)
            card = self.anki_agent.get_cards_info(ids)
            back_value = card[0]['fields']['Back']['value']
            word = self.extract_word_from_back_of_active_card(back_value)
        return word






if __name__ == "__main__":
    # CardProcessor(AnkiAgent()).active_to_positive("odyssey")
    card_service = CardService(AnkiAgent())
    id = card_service.get_cards_ids_by_deck("odyssey")[0]
    spelling = card_service.get_word_spell(id, CardType.ACTIVE)
    brick = card_service.pb_agent.get_brick_by_spelling(spelling)
    brick.anki_active_id = id
    card_service.pb_agent.update_brick(brick)
    word_spell = card_service.get_word_spell(id, CardType.ACTIVE)
    print(brick.spelling)


