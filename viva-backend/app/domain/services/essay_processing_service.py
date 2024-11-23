from re import S
import re
from typing import List
from sqlalchemy.orm import Session

from domain.entities.entities import Essay, ActiveMapping, Sentence, EssaySentence
from infrastructure.repositories import sentence_repository
from infrastructure.repositories.active_mapping_repository import ActiveMappingRepository
from infrastructure.repositories.sentence_repository import SentenceRepository
from infrastructure.text_processing.segmentation_service import SegmentationService
from infrastructure.repositories.database_manager import db_manager
import logging

logger = logging.getLogger(__name__)
class EssayProcessingService:
    def __init__(self, segmentation_service: SegmentationService
                 , sentence_repository: SentenceRepository
                 , active_mapping_repository: ActiveMappingRepository):
        
        self.segmentation_service = segmentation_service
        self.sentence_repository = sentence_repository
        self.active_mapping_repository = active_mapping_repository

    def process_essay(self, essay: Essay, session: Session):
        self.segmentation_service.validate_essay(essay.content)
        
        # 1. 分句并创建 Sentence 对象
        sentences = self.segmentation_service.split_into_sentences(essay.content)
        sentence_objects = []
        
        for sentence_text in sentences:
            sentence = Sentence(sentence=sentence_text)
            session.add(sentence)
            
            # 创建 EssaySentence 关联
            essay_sentence = EssaySentence(essay=essay, sentence=sentence)
            session.add(essay_sentence)
            
            sentence_objects.append(sentence)
        
        # 刷新 session 以获取生成的 ID
        session.flush()
        
        # 2. 分词并创建 ActiveMapping 对象
        for sentence in sentence_objects:
            segmentationResult = self.segmentation_service.segment_sentence(sentence.sentence)
            current_position = 0
            for word_info in segmentationResult.words:
                focus_start, focus_end = self._get_word_position(word_info, segmentationResult.original, current_position)
                current_position = focus_end  # 更新当前位置
                cleaned_words = [
                    word.replace('(', '')
                        .replace(')', '')
                        .replace('（', '')
                        .replace('）', '')
                        .replace('"', '')
                        .replace('"', '')
                        .replace('"', '')
                    for word in word_info.english
                ]
                # 用逗号连接所有单词
                word_info.english = ','.join(cleaned_words)
                active_mapping = ActiveMapping(
                    sentence=sentence,
                    focus_start=focus_start,
                    focus_end=focus_end,
                    chinese=word_info.chinese,
                    user_expression="",
                    ai_review_is_correct=None,
                    ai_review_expression=word_info.english
                )
                session.add(active_mapping)
    
        # 不需要显式调用 commit，因为这个方法应该在一个更大的事务中调用
        # session 的 commit 将在调用此方法的外部进行


    def enter_study_mode(self, essay_id: int):
        essay = self.essay_repository.get_by_id(essay_id)
        

    def generate_title(self, essay_content: str) -> str:
        return "test"

    def process_essay_transaction(self, essay: Essay):
        with db_manager.session_scope() as session:
            self.process_essay(essay, session)

    # 获取单词在 original_text 中的位置 todo：目前的正则方案和 ai 方案效果都不是完美的
    def _get_word_position(self, word_info, original_text: str, current_position: int) -> tuple[int, int]:
        # 正则方案
        word_match = re.search(r'\d+:(\d+)', original_text[current_position:])
        if word_match:
            focus_start = int(word_match.group(1)) + current_position
            focus_end = focus_start + len(word_info.chinese)
        # AI 方案
        else:
            focus_start = word_info.start
            focus_end = word_info.start + word_info.len

        return focus_start, focus_end
