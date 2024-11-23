import logging
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, BigInteger, JSON
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from infrastructure.english.coca import get_word_rank
from domain.services.tts_service import tts
from domain.services.translate_service import translate_english_sentence

Base = declarative_base()

class Brick(Base):
    __tablename__ = 'brick'
    __table_args__ = {'schema': 'public'}

    id = Column(Integer, primary_key=True, server_default="nextval('odyssey_id_seq'::regclass)", comment='主键，唯一标识每条记录')
    spelling = Column(Text, unique=True, nullable=False, comment='单词拼写')
    ranking = Column(Integer, comment='单词排名')
    pronunciation = Column(Text, comment='单词发音音频链接')
    english_sentence = Column(Text, comment='使用该单词的英文例句')
    chinese_sentence = Column(Text, comment='英文例句的中文翻译')
    spoken_frequency = Column(Integer, comment='口语中被使用的次数')
    written_frequency = Column(Integer, comment='写作中被使用的次数')
    listening_frequency = Column(Integer, comment='听力中被听到的次数')
    create_time = Column(TIMESTAMP, nullable=False, server_default=func.current_timestamp(), comment='创建时间')
    update_time = Column(TIMESTAMP, onupdate=func.current_timestamp(), comment='更新时间')
    anki_active_id = Column(BigInteger, comment='Anki主动复习卡片ID')
    anki_passive_id = Column(BigInteger, comment='Anki被动复习卡片ID')
    source = Column(String, comment='来源')
    deleted = Column(Boolean, comment='是否已删除')
    english_sentence_toefl = Column(Text, comment='托福风格的英语句子')
    chinese_sentence_toefl = Column(Text, comment='english_sentence_toefl的中文翻译')
    active_use_scenario = Column(JSON, comment='被我主动使用的场景,比如我想到苹果就可以主动说出apple')
    active_vocabulary = Column(Boolean, comment='设为TRUE，表示这是主动词汇')

    def __str__(self):
        return (f"Brick(id={self.id}, spelling={self.spelling}, ranking={self.ranking}, "
                f"pronunciation={self.pronunciation}, english_sentence={self.english_sentence}, "
                f"chinese_sentence={self.chinese_sentence}, spoken_frequency={self.spoken_frequency}, "
                f"written_frequency={self.written_frequency}, listening_frequency={self.listening_frequency}, "
                f"create_time={self.create_time}, update_time={self.update_time}, "
                f"anki_active_id={self.anki_active_id}, anki_passive_id={self.anki_passive_id}, "
                f"source={self.source}, deleted={self.deleted}, "
                f"english_sentence_toefl={self.english_sentence_toefl}, "
                f"chinese_sentence_toefl={self.chinese_sentence_toefl}, "
                f"active_use_scenario={self.active_use_scenario}, "
                f"active_vocabulary={self.active_vocabulary})")

    def __eq__(self, other):
        if not isinstance(other, Brick):
            return NotImplemented
        return self.spelling == other.spelling

    def __hash__(self):
        return hash(self.spelling)

    def update_fields(self):
        if self.ranking is None:
            self.ranking = get_word_rank(self.spelling)
        if (self.english_sentence is not None) and (self.chinese_sentence is None):
            self.chinese_sentence = translate_english_sentence(self.english_sentence)
        if ((self.pronunciation is None or not self.pronunciation.startswith('https://'))
                and self.english_sentence is not None and self.english_sentence != ''):
            self.pronunciation = tts(self.english_sentence)
            print(f"生成发音 {self.spelling} - {self.pronunciation}")
            logging.warning(f"生成发音 {self.spelling} - {self.pronunciation}")
            print(self)

