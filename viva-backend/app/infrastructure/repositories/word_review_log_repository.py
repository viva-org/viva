from datetime import datetime, time
from typing import Optional, Dict, List, Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from domain.entities.entities import WordReviewLog
from infrastructure.repositories.database_manager import db_manager


class WordReviewLogRepository:
    def create_word_review_log(self, word_review_log: WordReviewLog, session: Session = None):
        def _create(session: Session):
            session.add(word_review_log)
            session.flush()
            session.refresh(word_review_log)
            return word_review_log

        if session:
            return _create(session)
        else:
            with db_manager.session_scope() as new_session:
                created_word_review_log = _create(new_session)
                # 创建一个新的对象来返回，确保它与会话无关
                detached_word_review_log = WordReviewLog(
                    id=created_word_review_log.id,
                    word_id=created_word_review_log.word_id,
                    user_id=created_word_review_log.user_id,
                    easiness=created_word_review_log.easiness,
                    interval=created_word_review_log.interval,
                    repetitions=created_word_review_log.repetitions,
                    review_datetime=created_word_review_log.review_datetime,
                    create_time=created_word_review_log.create_time,
                )
                return detached_word_review_log

    def get_word_review_log_by_id(self, id: int, session: Session = None) -> Optional[WordReviewLog]:
        def _get(session: Session):
            return session.query(WordReviewLog).filter(WordReviewLog.id == id).first()

        if session:
            return _get(session)
        else:
            with db_manager.session_scope() as session:
                return _get(session)

    def get_today_review_count_by_user_id(self, user_id: str, session: Session = None) -> int:
        def _get(session: Session):
            now = datetime.now()
            return session.query(WordReviewLog.word_id).filter(
                WordReviewLog.user_id == user_id,
                WordReviewLog.create_time >= datetime.combine(now, time.min),
                WordReviewLog.create_time <= datetime.combine(now, time.max),
            ).distinct().count()

        if session:
            return _get(session)
        else:
            with db_manager.session_scope() as session:
                return _get(session)

    def get_word_reviews_log_by_user_id_and_date(self, user_id: str, start_date: datetime, end_date: datetime,
                                                 session: Session = None) -> List[Dict[str, Any]]:
        def _get(session: Session):
            query = (
                session.query(
                    func.date(WordReviewLog.create_time).label('date'),
                    func.count().label('count')
                )
                .filter(
                    WordReviewLog.user_id == user_id,
                    WordReviewLog.create_time >= datetime.combine(start_date, time.min),
                    WordReviewLog.create_time <= datetime.combine(end_date, time.max)
                )
                .group_by(func.date(WordReviewLog.create_time))
                .order_by('date')
            )
            results = query.all()
            return [{'date': result.date, 'value': result.count} for result in results]

        if session:
            return _get(session)
        else:
            with db_manager.session_scope() as session:
                return _get(session)

    def get_today_review_word_count(self, user_id: str, session: Session = None) -> int:
        def _get(session: Session):
            today = datetime.now().date()
            query = session.query(WordReviewLog).filter(
                WordReviewLog.user_id == user_id,
                func.date(WordReviewLog.review_datetime) == today
            )
            return query.count()

        if session:
            return _get(session)
        else:
            with db_manager.session_scope() as session:
                return _get(session)
