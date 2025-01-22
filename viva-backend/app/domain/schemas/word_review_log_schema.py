from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WordReviewLogSchema(BaseModel):
    id: int
    word_id: int
    user_id: str
    easiness: float
    interval: int
    repetitions: int
    review_datetime: datetime
    create_time: datetime

    model_config = ConfigDict(from_attributes=True)
