from typing import List, Optional, Dict
from datetime import UTC, datetime
from sqlalchemy.orm import Session, joinedload
from domain.entities.entities import Essay, User
from infrastructure.repositories.database_manager import db_manager
from sqlalchemy.orm.exc import DetachedInstanceError

class EssayRepository:
    def create_essay(self, essay: Essay, session: Session = None):
        def _create(session: Session):
            session.add(essay)
            session.flush()
            session.refresh(essay)
            return essay

        if session:
            return _create(session)
        else:
            with db_manager.session_scope() as new_session:
                created_essay = _create(new_session)
                # 创建一个新的 Essay 对象来返回，确保它与会话无关
                detached_essay = Essay(
                    essay_id=created_essay.essay_id,
                    title=created_essay.title,
                    content=created_essay.content,
                    user_id=created_essay.user_id,
                    image_url=created_essay.image_url,
                    create_time=created_essay.create_time,
                    update_time=created_essay.update_time,
                    is_deleted=created_essay.is_deleted,
                    deleted_at=created_essay.deleted_at
                )
                return detached_essay

    def get_essay_by_id(self, essay_id: int) -> Optional[Essay]:
        with db_manager.session_scope() as session:
            return session.query(Essay).filter(Essay.essay_id == essay_id, Essay.is_deleted == False).first()

    def get_essays_by_user_id(self, user_id: str) -> List[Dict]:
        with db_manager.session_scope() as session:
            essays = session.query(Essay).filter(
                Essay.user_id == user_id,
                Essay.is_deleted == False
            ).options(joinedload('*')).all()
            
            result = []
            for essay in essays:
                essay_dict = {
                    "essay_id": essay.essay_id,
                    "user_id": essay.user_id,
                    "title": essay.title,
                    "content": essay.content,
                    "image_url": essay.image_url,
                    "create_time": essay.create_time,
                    "update_time": essay.update_time,
                    "is_deleted": essay.is_deleted,
                    "deleted_at": essay.deleted_at
                }
                result.append(essay_dict)
            
            return result

    def update_essay(self, essay: Essay) -> Essay:
        with db_manager.session_scope() as session:
            existing_essay = session.query(Essay).filter(Essay.essay_id == essay.essay_id, Essay.is_deleted == False).first()
            if existing_essay:
                existing_essay.title = essay.title
                existing_essay.content = essay.content
                session.commit()
                session.refresh(existing_essay)
                return existing_essay
            raise ValueError(f"No Essay found with ID {essay.essay_id}")

    def delete_essay(self, essay_id: int) -> bool:
        with db_manager.session_scope() as session:
            essay = session.query(Essay).filter(Essay.essay_id == essay_id, Essay.is_deleted == False).first()
            if essay:
                essay.is_deleted = True
                essay.deleted_at = datetime.utcnow()
                session.commit()
                return True
            return False

    def get_all_essays(self) -> List[Essay]:
        with db_manager.session_scope() as session:
            return session.query(Essay).filter(Essay.is_deleted == False).all()

    def get_recent_essays(self, limit: int = 10) -> List[Essay]:
        with db_manager.session_scope() as session:
            return session.query(Essay).filter(Essay.is_deleted == False).order_by(Essay.create_time.desc()).limit(limit).all()

    def search_essays(self, keyword: str) -> List[Essay]:
        with db_manager.session_scope() as session:
            return session.query(Essay).filter(
                Essay.is_deleted == False,
                ((Essay.title.ilike(f'%{keyword}%')) | (Essay.content.ilike(f'%{keyword}%')))
            ).all()

    def get_essays_by_google_id(self, google_id: str) -> List[Essay]:
        with db_manager.session_scope() as session:
            return session.query(Essay).filter(Essay.user_id == google_id).all()
