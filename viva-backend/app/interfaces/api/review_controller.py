import logging
from datetime import datetime

from anthropic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from domain.entities.entities import WordReview, WordReviewLog
from domain.schemas.word_review_schema import WordReviewSchema
from domain.vo.api_response import api_response
from infrastructure.repositories.database_manager import get_db
from infrastructure.repositories.word_review_log_repository import WordReviewLogRepository
from infrastructure.repositories.word_review_repository import WordReviewRepository
from infrastructure.supermemo.supermemo_service import SupermemoService
from interfaces.service.jwt_service import get_current_user

router = APIRouter()

logger = logging.getLogger(__name__)

supermemoService = SupermemoService()


class WordReviewRequest(BaseModel):
    id: int | None = None
    word: str | None = None
    wrong_word: str | None = None
    quality: int | None = None
    translation: str | None = None
    example_sentence: str | None = None
    is_know: bool | None = False


@router.post("/word")
async def add_word(
        word_review_request: WordReviewRequest,
        current_user: dict = Depends(get_current_user),
        word_review_repository: WordReviewRepository = Depends(WordReviewRepository),
        word_review_log_repository: WordReviewLogRepository = Depends(WordReviewLogRepository),
        session: Session = Depends(get_db)
):
    """
    添加新单词
    """
    print(f"Received word: {word_review_request}")
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        word_review = WordReview(word=word_review_request.word,
                                 wrong_word=word_review_request.wrong_word,
                                 user_id=user_id,
                                 translation=word_review_request.translation,
                                 example_sentence=word_review_request.example_sentence)
        word_review = supermemoService.first_review(0, word_review)
        word_review = word_review_repository.create_word_review(word_review, session)
        word_review_log = WordReviewLog(word_id=word_review.id,
                                        user_id=user_id,
                                        easiness=word_review.easiness,
                                        interval=word_review.interval,
                                        repetitions=word_review.repetitions,
                                        review_datetime=word_review.review_datetime)
        word_review_log_repository.create_word_review_log(word_review_log, session)
        if word_review is not None:
            return api_response(data=WordReviewSchema.from_orm(word_review))
        else:
            return api_response(status=1, message="Add wordReview failed", data=None)
    except Exception as e:
        logger.error(f"Error submitting word:{str(e)}")
        raise HTTPException(status_code=500, detail=f"Error submitting word: {str(e)}")


@router.put("/word")
async def update_word(
        word_review_request: WordReviewRequest,
        current_user: dict = Depends(get_current_user),
        word_review_repository: WordReviewRepository = Depends(WordReviewRepository),
        word_review_log_repository: WordReviewLogRepository = Depends(WordReviewLogRepository),
        session: Session = Depends(get_db)
):
    """
    更新单词信息(提交复习结果)
    """
    print(f"Received word: {word_review_request}")
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")

        word_review = word_review_repository.get_word_review_by_id(word_review_request.id, session)
        if not word_review or word_review.user_id != user_id:
            raise HTTPException(status_code=404, detail="WordReview not found")
        word_review = supermemoService.review(word_review_request.quality, word_review)
        word_review = word_review_repository.update_word_review(word_review, session)
        word_review_log = WordReviewLog(word_id=word_review.id,
                                        user_id=user_id,
                                        easiness=word_review.easiness,
                                        interval=word_review.interval,
                                        repetitions=word_review.repetitions,
                                        review_datetime=word_review.review_datetime)
        word_review_log_repository.create_word_review_log(word_review_log, session)
        if word_review:
            return api_response(data=WordReviewSchema.from_orm(word_review))
        else:
            return api_response(status=1, message="Update wordReview failed", data=None)
    except Exception as e:
        logger.error(f"Error submitting word:{str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating word: {str(e)}")


