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


    async def ai_check(self, request: AICheckRequest) -> AICheckResponse:
        english_word = request.focus_word
        chinese_word = request.translation
        sentence = request.sentence

        prompt = f"""
        我把中文句子：{sentence}中的这个词"{chinese_word}"翻译为了：{english_word}
        这样合适吗？
        
        如果合适那么请回复"is_correct": true，如果不合适，那请告诉我"{chinese_word}"
        在这个语境下正确的英文翻译，注意时态、语态、单复数,拼写错误等常见的中国人容易犯的错误
        
        请以JSON格式回复，包含以下字段：
        - is_correct: 布尔值，表示用法是否正确
        - correction: 如果不正确，提供更好的表达方式；如果正确，则为null

        示例回复：
        {{"is_correct": false, "correction": "正确的英文翻译"}}
        或
        {{"is_correct": true, "correction": null}}

        请只返回JSON，不要有其他解释。
        """

        response = self.chat_agent.chat(prompt)
        logger.error(f"log: Raw AI response: {response}")

        try:
            # 首先尝试解析整个响应为 JSON
            result = json.loads(response)
        except json.JSONDecodeError:
            # 如果失败，尝试提取被 ```json 包围的内容
            json_match = re.search(r'```json\s*(.*?)\s*```', response,
                                   re.DOTALL)
            if json_match:
                try:
                    result = json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    logger.error(
                        f"Failed to parse JSON from matched content: {json_match.group(1)}")
                    return AICheckResponse(is_correct=False,
                                           correction="无法解析AI响应。请重试。")
            else:
                logger.error("No valid JSON found in the response")
                return AICheckResponse(is_correct=False,
                                       correction="无法解析AI响应。请重试。")

        # 验证结果包含所需的字段
        if 'is_correct' not in result or 'correction' not in result:
            logger.error(f"Missing required fields in parsed result: {result}")
            return AICheckResponse(is_correct=False,
                                   correction="AI响应格式不正确。请重试。")

        if result['is_correct']:
            BrickService().upsert_active_use_scenario(english_word,
                                                      chinese_word)
            logger.error(f"AI检查通过，更新使用次数")
        else:
            logger.error(f"AI检查不通过，不更新使用次数")

        return AICheckResponse(
            ai_review_is_correct=result['is_correct'],
            ai_review_expression=result['correction']
        )


if __name__ == "__main__":
    print(1)
