from dataclasses import dataclass
import json
import logging
import os
from typing import List, Dict, Optional
import anthropic
from dotenv import load_dotenv
import re
import sys
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from langchain_anthropic import Anthropic, ChatAnthropic
from enum import Enum

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录（假设 infrastructure 是在项目根目录下的一个文件夹）
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

# 将项目根目录添加到 Python 路径
sys.path.insert(0, project_root)

# 现在你可以导入 infrastructure 模块了
from infrastructure.english.coca import CocaService
from infrastructure.english.word_net import WordNetService
from infrastructure.text.llm_agent import LLMAgent

# 加载环境变量
load_dotenv()
# 获取 logger
logger = logging.getLogger(__name__)

class POS(str, Enum):
    NOUN = 'n'
    VERB = 'v'
    ADJECTIVE = 'a'
    ADVERB = 'r'

class Word(BaseModel):
    english: str = Field(description="english segmentation word I give you")
    pos: POS = Field(
        description="Part of speech tag. Must be one of: "
                   "n (noun), v (verb), a (adjective), r (adverb). "
                   "These tags align with WordNet's POS system."
    )
    chinese: str = Field(description="corresponding chinese word from original sentence")

class WordWithIndex(BaseModel):     
    english: str = Field(description="english segmentation word I give you")
    pos: POS = Field(description="I give you the pos of the word")
    chinese: str = Field(description="corresponding chinese word from original sentence")
    start: int = Field(description="chinese word index start in original sentence")
    len: int = Field(description="chinese word length")
class WordWithIndexAndSynonym(BaseModel):     
    english: List[str] = Field(description="english synonyms")
    pos: POS = Field(description="the pos of the word")
    chinese: str = Field(description="corresponding chinese word from original sentence")
    start: int = Field(description="chinese word index start in original sentence")
    len: int = Field(description="chinese word length")
class SegmentationResult(BaseModel):
    original: str = Field(description="The original Chinese sentence")
    translation: str = Field(description="The English translation of the sentence")
    words: List[Word] = Field(description="List of word mappings with English and Chinese")
class FinalSegmentationResult(BaseModel):
    original: str = Field(description="The original Chinese sentence")
    translation: str = Field(description="The English translation of the sentence")
    words: List[WordWithIndex] = Field(description="List of word mappings with English and Chinese")
class SynonymExpansionResult(BaseModel):
    original: str = Field(description="The original Chinese word")
    translation: str = Field(description="The English translation of the sentence")
    words: List[WordWithIndexAndSynonym] = Field(description="List of word mappings with English and Chinese")
class WordTransformationResult(BaseModel):
    words_transformation: List[str] = Field(description="converted words from the original words")

