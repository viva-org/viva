# infrastructure/repositories/active_mapping_repository.py

from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.entities import ActiveMapping
from infrastructure.repositories.database_manager import db_manager
from sqlalchemy.dialects.postgresql import insert

class ActiveMappingRepository:
    def create(self, active_mapping: ActiveMapping) -> ActiveMapping:
        with db_manager.session_scope() as session:
            session.add(active_mapping)
            session.flush()
            session.refresh(active_mapping)
            session.expunge_all()
            return active_mapping

    def get_by_id(self, mapping_id: int) -> Optional[ActiveMapping]:
        with db_manager.session_scope() as session:
            mapping = session.query(ActiveMapping).filter(ActiveMapping.mapping_id == mapping_id, ActiveMapping.is_deleted == False).first()
            if mapping:
                session.refresh(mapping)
                session.expunge_all()
            return mapping

    def get_by_sentence_id(self, sentence_id: int) -> List[ActiveMapping]:
        with db_manager.session_scope() as session:
            mappings = session.query(ActiveMapping).filter(ActiveMapping.sentence_id == sentence_id, ActiveMapping.is_deleted == False).all()
            for mapping in mappings:
                session.refresh(mapping)
            session.expunge_all()
            return mappings

    def update(self, active_mapping: ActiveMapping) -> ActiveMapping:
        with db_manager.session_scope() as session:
            existing_mapping = session.query(ActiveMapping).filter(ActiveMapping.mapping_id == active_mapping.mapping_id, ActiveMapping.is_deleted == False).first()
            if existing_mapping:
                for key, value in active_mapping.__dict__.items():
                    if key != 'mapping_id' and hasattr(existing_mapping, key):
                        setattr(existing_mapping, key, value)
                session.commit()
                session.refresh(existing_mapping)
                session.expunge_all()
                return existing_mapping
            raise ValueError(f"No ActiveMapping found with ID {active_mapping.mapping_id}")

    def delete(self, mapping_id: int) -> bool:
        with db_manager.session_scope() as session:
            active_mapping = session.query(ActiveMapping).filter(ActiveMapping.mapping_id == mapping_id, ActiveMapping.is_deleted == False).first()
            if active_mapping:
                active_mapping.is_deleted = True
                session.commit()
                return True
            return False

    def bulk_create(self, active_mappings: List[ActiveMapping]) -> List[ActiveMapping]:
        with db_manager.session_scope() as session:
            # Prepare the values for bulk insert
            values = [{
                'sentence_id': am.sentence_id,
                'focus_start': am.focus_start,
                'focus_end': am.focus_end,
                'user_expression': am.user_expression,
                'ai_review_is_correct': am.ai_review_is_correct,
                'ai_review_expression': am.ai_review_expression,
                'is_deleted': am.is_deleted
            } for am in active_mappings]

            # Perform bulk insert
            stmt = insert(ActiveMapping.__table__).values(values)
            stmt = stmt.on_conflict_do_nothing()  # In case of conflict, do nothing
            result = session.execute(stmt)

            # Fetch the inserted records
            inserted_ids = result.inserted_primary_key_rows
            if inserted_ids:
                inserted_mappings = session.query(ActiveMapping).filter(
                    ActiveMapping.mapping_id.in_([id[0] for id in inserted_ids])
                ).all()
                
                # Refresh and detach the inserted mappings
                for mapping in inserted_mappings:
                    session.refresh(mapping)
                session.expunge_all()
                
                return inserted_mappings
            
            return []
