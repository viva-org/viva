from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from interfaces.api.essay_controller import router as essay_router
from interfaces.api.review_controller import router as review_router
from interfaces.api.auth_controller import router as auth_router
from domain.services.essay_processing_service import EssayService
from domain.services.active_expression_service import ActiveExpressionService
from domain.services.anki_service import AnkiService
from infrastructure.text_processing.segmentation_service import SegmentationService
from infrastructure.repositories.sentence_repository import SentenceRepository
from infrastructure.repositories.essay_repository import EssayRepository
from infrastructure.repositories.active_mapping_repository import ActiveMappingRepository
from infrastructure.oss.AliOssAgent import OssAgent
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建共享的基础设施实例
segmentation_service = SegmentationService()
sentence_repository = SentenceRepository()
essay_repository = EssayRepository()
active_mapping_repository = ActiveMappingRepository()
oss_agent = OssAgent()

# 配置服务实例
essay_service = EssayService(
    essay_repository=essay_repository,
    sentence_repository=sentence_repository,
    active_mapping_repository=active_mapping_repository,
    segmentation_service=segmentation_service,
)
active_expression_service = ActiveExpressionService()
anki_service = AnkiService()

# 配置依赖注入
def get_essay_service():
    return essay_service

def get_active_expression_service():
    return active_expression_service

def get_anki_service():
    return anki_service

app.dependency_overrides[EssayService] = get_essay_service
app.dependency_overrides[ActiveExpressionService] = get_active_expression_service
app.dependency_overrides[AnkiService] = get_anki_service

# 注册路由
app.include_router(essay_router, prefix="/api", tags=["essays"])
app.include_router(review_router, prefix="/api", tags=["reviews"])
app.include_router(auth_router, prefix="/api", tags=["auth"])

if __name__ == "__main__":
    logger.info("Application started")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
