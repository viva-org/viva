from datetime import datetime, time
from typing import List, Optional, Dict, Type

from sqlalchemy.orm import Session, joinedload

from domain.entities.entities import WordReview
from infrastructure.repositories.database_manager import db_manager


class WordReviewRepository:
    def create_word_review(self, word_review: WordReview, session: Session = None):
        def _create(session: Session):
            session.add(word_review)
            session.flush()
            session.refresh(word_review)
            return word_review

        if session:
            return _create(session)
        else:
            with db_manager.session_scope() as new_session:
                created_word_review = _create(new_session)
                # 创建一个新的对象来返回，确保它与会话无关
                detached_word_review = WordReview(
                    id=created_word_review.id,
                    word=created_word_review.word,
                    wrong_word=word_review.wrong_word,
                    translation=created_word_review.translation,
                    example_sentence=created_word_review.example_sentence,
                    user_id=created_word_review.user_id,
                    easiness=created_word_review.easiness,
                    interval=created_word_review.interval,
                    repetitions=word_review.repetitions,
                    review_datetime=created_word_review.review_datetime,
                    is_know=created_word_review.is_know,
                    is_deleted=created_word_review.is_deleted,
                    create_time=created_word_review.create_time,
                    update_time=created_word_review.update_time,
                )
                return detached_word_review

    def get_word_review_by_id(self, id: int, session: Session = None) -> Optional[WordReview]:
        def _get(session: Session):
            return session.query(WordReview).filter(
                WordReview.id == id,
                WordReview.is_deleted == False
            ).options(joinedload('*')).first()

        if session:
            return _get(session)
        else:
            with (db_manager.session_scope() as session):
                return _get(session)

    def get_word_reviews_by_user_id(self, user_id: str, session: Session = None) -> List[Dict]:
        def _get(session: Session):
            word_reviews = session.query(WordReview).filter(
                WordReview.user_id == user_id,
                WordReview.is_deleted == False
            ).options(joinedload('*')).all()
            result = []
            for word_review in word_reviews:
                word_review_dict = {
                    "id": word_review.id,
                    "word": word_review.word,
                    "wrong_word": word_review.wrong_word,
                    "translation": word_review.translation,
                    "example_sentence": word_review.example_sentence,
                    "user_id": word_review.user_id,
                    "easiness": word_review.easiness,
                    "interval": word_review.interval,
                    "review_datetime": word_review.review_datetime,
                    "is_know": word_review.is_know,
                    "is_deleted": word_review.is_deleted,
                    "create_time": word_review.create_time,
                    "update_time": word_review.update_time,
                }
                result.append(word_review_dict)
            return result

        if session:
            return _get(session)
        else:
            with db_manager.session_scope() as session:
                return _get(session)

    def update_word_review(self, word_review: WordReview, session: Session = None) -> Optional[WordReview]:
        def _update(session: Session):
            existing_word_review = session.query(WordReview).filter(WordReview.id == word_review.id,
                                                                    WordReview.is_deleted == False).options(
                joinedload('*')).first()
            if word_review:
                existing_word_review.easiness = word_review.easiness
                existing_word_review.interval = word_review.interval
                existing_word_review.review_datetime = word_review.review_datetime
                existing_word_review.is_know = word_review.is_know
                session.commit()
                session.refresh(existing_word_review)
                return existing_word_review
            raise ValueError(f"No WordReview found with ID {word_review.id}")

        if session:
            return _update(session)
        else:
            with db_manager.session_scope() as session:
                return _update(session)

    def delete_word_review(self, id: int, session: Session = None) -> bool:
        def _delete(session: Session):
            word_review = session.query(WordReview).filter(WordReview.id == id, WordReview.is_deleted == False).first()
            if word_review:
                word_review.is_deleted = True
                session.commit()
                return True
            return False

        if session:
            return _delete(session)
        else:
            with db_manager.session_scope() as session:
                return _delete(session)

    def get_all_word_review(self, session: Session = None) -> Optional[List[WordReview]]:
        def _get(session: Session):
            return session.query(WordReview).filter(WordReview.is_deleted == False).all()

        if session:
            return _get(session)
        else:
            with db_manager.session_scope() as session:
                return _get(session)

    def get_today_word_review_list(self, user_id: str, limit: int = 200, session: Session = None) -> List[
        Type[WordReview]]:
        def _get(session: Session):
            return session.query(WordReview).filter(
                WordReview.user_id == user_id,
                WordReview.is_deleted == False,
                WordReview.is_know == False,
                (WordReview.review_datetime <= datetime.now()) | (WordReview.repetitions == 0)
            ).order_by(WordReview.review_datetime.asc()).limit(limit).all()

        if session:
            return _get(session)
        else:
            with db_manager.session_scope() as session:
                return _get(session)

    def get_today_word_review_count(self, user_id: str, session: Session = None) -> int:
        def _get(session: Session):
            return session.query(WordReview).filter(
                WordReview.user_id == user_id,
                WordReview.is_deleted == False,
                WordReview.is_know == False,
                WordReview.review_datetime <= datetime.combine(datetime.now(), time.max)
            ).count()

        if session:
            return _get(session)
        else:
            with db_manager.session_scope() as session:
                return _get(session)

    def get_know_word_review_count(self, user_id: str, session: Session = None) -> int:
        def _get(session: Session):
            return session.query(WordReview).filter(
                WordReview.user_id == user_id,
                WordReview.is_deleted == False,
                WordReview.is_know == True,
            ).count()

        if session:
            return _get(session)
        else:
            with db_manager.session_scope() as session:
                return _get(session)

    def search_word_reviews(self, user_id: str, keyword: str, session: Session = None) -> List[Type[WordReview]]:
        def _get(session: Session):
            query = session.query(WordReview).filter(
                WordReview.user_id == user_id,
                WordReview.is_deleted == False
            )
            if keyword:
                query = query.filter(
                    (WordReview.word.ilike(f'%{keyword}%')) | (WordReview.example_sentence.ilike(f'%{keyword}%')))
            return query.all()

        if session:
            return _get(session)
        else:
            with db_manager.session_scope() as session:
                return _get(session)

    def get_word_review_by_google_id(self, google_id: str, session: Session = None) -> List[Type[WordReview]]:
        def _get(session: Session):
            return session.query(WordReview).filter(WordReview.user_id == google_id).all()

        if session:
            return _get(session)
        else:
            with db_manager.session_scope() as session:
                return _get(session)
