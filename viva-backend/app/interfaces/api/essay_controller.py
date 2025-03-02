from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
import logging
from typing import List, Optional
import tempfile
import os
from application.use_cases.get_sentence_use_case import GetSentenceUseCase
from application.use_cases.get_user_essays_use_case import GetUserEssaysUseCase
from domain.entities.entities import Essay
from domain.schemas.essay_schema import EssaySchema, EssayWithSentencesSchema
from domain.services.active_expression_service import AICheckRequest, ActiveExpressionService
from domain.services.anki_service import AnkiService
from domain.services.essay_processing_service import EssayService
from domain.services.tts_service import slugify
from infrastructure.repositories.active_mapping_repository import ActiveMappingRepository
from infrastructure.repositories.sentence_repository import SentenceRepository
from infrastructure.repositories.database_manager import db_manager
from infrastructure.oss.AliOssAgent import OssAgent
from infrastructure.text_processing.segmentation_service import SegmentationService
from interfaces.service.jwt_service import get_current_user
from infrastructure.repositories.essay_repository import EssayRepository
from pydantic import BaseModel, ValidationError
import uuid

router = APIRouter()

logger = logging.getLogger(__name__)
class AddToAnkiRequest(BaseModel):
    sentence: str
    mapping_chinese: str
    mapping_wrong_english: str
    mapping_correct_english: str

@router.get("/essays", response_model=List[EssaySchema])
async def get_user_essays(
    current_user: dict = Depends(get_current_user),
    essay_repository: EssayRepository = Depends(EssayRepository),
    segmentation_service: SegmentationService = Depends(SegmentationService),
    sentence_repository: SentenceRepository = Depends(SentenceRepository),
    active_mapping_repository: ActiveMappingRepository = Depends(ActiveMappingRepository)
):
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        
        # Initialize service
        essay_service = EssayService(
            segmentation_service,
            sentence_repository,
            active_mapping_repository,
            essay_repository
        )
        
        # Get user essays
        essays_data = essay_service.get_essay_list(user_id)
        return [EssaySchema(**essay_data) for essay_data in essays_data]
    except ValidationError as e:
        print(f"Validation error: {e.json()}")
        raise HTTPException(status_code=500, detail=f"Error validating essay data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user essays: {str(e)}")

@router.post("/submitEssay")
async def submit_essay(
    content: str = Form(...),
    image: Optional[UploadFile] = File(None),
    current_user: dict = Depends(get_current_user),
    essay_repository: EssayRepository = Depends(EssayRepository),
    segmentation_service: SegmentationService = Depends(SegmentationService),
    sentence_repository: SentenceRepository = Depends(SentenceRepository),
    active_mapping_repository: ActiveMappingRepository = Depends(ActiveMappingRepository)
):
    print(f"Received content: {content}")
    print(f"Received image: {image}")
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        
        # Initialize service
        essay_service = EssayService(
            segmentation_service,
            sentence_repository,
            active_mapping_repository,
            essay_repository
        )
        
        # Create and process essay
        created_essay = await essay_service.create_and_process_essay(content, image, user_id)
        return created_essay
            
    except Exception as e:
        logger.error(f"Error submitting essay: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error submitting essay: {str(e)}")


@router.get("/essays/{essay_id}", response_model=EssayWithSentencesSchema)
async def get_essay_with_sentences(
    essay_id: int,
    current_user: dict = Depends(get_current_user),
    essay_repository: EssayRepository = Depends(EssayRepository)
):
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        
        essay = essay_repository.get_essay_by_id(essay_id)
        if not essay or essay.user_id != user_id:
            raise HTTPException(status_code=404, detail="Essay not found")
        
        return EssayWithSentencesSchema.model_validate(essay)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving essay: {str(e)}")

@router.get("/essays/{essay_id}/sentences")
async def get_essay_sentences(
    essay_id: int,
    current_user: dict = Depends(get_current_user),
    essay_repository: EssayRepository = Depends(EssayRepository),
    segmentation_service: SegmentationService = Depends(SegmentationService),
    sentence_repository: SentenceRepository = Depends(SentenceRepository),
    active_mapping_repository: ActiveMappingRepository = Depends(ActiveMappingRepository)
):
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        
        # Initialize service
        essay_service = EssayService(
            segmentation_service,
            sentence_repository,
            active_mapping_repository,
            essay_repository
        )
        
        # Get essay sentences
        return essay_service.get_essay_detail(essay_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sentence: {str(e)}")

@router.get("/sentence/{sentence_id}")
async def get_sentence(
    sentence_id: int,
    current_user: dict = Depends(get_current_user),
    sentence_repository: SentenceRepository = Depends(SentenceRepository),
    active_mapping_repository: ActiveMappingRepository = Depends(ActiveMappingRepository)
):
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        
        use_case = GetSentenceUseCase(sentence_repository, active_mapping_repository)
        res = use_case.execute(sentence_id)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sentence: {str(e)}")
    

@router.post("/mapping/addToAnki")
async def add_to_anki(
    request: AddToAnkiRequest,
    anki_service: AnkiService = Depends(AnkiService)
):
    try:
        return anki_service.add_card_to_deck("active", 
                                           request.sentence, 
                                           request.mapping_chinese, 
                                           request.mapping_wrong_english, 
                                           request.mapping_correct_english)
    except Exception as e:
        # 更新错误消息以更准确地反映错误类型
        raise HTTPException(status_code=500, detail=f"Error adding card to Anki: {str(e)}")
