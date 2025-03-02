from re import S
import re
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
import tempfile
import os
import uuid

from domain.entities.entities import Essay, ActiveMapping, Sentence, EssaySentence
from infrastructure.repositories import sentence_repository
from infrastructure.repositories.active_mapping_repository import ActiveMappingRepository
from infrastructure.repositories.sentence_repository import SentenceRepository
from infrastructure.text_processing.segmentation_service import SegmentationService
from infrastructure.repositories.database_manager import db_manager
from infrastructure.repositories.essay_repository import EssayRepository
from infrastructure.oss.AliOssAgent import OssAgent
from domain.services.tts_service import slugify
from fastapi import UploadFile
import logging

logger = logging.getLogger(__name__)
class EssayService:
    def __init__(self, segmentation_service: SegmentationService
                 , sentence_repository: SentenceRepository
                 , active_mapping_repository: ActiveMappingRepository
                 , essay_repository: EssayRepository):
        
        self.segmentation_service = segmentation_service
        self.sentence_repository = sentence_repository
        self.active_mapping_repository = active_mapping_repository
        self.essay_repository = essay_repository
        #self.oss_agent = OssAgent()

    async def create_and_process_essay(self, content: str, image: Optional[UploadFile], user_id: str) -> Essay:
        # Handle image upload if present
        image_url = await self._handle_image_upload(image) if image and image.filename else None
        
        # Create essay entity
        essay = Essay(
            title="暂无",  # Temporary title
            content=content,
            image_url=image_url,
            user_id=user_id
        )
        
        # Create essay and process it within a transaction
        with db_manager.session_scope() as session:
            created_essay = self.essay_repository.create_essay(essay, session)
            self.process_essay(created_essay, session)
            return created_essay

    async def _handle_image_upload(self, image: Optional[UploadFile]) -> Optional[str]:
        """Handle image upload and return the URL of the uploaded image."""
        if not image or not image.filename:
            return None
            
        try:
            file_extension = image.filename.split('.')[-1]
            slug = slugify(f"essay_cover_{uuid.uuid4()}.{file_extension}")
            
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp_file:
                contents = await image.read()
                tmp_file.write(contents)
                tmp_file.flush()
                
                try:
                    # Upload the temporary file
                    return self.oss_agent.upload_file(slug, tmp_file.name)
                finally:
                    # Clean up the temporary file
                    os.unlink(tmp_file.name)
        except Exception as e:
            logger.error(f"Error uploading image: {str(e)}")
            return None

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
                english_str = ','.join(cleaned_words)
                active_mapping = ActiveMapping(
                    sentence=sentence,
                    focus_start=focus_start,
                    focus_end=focus_end,
                    chinese=word_info.chinese,
                    user_expression="",
                    ai_review_is_correct=None,
                    ai_review_expression=english_str
                )
                session.add(active_mapping)

    def enter_study_mode(self, essay_id: int):
        essay = self.essay_repository.get_essay_by_id(essay_id)
        

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

    def get_essay_list(self, user_id: str) -> List[Dict]:
        """Get all essays for a given user."""
        return self.essay_repository.get_essays_by_user_id(user_id)

    def get_essay_detail(self, essay_id: int) -> List[int]:
        """Get all sentence IDs for a given essay."""
        sentences = self.sentence_repository.get_by_essay_id(essay_id)
        return [sentence.sentence_id for sentence in sentences]