class SegmentationService:

    def __init__(self):
        self.chat_agent = LLMAgent(model_type="openrouter")
        self.parser2 = PydanticOutputParser(pydantic_object=SegmentationResult)
        self.parser3 = PydanticOutputParser(pydantic_object=FinalSegmentationResult)
        self.parser4 = PydanticOutputParser(pydantic_object=WordTransformationResult)

    def validate_essay(self, essay: str) -> None:
        """
        验证作文内容是否符合要求
        """
        if not essay.strip():
            raise ValueError("作文内容不能为空。")
        if len(essay) > 1500:
            raise ValueError("作文内容不能超过1500个字。")

    def split_into_sentences(self, essay: str) -> List[str]:
        """
        将作文分割成句子
        """
        # 使用正则表达式分割句子，这里的模式可能需要根据实际情况调整
        sentences = re.split(r'([。！？])', essay)
        # 将分割符加回句子中
        sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2] + [''])]
        return [s.strip() for s in sentences if s.strip()]

    def segment_sentence(self, sentence: str) -> SynonymExpansionResult:
        process1_result = self._translate2English_and_segment(sentence)
        process2_result = self._fill_chinese_segment(process1_result)
        process3_result = self._fill_chinese_segment_index(process2_result)
        expanded_result = self.expand_synonyms(process3_result)
        return expanded_result
        
    def _translate2English_and_segment(self, sentence: str):
        """
        第一步：使用LLM分词
        """
        sentence = sentence.strip()
        prompt_file = os.getenv("SEGMENT_PROMPT_FILE1")
        if not prompt_file:
            raise ValueError("SEGMENT_PROMPT_FILE is not set in environment variables.")
        prompt = open(prompt_file, "r", encoding='utf-8').read()
        prompt = prompt.replace("{sentence}", sentence)
        response = self.chat_agent.chat(prompt)
        logger.info(f"Segment phase1 LLM original response: {response}")
        return response

    def _fill_chinese_segment(self, process1_result) -> SegmentationResult:
        """
        第二步：使用LLM填充中文分词
        """
        prompt_file = os.getenv("SEGMENT_PROMPT_FILE2")
        if not prompt_file:
            raise ValueError("SEGMENT_PROMPT_FILE is not set in environment variables.")
        
        with open(prompt_file, "r", encoding='utf-8') as file:
            prompt_template = file.read()

        prompt = prompt_template.format(
            process1_result=str(process1_result),
            format_instructions=self.parser2.get_format_instructions()
        )

        try:
            output = self.chat_agent.chat(prompt)
            logger.error(f"Segment phase2 LLM original response: {output}")
            result = self.parser2.parse(output)
            logger.info(f"Successfully parsed result: {result}")

            return result
        except Exception as e:
            logger.error(f"Error in filling Chinese segment: {str(e)}")
            return None

    def _fill_chinese_segment_index(self, process2_result) -> FinalSegmentationResult:
        """
        第三步：使用LLM填充中文分词索引
        """
        prompt_file = os.getenv("SEGMENT_PROMPT_FILE3")
        if not prompt_file:
            raise ValueError("SEGMENT_PROMPT_FILE3 is not set in environment variables.")
        prompt_template = open(prompt_file, "r", encoding='utf-8').read()
        prompt = prompt_template.format(
            process2_result=str(process2_result),
            format_instructions=self.parser3.get_format_instructions()
        )

        try:
            output = self.chat_agent.chat(prompt)
            logger.info(f"Segment phase3 LLM original response: {output}")
            result = self.parser3.parse(output)
            logger.info(f"Successfully parsed result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in filling Chinese segment index: {str(e)}")
            return None
        
    def expand_synonyms(self, segmentation_result: FinalSegmentationResult) -> SynonymExpansionResult:
        """
        第四步：扩展分词结果到所属的WordNet synset里的 synonyms同义词，并去掉其中词频大于 20000 名的
        """
        
        expanded_result = SynonymExpansionResult(
            original=segmentation_result.original,
            translation=segmentation_result.translation,
            words=[]
        )
        
        for word in segmentation_result.words:
            # 使用新方法获取同义词，排除原词的其他形式
            synonyms = WordNetService.get_synonyms_by_context(word.english
            , word.pos, segmentation_result.original)
            
            # 过滤出高频同义词（词频排名<=2000的词）
            high_freq_synonyms = {
                syn for syn in synonyms 
                if CocaService.get_word_rank(syn) <= 2000
            }
            # 将剩下的词变为和原词同样的形式
            transformed_synonyms = []
            if high_freq_synonyms:
                transformed_synonyms = self._transform_word_to_same_form(word.english, word.pos
                                                                     , list(high_freq_synonyms))
            # 将原词放在第一位
            synonyms_list = [word.english] + transformed_synonyms

            expanded_word = WordWithIndexAndSynonym(
                english=synonyms_list,
                pos=word.pos,
                chinese=word.chinese,
                start=word.start,
                len=word.len
            )
            
            expanded_result.words.append(expanded_word)
        
        return expanded_result

    def _transform_word_to_same_form(self, word: str, pos: str, synonyms: List[str]) -> List[str]:
        """
        将同义词转换为与原始单词相同的形式
        Args:
            word: 原始单词
            synonyms: 需要转换的同义词列表
        Returns:
            转换后的同义词列表
        """
        # 获取原始单词的原型
        word_lemma = WordNetService.get_word_lemma(word, pos)
        word_transformation = word
        print(f"word_lemma: {word_lemma}, word_transformation: {word_transformation}")
        prompt_file = os.getenv("SEGMENT_PROMPT_FILE4")
        if not prompt_file:
            raise ValueError("SEGMENT_PROMPT_FILE4 is not set in environment variables.")
        prompt_template = open(prompt_file, "r", encoding='utf-8').read()

        prompt = prompt_template.format(
            ref_word_lemma=word_lemma,
            ref_word_transformation=word_transformation,
            words=synonyms,
            format_instructions=self.parser4.get_format_instructions()
        )
        try:    
            output = self.chat_agent.chat(prompt)
            result = self.parser4.parse(output)
            return result.words_transformation
        except Exception as e:
            logger.error(f"Error in transforming synonyms form: {str(e)}")
            return None
        
if __name__ == "__main__":
    # 创建服务实例
    segmentation_service = SegmentationService()
    
    # 测试用例1：动词变化
    print("\n测试用例1：动词变化")
    result1 = segmentation_service._transform_word_to_same_form(
        word="playing", 
        pos="v",
        synonyms=["run", "swim"]
    )
    print(f"原词: playing")
    print(f"同义词: ['run', 'swim']")
    print(f"转换结果: {result1}")
    
    # 测试用例2：名词复数
    print("\n测试用例2：名词复数")
    result2 = segmentation_service._transform_word_to_same_form(
        word="dogs",
        pos="n",
        synonyms=["cat", "bird"]
    )
    print(f"原词: dogs")
    print(f"同义词: ['cat', 'bird']")
    print(f"转换结果: {result2}")
    
    # 测试用例3：空列表处理
    print("\n测试用例3：空列表处理")
    result3 = segmentation_service._transform_word_to_same_form(
        word="test",
        pos="n",
        synonyms=[]
    )
    print(f"原词: test")
    print(f"同义词: []")
    print(f"转换结果: {result3}")
    