@router.post("/word/known")
async def know_word(
        word_review_request: WordReviewRequest,
        current_user: dict = Depends(get_current_user),
        word_review_repository: WordReviewRepository = Depends(WordReviewRepository),
        session: Session = Depends(get_db)
):
    """
    标记熟知
    """
    print(f"Received word: {word_review_request}")
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")

        word_review = word_review_repository.get_word_review_by_id(word_review_request.id, session)
        if not word_review or word_review.user_id != user_id:
            raise HTTPException(status_code=404, detail="WordReview not found")
        word_review.is_know = word_review_request.is_know
        word_review = word_review_repository.update_word_review(word_review, session)
        if word_review:
            return api_response(data=WordReviewSchema.from_orm(word_review))
        else:
            return api_response(status=1, message="Update wordReview failed", data=None)
    except Exception as e:
        logger.error(f"Error submitting word:{str(e)}")
        raise HTTPException(status_code=500, detail=f"Error updating word: {str(e)}")


@router.get("/word/{word_id}")
async def get_word(
        word_id: int,
        current_user: dict = Depends(get_current_user),
        word_review_repository: WordReviewRepository = Depends(WordReviewRepository),
        session: Session = Depends(get_db)
):
    """
    获取单词复习详细信息
    """
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")

        word_review = word_review_repository.get_word_review_by_id(word_id, session)
        if not word_review or word_review.user_id != user_id:
            raise HTTPException(status_code=404, detail="WordReview not found")
        return api_response(data=WordReviewSchema.from_orm(word_review))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving word_review: {str(e)}")


@router.get("/word")
async def get_all_word(
        keyword: str = Query(None),
        current_user: dict = Depends(get_current_user),
        word_review_repository: WordReviewRepository = Depends(WordReviewRepository),
        session: Session = Depends(get_db)
):
    """
    获取所有单词信息
    """
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")

        word_reviews = word_review_repository.search_word_reviews(user_id, keyword, session)
        return api_response(data=[WordReviewSchema.from_orm(word_review) for word_review in word_reviews])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving word_review: {str(e)}")


@router.get("/word/review/list")
async def get_word_review_list(
        current_user: dict = Depends(get_current_user),
        word_review_repository: WordReviewRepository = Depends(WordReviewRepository),
        session: Session = Depends(get_db)
):
    """
    获取今日复习单词列表
    """
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")

        word_reviews = word_review_repository.get_today_word_review_list(user_id, session=session)
        return api_response(data=[WordReviewSchema.from_orm(word_review) for word_review in word_reviews])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving word_review list: {str(e)}")


@router.get("/word/review/count")
async def get_word_review_count(
        current_user: dict = Depends(get_current_user),
        word_review_repository: WordReviewRepository = Depends(WordReviewRepository),
        session: Session = Depends(get_db)
):
    """
    获取今日复习单词数量
    """
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")

        return api_response(data=word_review_repository.get_today_word_review_count(user_id, session))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving word_review count: {str(e)}")


@router.get("/word/review/stat")
async def get_word_review_stat(
        current_user: dict = Depends(get_current_user),
        word_review_repository: WordReviewRepository = Depends(WordReviewRepository),
        word_review_log_repository: WordReviewLogRepository = Depends(WordReviewLogRepository),
        session: Session = Depends(get_db)
):
    """
    获取用户复习单词统计数据
    """
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        stat = {
            "todayReviewCount": word_review_log_repository.get_today_review_count_by_user_id(user_id, session),
            "todayNeedReviewCount": word_review_repository.get_today_word_review_count(user_id, session),
            "totalKnowWordReviewCount": word_review_repository.get_know_word_review_count(user_id, session)
        }
        return api_response(data=stat)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving word_review count: {str(e)}")


@router.get("/word/review/dayStat")
async def get_word_review_day_stat(
        start_date=Query(),
        end_date=Query(),
        current_user: dict = Depends(get_current_user),
        word_review_log_repository: WordReviewLogRepository = Depends(WordReviewLogRepository),
        session: Session = Depends(get_db)
):
    """
    获取热力图数据
    """
    try:
        user_id = current_user.get('id')
        if not user_id:
            raise HTTPException(status_code=400, detail="Invalid user ID")
        date_format = "%Y-%m-%d"
        return api_response(data=word_review_log_repository.get_word_reviews_log_by_user_id_and_date(
            user_id,
            datetime.strptime(start_date, date_format),
            datetime.strptime(end_date, date_format),
            session))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving word_review count: {str(e)}")
