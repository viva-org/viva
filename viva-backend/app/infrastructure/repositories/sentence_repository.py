from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.entities import Essay, Sentence, EssaySentence
from infrastructure.repositories.database_manager import db_manager
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update as sql_update, func

class SentenceRepository:
    def create(self, sentence: Sentence, essay_id: int) -> Sentence:
        with db_manager.session_scope() as session:
            # 插入或获取 Sentence
            stmt = insert(Sentence.__table__).values({
                'sentence': sentence.sentence,
                'is_deleted': sentence.is_deleted
            }).on_conflict_do_update(
                index_elements=[func.md5(Sentence.__table__.c.sentence)],
                set_={'sentence': sentence.sentence}
            ).returning(Sentence.__table__)

            result = session.execute(stmt)
            db_sentence = result.fetchone()
            sentence.sentence_id = db_sentence.sentence_id

            # 创建 EssaySentence 关联
            essay_sentence = EssaySentence(
                essay_id=essay_id,
                sentence_id=sentence.sentence_id
            )
            session.add(essay_sentence)
            session.flush()

            # 刷新 sentence 对象以获取所有属性
            session.refresh(sentence)

            # 创建与会话无关的对象
            detached_sentence = Sentence(
                sentence_id=sentence.sentence_id,
                sentence=sentence.sentence,
                create_time=sentence.create_time,
                update_time=sentence.update_time,
                is_deleted=sentence.is_deleted
            )

            session.expunge_all()
            return detached_sentence

    def get_by_id(self, sentence_id: int) -> Optional[Sentence]:
        with db_manager.session_scope() as session:
            sentence = session.query(Sentence).filter(
                Sentence.sentence_id == sentence_id,
                Sentence.is_deleted == False
            ).first()
            if sentence:
                session.refresh(sentence)
                session.expunge_all()
            return sentence

    def get_by_essay_id(self, essay_id: int) -> List[Sentence]:
        with db_manager.session_scope() as session:
            sentences = session.query(Sentence).join(EssaySentence).filter(
                EssaySentence.essay_id == essay_id,
                Sentence.is_deleted == False,
                EssaySentence.is_deleted == False
            ).all()
            for sentence in sentences:
                session.refresh(sentence)
            session.expunge_all()
            return sentences

    def update(self, sentence: Sentence) -> Sentence:
        with db_manager.session_scope() as session:
            stmt = sql_update(Sentence.__table__).where(
                Sentence.__table__.c.sentence_id == sentence.sentence_id,
                Sentence.__table__.c.is_deleted == False
            ).values({
                'sentence': sentence.sentence,
                'is_deleted': sentence.is_deleted,
            }).returning(Sentence.__table__)

            result = session.execute(stmt)
            updated_row = result.fetchone()

            if updated_row is None:
                raise ValueError(f"No Sentence found with ID {sentence.sentence_id}")

            updated_sentence = Sentence(
                sentence_id=updated_row.sentence_id,
                sentence=updated_row.sentence,
                create_time=updated_row.create_time,
                update_time=updated_row.update_time,
                is_deleted=updated_row.is_deleted
            )

            session.expunge_all()
            return updated_sentence

    def delete(self, sentence_id: int) -> bool:
        with db_manager.session_scope() as session:
            sentence = session.query(Sentence).filter(
                Sentence.sentence_id == sentence_id,
                Sentence.is_deleted == False
            ).first()
            if sentence:
                sentence.is_deleted = True
                session.commit()
                return True
            return False

    def bulk_create(self, sentences: List[Sentence], essay_id: int) -> List[Sentence]:
        with db_manager.session_scope() as session:
            # 插入或获取所有 Sentence
            stmt = insert(Sentence.__table__).values([{
                'sentence': s.sentence,
                'is_deleted': s.is_deleted
            } for s in sentences])
            stmt = stmt.on_conflict_do_update(
                index_elements=[func.md5(Sentence.__table__.c.sentence)],
                set_={'sentence': stmt.excluded.sentence}
            ).returning(Sentence.__table__)

            result = session.execute(stmt)
            db_sentences = {r.sentence: r for r in result}

            # 获取已存在的句子的 ID
            existing_sentences = session.query(Sentence).filter(
                func.md5(Sentence.sentence).in_([func.md5(s.sentence) for s in sentences if s.sentence not in db_sentences])
            ).all()
            for s in existing_sentences:
                db_sentences[s.sentence] = s

            # 创建 EssaySentence 关联
            essay_sentences = [
                EssaySentence(essay_id=essay_id, sentence_id=db_sentences[s.sentence].sentence_id)
                for s in sentences
            ]
            session.bulk_save_objects(essay_sentences)

            # 更新原始 sentences 列表中的 ID 并获取完整信息
            for sentence in sentences:
                sentence.sentence_id = db_sentences[sentence.sentence].sentence_id
                db_sentence = session.query(Sentence).get(sentence.sentence_id)
                sentence.create_time = db_sentence.create_time
                sentence.update_time = db_sentence.update_time

            # 创建与会话无关的对象
            detached_sentences = [
                Sentence(
                    sentence_id=s.sentence_id,
                    sentence=s.sentence,
                    create_time=s.create_time,
                    update_time=s.update_time,
                    is_deleted=s.is_deleted
                )
                for s in sentences
            ]

            session.expunge_all()
            return detached_sentences
