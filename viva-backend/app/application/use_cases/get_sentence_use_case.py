import sys
import os
# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录（假设 infrastructure 是在项目根目录下的一个文件夹）
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

# 将项目根目录添加到 Python 路径
sys.path.insert(0, project_root)
from domain.vo.vos import AiReviewVO, MappingVO, SentenceVO, SentenceWithMappingsVO
from infrastructure.repositories.active_mapping_repository import ActiveMappingRepository


class GetSentenceUseCase:
    def __init__(self, sentence_repository, active_mapping_repository):
        self.sentence_repository = sentence_repository
        self.active_mapping_repository = active_mapping_repository

    def execute(self, sentence_id: int) -> SentenceWithMappingsVO:
        sentence = self.sentence_repository.get_by_id(sentence_id)
        mappings = self.active_mapping_repository.get_by_sentence_id(sentence_id)

        mapping_list = []
        for mapping in mappings:
            ai_review = AiReviewVO(
                ai_review_is_correct=mapping.ai_review_is_correct, ## 这个字段似乎没啥用了
                ai_review_expression=mapping.ai_review_expression 
            )
            # 从sentence中提取对应的文本作为translation
            mapping_vo = MappingVO(
                focus_word=mapping.chinese,
                translation=mapping.user_expression,
                part_of_speech="",  # 这需要从某处获取
                definition="",  # 这需要从某处获取
                example="",  # 这需要从某处获取
                is_need_translation=True,  # 这需要根据实际情况设置
                ai_review=ai_review,
                checkingAI=False,
                usage_history=[]
            )
            mapping_list.append(mapping_vo)

        sentence_vo = SentenceVO(sentence=sentence.sentence)

        return SentenceWithMappingsVO(
            sentence=sentence_vo,
            mappingList=mapping_list
        )
    
if __name__ == "__main__":
    mappings = ActiveMappingRepository().get_by_sentence_id(61)
    print(mappings[0].ai_review_expression)