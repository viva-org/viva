from typing import List, Optional
from assemblyai import Sentence
from pydantic import BaseModel




class UsageHistory(BaseModel):
    # 定义 UsageHistory 的字段
    # 例如：
    date: str
    context: str

class AiReviewVO(BaseModel):
    ai_review_is_correct: Optional[bool] = None
    ai_review_expression: Optional[str] = None

class MappingVO(BaseModel):
    focus_word: str
    translation: str
    part_of_speech: str
    definition: str
    example: str
    is_need_translation: bool
    ai_review: Optional[AiReviewVO] = None
    checkingAI: bool = False
    usage_history: List[UsageHistory]

class SentenceVO(BaseModel):
    sentence: str

class SentenceWithMappingsVO(BaseModel):
    sentence: SentenceVO
    mappingList: List[MappingVO]
