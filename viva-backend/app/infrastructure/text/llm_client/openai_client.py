# 加载 .env 文件中的环境变量
import json
import os
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser, CommaSeparatedListOutputParser
from langchain.prompts import PromptTemplate
from domain.entities.revision import Suggestion
import openai

class OpenAIClient():

    def polish_expression(self, utterances):
        load_dotenv()
        openai_api_key = os.getenv('OPENAI_API_KEY')
        model_name = os.getenv('OPENAI_MODEL_NAME')
        temperature = 0.3
        model = openai.OpenAI()

        role = """
                我是一位中国人，正在寻求帮助以提高我的英语口语能力。
                我想展示一段我和我的英语老师之间的对话（我是发言者B）。
                能否请你帮忙指出其中的错误或者听起来对于母语为英语的人不自然的短语,并给出地道的表达方式,另外将这种修改归类打上我提供的tags？
                请复制我的输入文本，并在B的发言后插入你的纠正或建议，类似这样
                A: 我们称它们为菌株。
                B: 菌株。
                authentic_expression: [你的纠正或建议]
                tags：修改的类型
                
                详细的格式是这样：    
                """
        instruction = ("""
                       下面是我们的对话,你需要对每一轮都提出建议和标记，
                       如果觉得不需要修改authentic_expression可以为none，tags打上CORRECT即可
                       你返回的json文本中应该包括了我所有给你的对话内容
                        """)

        parser = PydanticOutputParser(pydantic_object=Suggestion)

        # prompt = PromptTemplate(
        #     template="Answer the user query.\n{format_instructions}\n{query}\n",
        #     input_variables=["query"],
        #     partial_variables={"format_instructions": },
        # )

        _input = role + parser.get_format_instructions() + instruction + str(utterances)
        with get_openai_callback() as cb:
            response1 = openai.Completion.create(
                engine=model_name,
                prompt=_input,
                temperature=temperature,
                max_tokens=1500
            )
            print(cb)

        with(open("_output1.txt", "w") as f):
            f.write(response1)

        with get_openai_callback() as cb:
            response2 = openai.Completion.create(
                engine=model_name,
                prompt="继续",
                temperature=temperature,
                max_tokens=1500
            )
            print(cb)

        with(open("_output2.txt", "w") as f):
            f.write(response2)

        # start = _output.find('{')
        # end = _output.rfind('}') + 1
        # jsonl_data = _output[start:end]
        # print(jsonl_data)
        #
        # # 首先，我们需要将这个字符串转换为一个有效的 JSON 格式
        # # 因为这个字符串有多个 JSON 对象，但没有包裹在一个列表中，我们需要先将它们包裹在一个列表中
        # json_like_str = "[" + jsonl_data.strip().rstrip(',') + "]"
        #
        # # 解析 JSON 字符串
        # data = json.loads(json_like_str)
        #
        # # 转换为无花括号和引号的字符串
        # output_str = ""
        # for entry in data:
        #     for key, value in entry.items():
        #         output_str += f"{key} says: {value}\n"
        #     output_str += "\n"
        #
        # with open("utterances_with_suggestion.txt", "w") as f:
        #     f.write(output_str)
        return "utterances_with_suggestion.txt"


if __name__ == "__main__":

    OpenAIClient().polish_expression("content")