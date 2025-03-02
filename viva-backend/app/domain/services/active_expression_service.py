import json
import logging
import re
from http.client import HTTPException
from typing import Optional, List

import jieba
from pydantic import BaseModel

from domain.services.brick_service import BrickService
from infrastructure.text.llm_agent import LLMAgent

# 获取 logger
logger = logging.getLogger(__name__)


class AICheckRequest(BaseModel):
    focus_word: str
    translation: str
    sentence: str


class AICheckResponse(BaseModel):
    ai_review_is_correct: bool
    ai_review_expression: Optional[str] = None


class ActiveExpressionService:
    def __init__(self):
        # 在这里添加一些测试日志
        logger.debug("ActiveExpressionService initialized")
        logger.info("ActiveExpressionService info log")
        logger.warning("ActiveExpressionService warning log")
        self.chat_agent = LLMAgent()

    def split_into_sentences(text: str) -> List[str]:
        # 使用正则表达式按照句号、问号、感叹号等中文标点符号分割 todo：想想怎么改进
        sentence_endings = re.compile(r'[。！？]')
        sentences = sentence_endings.split(text)
        # 去除空白句子并保留句子
        sentences = [sentence.strip() for sentence in sentences if
                     sentence.strip()]
        return sentences

    # 添加一个新的辅助函数来检查是否为标点符号
    def is_punctuation(char):
        return bool(re.match(r'[^\w\s]', char))

    async def process_essay(self, essay):
        if not essay.essay.strip():
            raise HTTPException(status_code=400, detail="作文内容不能为空。")
        if len(essay.essay) > 1500:
            raise HTTPException(status_code=400,
                                detail="作文内容不能超过1500个字。")
        # 分割作文为句子
        sentences = self.split_into_sentences(essay.essay)

        # 使用 jieba 精确模式进行分词 todo:现在'你的'会分成'你'和'的'，想想咋改进。
        words = []
        word_set = set()
        for sentence in sentences:
            segmented = jieba.lcut(sentence, cut_all=False)
            for word in segmented:
                # 过滤掉标点符号和空白字符
                if word.strip() and not self.is_punctuation(
                    word) and word not in word_set:
                    word_set.add(word)
                    words.append({
                        "chinese_word": word,
                        "sentence": sentence
                    })

        # 构建响应数据
        response = []
        for idx, word_info in enumerate(words, start=1):
            word = word_info["chinese_word"]
            sentence = word_info["sentence"]
            past_usage = BrickService().get_bricks_by_scenario(word)
            response.append({
                "id": idx,
                "chinese_word": word,
                "past_usage": past_usage,
                "current_use": None,
                "sentence": sentence
            })

        return response



if __name__ == "__main__":
    print(1)
