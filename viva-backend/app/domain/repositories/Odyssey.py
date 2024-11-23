from sqlalchemy import create_engine, Column, Integer, String, Text, Sequence
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, declarative_base

# 定义连接和模型基类
engine = create_engine('postgresql://root:root@localhost/root')
Base = declarative_base()

class Odyssey(Base):
    __tablename__ = 'odyssey'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, Sequence('odyssey_id_seq'), primary_key=True, comment='主键，唯一标识每条记录')
    spell = Column(Text, nullable=False, comment='单词拼写')
    rank = Column(Integer, comment='单词排名')
    audio = Column(Text, comment='单词发音音频链接')
    english_sentence = Column(Text, comment='使用该单词的英文例句')
    chinese_sentence = Column(Text, comment='英文例句的中文翻译')
    spoken_frequency = Column(Integer, comment='口语中被使用的次数')
    written_frequency = Column(Integer, comment='写作中被使用的次数')
    listening_frequency = Column(Integer, comment='听力中被听到的次数')

# 创建表格（如果尚未存在）
Base.metadata.create_all(engine)

# 创建Session用于执行操作
Session = sessionmaker(bind=engine)
session = Session()

# 创建新记录
def create_odyssey(word):
    session.add(word)
    session.commit()

# 读取记录
def read_odyssey(id):
    return session.query(Odyssey).filter_by(id=id).first()

# 更新记录
def update_odyssey(id, **kwargs):
    odyssey = session.query(Odyssey).filter_by(id=id).first()
    for key, value in kwargs.items():
        setattr(odyssey, key, value)
    session.commit()

# 删除记录
def delete_odyssey(id):
    odyssey = session.query(Odyssey).filter_by(id=id).first()
    session.delete(odyssey)
    session.commit()
def bulk_insert_odyssey(words):
    """
    批量插入单词到数据库
    :param words: 包含Odyssey对象的列表
    :return: None
    """
    try:
        # 使用bulk_save_objects进行批量插入
        session.bulk_save_objects(words)
        session.commit()
        print(f"Successfully inserted {len(words)} words.")
    except SQLAlchemyError as e:
        session.rollback()  # 发生错误时回滚
        print(f"Failed to insert words: {str(e)}")
        raise e  # 可选择重新抛出异常以便外部处理




