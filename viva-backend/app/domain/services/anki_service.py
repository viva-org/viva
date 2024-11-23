import os
from typing import List

from dotenv import load_dotenv

from domain.entities.brick import Brick
from domain.services.tts_service import tts
from infrastructure.anki.anki_agent import AnkiAgent

load_dotenv()


class AnkiService:
    def __init__(self, deck_name: str = 'Default', note_type: str = 'Basic',
        anki_connect_url: str = "http://localhost:8765"):
        self.agent = AnkiAgent(os.getenv("ANKI_CONNECT_URL"))
        self.deck_name = deck_name
        self.note_type = note_type

    def ensure_deck_exists(self):
        if not self.agent.is_deck_exists(self.deck_name):
            self.agent.create_deck(self.deck_name)

    def add_or_update_brick(self, brick: Brick) -> int:
        self.ensure_deck_exists()
        return self.agent.upsert_card_to_anki(self.deck_name, self.note_type,
                                              brick)

    def add_media_file(self, file_name: str, file_content: bytes):
        return self.agent.store_media_file_in_anki(file_name, file_content)

    def remove_media_file(self, file_name: str):
        return self.agent.delete_media_file_from_anki(file_name)

    def get_suspended_cards(self) -> List[dict]:
        return self.agent.get_suspended_flag1_cards(self.deck_name)

    def reactivate_cards(self, card_ids: List[int]):
        return self.agent.remove_suspend_and_flag(card_ids)

    def get_cards_by_flag(self, flag_num: int) -> List[int]:
        return self.agent.get_cards_by_flag(flag_num)

    def get_cards_info(self, card_ids: List[int]) -> List[dict]:
        return self.agent.get_cards_info(card_ids)

    def update_card_front(self, note_id, new_front):
        return self.agent.update_card_front(note_id, new_front)

    def update_note_tag(self, note_id, tag):
        return self.agent.update_note_tag(note_id, tag)

    # 给指定的 deck，增加指定的卡片，卡片的正面，卡片的背面
    def add_card_to_deck(self, deck_name: str, sentence: str, mapping_chinese: str,
        mapping_wrong_english: str, mapping_correct_english: str) -> int:
        if not mapping_wrong_english:
            mapping_wrong_english = "?"
            
        # 清理特殊字符
        clean_sentence = self._clean_text_for_anki(sentence)
        clean_chinese = self._clean_text_for_anki(mapping_chinese)
        
        # 替换中文并添加高亮
        context = clean_sentence.replace(
            clean_chinese,
            f'<span style="color: red; font-weight: bold;">{clean_chinese}</span>'
        )
        
        audio_url = tts(mapping_correct_english)
        print("audio_url:", audio_url)
        return self.agent.add_card_to_deck(deck_name, context, 
                                         mapping_wrong_english,
                                         mapping_correct_english,
                                         audio_url)
    
    def _clean_text_for_anki(self, text: str) -> str:
        """清理可能影响 Anki HTML 渲染的特殊字符"""
        replacements = {
            '=': '',   # 移除等号
            '[': '',   # 移除左方括号
            ']': '',   # 移除右方括号
            '{': '',   # 可选：移除左花括号
            '}': '',   # 可选：移除右花括号
            '<': '&lt;',  # 转义 HTML 特殊字符
            '>': '&gt;',  # 转义 HTML 特殊字符
            '\n': '',  # 移除换行符
            '\r': '',  # 移除回车符
        }
        
        for old, new in replacements.items():
            text = text.replace(old, new)
            
        return text.strip()
