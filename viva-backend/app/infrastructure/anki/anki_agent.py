import base64
import json
import logging
from typing import List

import requests

from domain.entities.brick import Brick

# 获取 logger
logger = logging.getLogger(__name__)

class AnkiAgent:

    # documentation：

    def __init__(self, anki_connect_url):
        self.anki_connect_url = anki_connect_url

    def is_deck_exists(self, deck_name):
        """检验某 deck 是否存在

        :param deck_name: deck 名字
        :return: true 代表存在
        """
        payload = {
            "action": "deckNames",
            "version": 6
        }
        response = requests.post(self.anki_connect_url, json=payload)
        decks = response.json().get('result', [])
        return deck_name in decks

    def create_deck(self, deck_name):
        payload = {
            "action": "createDeck",
            "version": 6,
            "params": {
                "deck": deck_name
            }
        }
        response = requests.post(self.anki_connect_url, json=payload)
        return response.json()

    def store_media_file_in_anki(self, file_name, file_content):
        encoded_content = base64.b64encode(file_content).decode('utf-8')
        # if there is an old one, delete it first
        payload = {
            "action": "deleteMediaFile",
            "version": 6,
            "params": {
                "filename": file_name,
            }
        }
        requests.post(self.anki_connect_url, json=payload)
        payload = {
            "action": "storeMediaFile",
            "version": 6,
            "params": {
                "filename": file_name,
                "data": encoded_content,
            }
        }
        response = requests.post(self.anki_connect_url, json=payload)
        return response.json()

    def delete_media_file_from_anki(self, file_name):
        payload = {
            "action": "deleteMediaFile",
            "version": 6,
            "params": {
                "filename": file_name,
            }
        }
        response = requests.post(self.anki_connect_url, json=payload)
        return response.json()

    def add_card_to_anki(self, deck_name, note_type, brick:Brick) -> int:
        fields = {
            "spelling": brick.spelling or "null",
            "english_sentence": brick.english_sentence or "null",
            "ranking": str(brick.ranking) if brick.ranking is not None else "null",
            "pronunciation": brick.pronunciation if brick.pronunciation is not None else "null",
            "chinese_sentence": brick.chinese_sentence if brick.chinese_sentence is not None else "null"
        }

        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": note_type,
                    "fields": fields,
                    "options": {
                        "allowDuplicate": False,
                    },
                    "tags": [
                        "automated"
                    ]
                }
            }
        }
        response = requests.post(self.anki_connect_url, json=payload)
        return response.json()

    def upsert_card_to_anki(self, deck_name, note_type, brick: Brick) -> int:
        fields = {
            "spelling": brick.spelling or "null",
            "english_sentence": brick.english_sentence or "null",
            "ranking": str(brick.ranking) if brick.ranking is not None else "null",
            "pronunciation": brick.pronunciation if brick.pronunciation is not None else "null",
            "chinese_sentence": brick.chinese_sentence if brick.chinese_sentence is not None else "null"
        }

        if brick.anki_passive_id:
            # Update logic
            # Update logic
            payload = {
                "action": "updateNoteFields",
                "version": 6,
                "params": {
                    "note": {
                        "id": brick.anki_passive_id,
                        "fields": fields
                    }
                }
            }
            # Remove suspend and flag1
            remove_suspend_payload = {
                "action": "updateCards",
                "version": 6,
                "params": {
                    "cards": [brick.anki_passive_id],
                    "suspended": False,
                    "flag": 0
                }
            }
            response = requests.post(self.anki_connect_url, json=payload)
            update_response = requests.post(self.anki_connect_url, json=remove_suspend_payload)
        else:
            # Insert logic
            payload = {
                "action": "addNote",
                "version": 6,
                "params": {
                    "note": {
                        "deckName": deck_name,
                        "modelName": note_type,
                        "fields": fields,
                        "options": {
                            "allowDuplicate": False,
                        },
                        "tags": [
                            "automated"
                        ]
                    }
                }
            }
            response = requests.post(self.anki_connect_url, json=payload)
        return response.json()

    def update_card_front(self, note_id, new_front):
        """更新某张卡片的正面

        :param note_id: 卡片的笔记 ID
        :param new_front: 新的正面文本
        :return: true 如果更新成功，否则返回 false
        """
        payload = {
            "action": "updateNoteFields",
            "version": 6,
            "params": {
                "note": {
                    "id": note_id,
                    "fields": {
                        "Front": new_front
                    }
                }
            }
        }
        response = requests.post(self.anki_connect_url, json=payload)
        if response.status_code == 200:
            return response.json().get('result', False)
        else:
            return False

    def update_note_tag(self, note_id, tag):
        """为一个或多个笔记添加标签

        :param note_ids: 笔记ID列表
        :param tag: 要添加的标签，单个或多个标签组成的字符串
        :return: True 如果添加成功，否则返回 False
        """
        url = "http://localhost:8765"
        headers = {"Content-Type": "application/json"}
        payload = {
            "action": "updateNoteTags",
            "version": 6,
            "params": {
                "note": note_id,
                "tags": [tag,]
            }
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            return response.json().get('result', False)
        else:
            return False

    def get_cards_info(self, card_ids:List) -> List:
        url = "http://localhost:8765"
        headers = {"Content-Type": "application/json"}
        payload = {
            "action": "cardsInfo",
            "version": 6,
            "params": {
                "cards": card_ids
            }
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result.get('result', [])
        else:
            return "Error: Failed to communicate with Anki."

    def get_cards_by_flag(self, num):
        url = "http://localhost:8765"
        headers = {"Content-Type": "application/json"}
        payload = {
            "action": "findCards",
            "version": 6,
            "params": {
                "query": f"flag:{num}"
            }
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result.get('result', [])
        else:
            return "Error: Failed to communicate with Anki."

    def get_cards_ids_by_deck(self, deck_name : str) -> list:
        url = "http://localhost:8765"
        headers = {"Content-Type": "application/json"}
        payload = {
            "action": "findCards",
            "version": 6,
            "params": {
                "query": f"deck:{deck_name}"
            }
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            return result.get('result', [])
        else:
            return "Error: Failed to communicate with Anki."

    def get_suspended_flag1_cards(self, deck_name):
        """找到某 deck 下所有标记为 flag1 且 suspend 的卡片

        :param deck_name: 要搜索的 deck 名称
        :return: 符合条件的卡片笔记信息列表
        """
        # Step 1: 找到符合条件的笔记 ID
        find_notes_payload = {
            "action": "findNotes",
            "version": 6,
            "params": {
                "query": f'deck:"{deck_name}" flag:1 is:suspended'
            }
        }
        find_notes_response = requests.post(self.anki_connect_url, json=find_notes_payload)
        note_ids = find_notes_response.json().get('result', [])

        if not note_ids:
            return []

        # Step 2: 获取笔记的详细信息
        notes_info_payload = {
            "action": "notesInfo",
            "version": 6,
            "params": {
                "notes": note_ids
            }
        }
        notes_info_response = requests.post(self.anki_connect_url, json=notes_info_payload)
        notes_info = notes_info_response.json().get('result', [])

        return notes_info

    def remove_suspend_and_flag(self, card_ids: list) -> dict:
        if not card_ids:
            return {"error": "No cards to update"}

        remove_suspend_payload = {
            "action": "updateCards",
            "version": 6,
            "params": {
                "cards": card_ids,
                "suspended": False,
                "flag": 0
            }
        }
        response = requests.post(self.anki_connect_url, json=remove_suspend_payload)
        return response.json()

    def update_suspended_flag1_cards(self) -> dict:
        card_ids = self.get_suspended_flag1_cards()
        if not card_ids:
            return {"message": "No suspended and flagged cards found"}
        result = self.remove_suspend_and_flag(card_ids)
        return result

    def add_card_to_deck(self, deck_name: str, context: str, 
        mapping_wrong_english: str, mapping_correct_english: str, audio_url: str) -> int: # type: ignore
        payload = {
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": deck_name,
                    "modelName": "active_brick",  # 使用active_brick卡片类型
                    "fields": {
                        "context": context,
                        "incorrect_translation": mapping_wrong_english,
                        "correct_translation": mapping_correct_english,
                        "pronunciation": audio_url
                    },
                    "options": {
                        "allowDuplicate": True,  # 这将告诉 Anki 不要进行重复检查，允许添加重复的卡片。
                        "duplicateScope": "none" 
                    },
                    "tags": ["added_by_api"]
                }
            }
        }
        logger.info(payload)

        response = requests.post(self.anki_connect_url, json=payload)
        if response.status_code == 200:
            result = response.json()
            if result.get("error") is None:
                return result["result"]  # 返回新添加的笔记ID
            else:
                raise Exception(f"Anki Connect Error: {result['error']}")
        else:
            raise Exception(f"HTTP Error: {response.status_code}")



if __name__ == '__main__':
    agent = AnkiAgent()
    print(agent.get_cards_ids_by_deck('bricks'))
