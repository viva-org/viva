from typing import List

from pydantic import BaseModel, Field


from enum import Enum



class Revision(BaseModel):
    Round : str = Field(description="对话轮数")
    speaker_A: str = Field(description="speaker A 的原表达")
    speaker_B: str = Field(description="speaker B 的原表达")
    authentic_expression: str = Field(description="你提供的authentic expression")
    tags : str = Field(description="""{
                                            CORRECT
                                            POLITENESS_USAGE 
                                            SENTENCE_STRUCTURE_ERROR 
                                            WORD_USAGE_ERROR 
                                            SENTENCE_SEQUENCE_ERROR
                                            TENSE_ERROR
                                            VOICE_ERROR
                                            MODAL_VERB_ERROR 
                                            PRONOUN_AGREEMENT_ERROR 
                                            GRAMMAR
                                            VOCABULARY
                                            CLARITY_AND_FLUENCY
                                        }这些中的一个或者多个""")

class Suggestion(BaseModel):
    Suggestion : List[Revision] = Field(description="对每一轮对话的修改和标记")




