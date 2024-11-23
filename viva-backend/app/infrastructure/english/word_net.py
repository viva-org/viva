import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from nltk.corpus import wordnet as wn
from typing import List, Dict, Any
from collections import defaultdict
import textwrap
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from pydantic import Field
from pydantic import BaseModel
import json

load_dotenv()


class Input(BaseModel):
    word : str
    context : str
    synsets : str
class Synset(BaseModel):
    synset_name : str = Field(description="the synset name that is the most suitable for the word")
    definition : str = Field(description="the definition of the synset")
class ChooseSynsetOutput(BaseModel):
    synsets : List[Synset]


class WordNetService:


    # 静态类属性
    POS_MAP = {
        'n': 'NOUN',
        'v': 'VERB',
        'a': 'ADJECTIVE',
        's': 'ADJECTIVE SATELLITE',
        'r': 'ADVERB'
    }
    _lemmatizer = WordNetLemmatizer()
    _stemmer = PorterStemmer()
    _llm = ChatOpenAI(model = os.getenv("LLM_MODEL_NAME_FOR_BASIC_CHAT")
                                     , temperature=0.4, openai_api_key=os.getenv("OPENAI_API_KEY")) 
    _parser1 = PydanticOutputParser(pydantic_object=ChooseSynsetOutput)
    
    
    @staticmethod
    def get_word_lemma(word: str, pos: str = "n") -> str:
        """获取单词的原型  decided -> decide """
        return WordNetService._lemmatizer.lemmatize(word, pos)

    
    @staticmethod
    def get_word_stem(word: str) -> str:
        """获取单词的词干 decided -> decid 不一定是完整的单词 """
        return WordNetService._stemmer.stem(word.lower())

    @staticmethod
    def explore_word(word: str, pos: str = None) -> Dict[str, Any]:
        """静态方法：探索单词的所有关系"""
        results = defaultdict(list)
        synsets = wn.synsets(word, pos=pos) if pos else wn.synsets(word)
        
        if not synsets:
            return {"error": f"No synsets found for word: {word}"}
        
        for synset in synsets:
            sense_info = {
                "pos": WordNetService.POS_MAP.get(synset.pos(), "UNKNOWN"),
                "definition": synset.definition(),
                "examples": synset.examples(),
                "lemmas": [lemma.name() for lemma in synset.lemmas()],
                "relations": WordNetService._get_relations(synset)
            }
            results[synset.name()].append(sense_info)
        
        return dict(results)

    @staticmethod
    def _get_relations(synset) -> Dict[str, List[str]]:
        """静态方法：获取同义词集的所有关系"""
        relations = defaultdict(list)
        
        # 同义词集关系
        if synset.hypernyms():
            relations["hypernyms"].extend(hyp.name() for hyp in synset.hypernyms())
        
        if synset.hyponyms():
            relations["hyponyms"].extend(hyp.name() for hyp in synset.hyponyms())
        
        if synset.part_meronyms():
            relations["part_meronyms"].extend(m.name() for m in synset.part_meronyms())
        
        if synset.part_holonyms():
            relations["part_holonyms"].extend(h.name() for h in synset.part_holonyms())
            
        if synset.member_meronyms():
            relations["member_meronyms"].extend(m.name() for m in synset.member_meronyms())
            
        if synset.member_holonyms():
            relations["member_holonyms"].extend(h.name() for h in synset.member_holonyms())
            
        if synset.substance_meronyms():
            relations["substance_meronyms"].extend(m.name() for m in synset.substance_meronyms())
            
        if synset.substance_holonyms():
            relations["substance_holonyms"].extend(h.name() for h in synset.substance_holonyms())

        # 动词特有关系
        if synset.pos() == 'v':
            if synset.entailments():
                relations["entailments"].extend(ent.name() for ent in synset.entailments())
            if synset.causes():
                relations["causes"].extend(cause.name() for cause in synset.causes())

        # 词级关系
        for lemma in synset.lemmas():
            if lemma.antonyms():
                relations["antonyms"].extend(ant.name() for ant in lemma.antonyms())
            if lemma.derivationally_related_forms():
                relations["derivationally_related"].extend(
                    drf.name() for drf in lemma.derivationally_related_forms()
                )

        return dict(relations)

    @staticmethod
    def get_synonyms_by_context(word: str, pos: str = None, context: str = None) -> set:
        """根据单词和所在语境，找到对应的 synset，以及里面的 synonyms """
        synsets = wn.synsets(word, pos=pos) if pos else wn.synsets(word)
        prompt_file = os.getenv("WORDNET_PROMPT_FILE1")
        if not prompt_file:
            raise ValueError("SEGMENT_PROMPT_FILE is not set in environment variables.")
        
        with open(prompt_file, "r") as file:
            prompt_template = file.read()
        prompt = ChatPromptTemplate.from_template(prompt_template)

        # 将 synsets 信息转换为字符串
        synsets_str = json.dumps([
            {
                "name": synset.name(),
                "definition": synset.definition(),
                "lemmas": [lemma.name() for lemma in synset.lemmas()]
            }
            for synset in synsets
        ], indent=2)

        print("synsets_str: ", synsets_str)  # 用于调试
        
        messages = prompt.format_messages(
            word=word,
            context=context,
            synsets=str(synsets_str),
            format_instructions=WordNetService._parser1.get_format_instructions()
        )

        try:
            llm_response = WordNetService._llm.invoke(messages)
            output = WordNetService._parser1.parse(llm_response.content)
            synonyms = set()
            print("output: ", output)
            for synset in output.synsets:
                synset_name = synset.synset_name    
                original_stem = WordNetService.get_word_stem(word)

                synset = wn.synset(synset_name)
                for lemma in synset.lemmas():
                    synonym = lemma.name()
                    # 如果词干相同但不是完全相同的词，则跳过
                    if WordNetService.get_word_stem(synonym) == original_stem:
                        continue
                    synonyms.add(synonym)
            
            return synonyms
        except Exception as e:
            print(f"Error processing response: {e}")
            print(f"Response content: {llm_response.content}")
            return set()
    
    @staticmethod
    def get_synsets(word: str, pos: str = None) -> List[str]:
        synsets = wn.synsets(word, pos=pos) if pos else wn.synsets(word)
        return [synset.name() for synset in synsets]
    

    
if __name__ == "__main__":
    print(WordNetService.get_synsets("persist", "v"))
    
