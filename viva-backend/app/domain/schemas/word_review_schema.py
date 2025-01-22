from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WordReviewSchema(BaseModel):
    id: int
    word: str
    wrong_word: str
    translation: str
    example_sentence: str
    user_id: str
    easiness: float
    interval: int
    repetitions: int
    review_datetime: datetime
    is_know: bool
    is_deleted: bool
    create_time: datetime
    update_time: datetime

    model_config = ConfigDict(from_attributes=True)
