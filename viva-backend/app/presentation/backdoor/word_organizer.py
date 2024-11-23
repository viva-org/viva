from infrastructure.anki.anki_agent import AnkiAgent


class WordOrganizer:
    def __init__(self, anki_agent):
        self.active_verbs = set()
        self.passive_verbs = set()
        self.added_verbs = set()
        self.word_deck = set()
        self.anki_agent = anki_agent

    def get_active_verb(self):
        ids = self.anki_agent.get_cards_ids_by_deck("odyssey")
        cards_info = self.anki_agent.get_cards_info(ids)
        repeated_verbs = set()  # 用于存储重复的动词
        for card in cards_info:
            back_text = card.get('fields', {}).get('Back', '').get('value', '')
            # 找到 [sound] 标签前的部分
            br_index = back_text.find("<br>")
            if br_index != -1:
                verb_part = back_text[:br_index].strip()  # 去掉前后空格
                if verb_part in self.active_verbs:
                    repeated_verbs.add(verb_part)
                else:
                    self.active_verbs.add(verb_part)
        print("主动词汇量：", len(self.active_verbs))
        if repeated_verbs:
            print("重复的单词：", repeated_verbs)
            print("重复的单词数量：", len(repeated_verbs))

    def get_passive_verb(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                self.passive_verbs.add(line.strip())  # 去掉行尾的换行符并加入集合中
        print("被动词汇量：", len(self.passive_verbs))

    def get_added_verbs(self):
        self.get_active_verb()
        self.get_passive_verb("/Users/liuyishou/usr/projects/viva/files/passive_vab.txt")
        self.added_verbs = self.passive_verbs - self.active_verbs
        with open("added_verbs.txt", 'w') as file:
            for verb in self.added_verbs:
                file.write(verb + "\n")



if __name__ == "__main__":
    organizer = WordOrganizer(AnkiAgent())
    organizer.get_added_verbs()

