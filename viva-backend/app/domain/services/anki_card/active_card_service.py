from domain.services.anki_card.card_processor import CardProcessor


class ActiveCardService(CardProcessor):


    def get_word_spell(self, anki_id):
        anki_ids = list()
        anki_ids.append(anki_id)
        card = self.anki_agent.get_cards_info(anki_ids)
        back_value = card[0]['fields']['Back']['value']
        word = self.extract_word_from_back_of_active_card(back_value)
        return word
