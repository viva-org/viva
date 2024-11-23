import logging
import os
from contextlib import contextmanager
from pathlib import Path
from typing import List

from dotenv import load_dotenv

# 获取当前文件的目录
base_dir = Path(__file__).resolve().parent.parent.parent

# 构造 .env 文件的路径（假设它在项目根目录）
env_path = base_dir / '.env'

# 加载 .env 文件
load_dotenv(dotenv_path=env_path)

from sqlalchemy import create_engine, func, cast, text
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.postgresql import JSONB

from domain.entities.brick import Brick

# 定义模型基类
Base = declarative_base()

logger = logging.getLogger(__name__)

class BrickRepository:

    def __init__(self, db_url=None):
        if db_url is None:
            db_url = os.getenv('DATABASE_URL')
            if db_url is None:
                logger.error(
                    "Database URL not provided and not found in environment variables.")
                raise ValueError(
                    "Database URL not provided and not found in environment variables.")

        logger.info(f"Initializing BrickRepository with database URL: {db_url}")
        self.engine = create_engine(db_url, poolclass=QueuePool, pool_size=5,
                                    max_overflow=10)
        self.Session = scoped_session(sessionmaker(bind=self.engine))

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def get_all_ids(self) -> List:
        with self.session_scope() as session:
            ids = [result.id for result in session.query(Brick).all()]
        return ids

    def get_all_bricks(self) -> List[Brick]:
        with self.session_scope() as session:
            bricks = [result for result in session.query(Brick).all()]
        return bricks

    def create_brick(self, word):
        with self.session_scope() as session:
            session.add(word)

    def get_brick_by_id(self, id):
        with self.session_scope() as session:
            return session.query(Brick).filter_by(id=id).first()

    def get_brick_by_spelling(self, spelling) -> Brick:
        with self.session_scope() as session:
            return session.query(Brick).filter_by(spelling=spelling).first()

    def update_brick(self, brick):
        with self.session_scope() as session:
            existing_brick = session.query(Brick).filter_by(id=brick.id).first()
            if existing_brick:
                existing_brick.spelling = brick.spelling
                existing_brick.ranking = brick.ranking
                existing_brick.pronunciation = brick.pronunciation
                existing_brick.english_sentence = brick.english_sentence
                existing_brick.chinese_sentence = brick.chinese_sentence
                existing_brick.spoken_frequency = brick.spoken_frequency
                existing_brick.written_frequency = brick.written_frequency
                existing_brick.listening_frequency = brick.listening_frequency
                session.commit()
            else:
                raise ValueError(f"No Brick found with ID {brick.id}")

    def delete_brick(self, id):
        with self.session_scope() as session:
            brick = session.query(Brick).filter_by(id=id).first()
            session.delete(brick)
            session.commit()

    def bulk_insert_brick(self, words):
        with self.session_scope() as session:
            try:
                session.bulk_save_objects(words)
                session.commit()
                print(f"Successfully inserted {len(words)} words.")
            except SQLAlchemyError as e:
                session.rollback()  # 发生错误时回滚
                print(f"Failed to insert words: {str(e)}")
                raise e  # 可选择重新抛出异常以便外部处理

    # 为某个单词，新增一个active_use_scenario
    def update_active_use_scenario(self, spelling, chinese_scenario):
        with self.session_scope() as session:
            existing_brick = session.query(Brick).filter_by(
                spelling=spelling).first()
            if not existing_brick:
                raise ValueError(f"No Brick found with spelling {spelling}")

            if existing_brick.active_use_scenario is None:
                existing_brick.active_use_scenario = {}

            # 将 JSONB 字段转换为 Python 字典
            scenarios = existing_brick.active_use_scenario if isinstance(
                existing_brick.active_use_scenario, dict) else {}

            # 如果中文场景已存在，增加计数；否则，初始化为1
            if chinese_scenario in scenarios:
                scenarios[chinese_scenario] += 1
            else:
                scenarios[chinese_scenario] = 1

            # 使用 SQLAlchemy 的 func.jsonb_build_object 构建 JSONB 对象
            jsonb_pairs = [(key, value) for key, value in scenarios.items()]
            existing_brick.active_use_scenario = cast(
                func.jsonb_build_object(
                    *[item for pair in jsonb_pairs for item in pair]),
                JSONB
            )

            session.commit()

            # 验证更新
            session.refresh(existing_brick)
            print(
                f"Updated active_use_scenario: {existing_brick.active_use_scenario}")


    # 根据某个中文场景，找到使用过的英文单词，以及使用次数
    def get_bricks_by_chinese_word(self, chinese_word):
        with self.session_scope() as session:
            query = text("""
                SELECT spelling, active_use_scenario
                FROM brick
                WHERE active_use_scenario ? :chinese_word
            """)

            result = session.execute(query, {'chinese_word': chinese_word})

            matches = []
            for row in result:
                spelling = row.spelling
                scenarios = row.active_use_scenario
                usage_count = scenarios.get(chinese_word, 0)
                matches.append({
                    'spelling': spelling,
                    'chinese_word': chinese_word,
                    'usage_count': usage_count
                })

        if not matches:
            print(f"No bricks found containing the Chinese word: {chinese_word}")
        else:
            print(f"Found {len(matches)} bricks containing the Chinese word: {chinese_word}")
            for match in matches:
                print(f"English word: {match['spelling']}, Chinese word: {match['chinese_word']}, Usage count: {match['usage_count']}")

        return matches

if __name__ == "__main__":
    
    db_url = 'postgresql://root:root@localhost/root'
    repo = BrickRepository(db_url)
