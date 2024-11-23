import asyncio
from typing import Optional
from fastapi import HTTPException, UploadFile, BackgroundTasks
from domain.services.brick_service import BrickService
from infrastructure.oss.AliOssAgent import OssAgent
from infrastructure.text.llm_agent import LLMAgent
from infrastructure.text_processing.segmentation_service import SegmentationService

class EssayService:
    def __init__(self):
        self.oss_agent = OssAgent()
        self.llm_agent = LLMAgent()
        self.segmentation_service = SegmentationService()
        self.brick_service = BrickService()

    async def process_essay(self, content: str, image: Optional[UploadFile] = None, background_tasks: Optional[BackgroundTasks] = None):
        if not content.strip():
            raise HTTPException(status_code=400, detail="作文内容不能为空。")
        if len(content) > 1500:
            raise HTTPException(status_code=400, detail="作文内容不能超过1500个字。")
        
        image_url = await self._handle_image_upload(image)
        essay_id = await self._save_essay_to_database(content, image_url)
        
        # 添加后台任务
        background_tasks.add_task(self._process_essay_background, essay_id, content)
        
        return {
            "essay_id": essay_id,
            "message": "文章已成功保存，正在进行后续处理"
        }

    async def _handle_image_upload(self, image: Optional[UploadFile] = None) -> Optional[str]:
        # 图片上传逻辑保持不变
        ...

    async def _save_essay_to_database(self, content: str, image_url: Optional[str]) -> int:
        # 实现保存文章到数据库的逻辑
        # 返回文章ID
        ...

    async def _process_essay_background(self, essay_id: int, content: str):
        # 异步生成标题
        title_task = asyncio.create_task(self.llm_agent.generate_title(content))
        
        # 异步进行分词
        sentences_task = asyncio.create_task(self.segmentation_service.segment_to_sentences(content))
        
        # 等待两个任务完成
        title, sentences = await asyncio.gather(title_task, sentences_task)
        
        # 生成 MappingList
        mapping_list = await self._generate_mapping_list(sentences)
        
        # 更新数据库中的文章信息
        await self._update_essay_in_database(essay_id, title, sentences, mapping_list)

    async def _generate_mapping_list(self, sentences):
        mapping_list = []
        for sentence in sentences:
            words = self.segmentation_service.segment_to_words(sentence)
            for word in words:
                past_usage = await self.brick_service.get_bricks_by_scenario(word)
                mapping_list.append({
                    "chinese_word": word,
                    "sentence": sentence,
                    "past_usage": str(past_usage),
                    "current_use": None,
                    "is_need_translation": self.segmentation_service.should_translate(word)
                })
        return mapping_list

    async def _update_essay_in_database(self, essay_id: int, title: str, sentences: list, mapping_list: list):
        # 实现更新数据库中文章信息的逻辑
        ...
