import logging
import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql

class PgClient:
    def __init__(self):
        load_dotenv(".././.env")
        # 从环境变量中获取配置
        host = os.getenv('DB_HOST')  # 数据库主机地址
        user = os.getenv('DB_USER')  # 数据库用户名
        password = os.getenv('DB_PASSWORD')  # 数据库密码
        port = os.getenv('DB_PORT')  # 数据库端口，通常为字符串类型
        dbname = os.getenv("DB_DBNAME")

        self.connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.connection.cursor()

    def add_word(self, word=None, rank=None, audio=None, english_sentence=None, chinese_sentence=None,
             spoken_frequency=None, written_frequency=None, listening_frequency=None):
        # Ensure mandatory fields are provided
        if word is None and rank is None:
            logging.error("Mandatory fields 'word' or 'rank' not provided.")
            return  # Optionally, raise an exception

        # Set default values for optional parameters if None
        audio = audio or 'default_audio.mp3'
        english_sentence = english_sentence or 'No English sentence provided.'
        chinese_sentence = chinese_sentence or '未提供英文句子。'
        spoken_frequency = spoken_frequency or 0
        written_frequency = written_frequency or 0
        listening_frequency = listening_frequency or 0

        # Prepare SQL query
        sql = """
        INSERT INTO odyssey (word, rank, audio, english_sentence, chinese_sentence, spoken_frequency, written_frequency, listening_frequency)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            # Execute SQL command
            self.cursor.execute(sql, (
            word, rank, audio, english_sentence, chinese_sentence, spoken_frequency, written_frequency,
            listening_frequency))
            self.connection.commit()
            logging.info(f"Word '{word}' added successfully.")
        except Exception as e:
            # Handle errors
            logging.error(f"Failed to add word '{word}': {e}")
            self.connection.rollback()

    def update_word(self, id, **kwargs):
        updates = ', '.join([f"{k} = %s" for k in kwargs])
        values = list(kwargs.values())
        values.append(id)
        sql = f"UPDATE vocabulary_usage SET {updates} WHERE id = %s"
        self.cursor.execute(sql, values)
        self.connection.commit()

    def delete_word(self, id):
        sql = "DELETE FROM vocabulary_usage WHERE id = %s"
        self.cursor.execute(sql, (id,))
        self.connection.commit()

    def get_word(self, id):
        sql = "SELECT * FROM vocabulary_usage WHERE id = %s"
        self.cursor.execute(sql, (id,))
        result = self.cursor.fetchone()
        return result

    def close(self):
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    PgClient().add_word(word="good", audio="https://odyssey-liugongzi.oss-cn-beijing.aliyuncs.com/Her (brilliant) idea solved the problem..mp3")