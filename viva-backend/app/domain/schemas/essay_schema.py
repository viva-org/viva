from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class SentenceSchema(BaseModel):
    sentence_id: int
    sentence: str
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None
    is_deleted: bool

class EssaySchema(BaseModel):
    essay_id: int
    user_id: str
    title: str
    content: str
    image_url: Optional[str] = None
    create_time: datetime
    update_time: datetime
    is_deleted: bool
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class EssayWithSentencesSchema(EssaySchema):
    sentences: List[SentenceSchema] = []