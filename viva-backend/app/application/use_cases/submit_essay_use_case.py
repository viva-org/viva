# application/use_cases/process_essay_use_case.py

from typing import Optional
from fastapi import UploadFile
from domain.entities.entities import Essay
from domain.services.essay_processing_service import EssayService
from domain.services.tts_service import slugify
from infrastructure.oss.AliOssAgent import OssAgent
from infrastructure.repositories.essay_repository import EssayRepository
from infrastructure.repositories.active_mapping_repository import ActiveMappingRepository
from infrastructure.task.task_queue import TaskQueue
from infrastructure.repositories.database_manager import db_manager
from test import ImageGenerator
import uuid
import requests
import tempfile
import os


class SubmitEssayUseCase:
    def __init__(self, 
                 essay_processing_service: EssayService, 
                 essay_repository: EssayRepository,
                 mapping_card_repository: ActiveMappingRepository
                 #task_queue: TaskQueue
                 ):
        self.essay_processing_service = essay_processing_service
        self.essay_repository = essay_repository
        self.mapping_card_repository = mapping_card_repository
        self.image_generator = ImageGenerator()
        self.oss_agent = OssAgent()
        #self.task_queue = task_queue

    def execute(self, essay_content: str, image: Optional[UploadFile], user_id: str):
        with db_manager.session_scope() as session:
            title = "暂无"
            image_url = None
            if image is not None:
                # 处理用户上传的图片
                file_extension = image.filename.split('.')[-1]
                slug = slugify(f"essay_cover_{uuid.uuid4()}.{file_extension}")
                image_url = self.oss_agent.upload_file(slug, image)
            else:
                # 获取 AI 生成的图片 URL
                generated_image_url = self.image_generator.generate_cover(essay_content)
                if generated_image_url:
                    # 下载图片
                    response = requests.get(generated_image_url)
                    if response.status_code == 200:
                        # 创建临时文件保存下载的图片
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
                            tmp_file.write(response.content)
                            tmp_path = tmp_file.name
                        
                        try:
                            # 上传到自己的 OSS
                            slug = slugify(f"essay_cover_{uuid.uuid4()}.png")
                            image_url = self.oss_agent.upload_file(slug, tmp_path)
                        finally:
                            # 清理临时文件
                            if os.path.exists(tmp_path):
                                os.remove(tmp_path)
            
            essay = Essay(title=title, content=essay_content, image_url=image_url, user_id=user_id)
            created_essay = self.essay_repository.create_essay(essay, session)
            
            # 处理 essay
            self.essay_processing_service.process_essay(created_essay, session)
            
            return created_essay

    # 以后改成异步的
    def _process_essay_background(self, essay_id: int):
        # 1. 从数据库获取 Essay
        essay = self.essay_repository.get_essay_by_id(essay_id)

        # 2. 处理 Essay，生成 sentence 和 active_mapping_list
        self.essay_processing_service.process_essay(essay)

        # 3. 可以在这里添加其他后续处理，如通知用户处理完成等
