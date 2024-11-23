import os
from abc import abstractmethod, ABC

from dotenv import load_dotenv
from langchain.output_parsers import PydanticOutputParser
from openai import OpenAI

from domain.entities.revision import Suggestion


class LLMModel(ABC):
    @abstractmethod
    def basic_chat(self, prompt):
        pass
load_dotenv()  # 加载 .env 文件中的环境变量

class ChatGptAgent(LLMModel):
    def __init__(self):
        """
        初始化ChatGptAgent类的实例。
        """
        
        self.api_key = os.getenv('OPENAI_API_KEY')  # 从环境变量中获取 API 密钥
        self.client = OpenAI(api_key=self.api_key)

    def generate_sentence_for_word(self, word):
        """
        为给定的单词生成十五字以内的英文句子

        参数:
        - word: 需要生成句子的单词。

        返回:
        - 生成的句子。
        """
        client = OpenAI(api_key=self.api_key)
        completion = client.chat.completions.create(
            model="o1-preview",
            messages=[
                {"role": "system",
                 "content": "You are an assistant who can compose sentences with given words or phrases or sentences, you are expert in Chinese and English."},
                {"role": "user",
                 "content": f"如果“{word}” 是一个单词或者短语，那么用其造一个十五字以内的英文句子，并把“{word}” 对应的英文用（）围起来，；如果“{word}” 是一句话的话，把它原封不动返回给我就好，返回结果中不应当有括号"}
            ]
        )
        sentence = completion.choices[0].message.content
        return sentence

    def translate_english_sentence(self, sentence):
        """
        将句子从中文翻译到英文

        参数:
        - sentence: 中文句子。

        返回:
        - 生成的句子。
        """
        client = OpenAI(api_key=self.api_key)
        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system",
                 "content": "You are an assistant who can translate English sentences to authentic Chinese sentences, you are expert in Chinese and English."},
                {"role": "user",
                 "content": f"将“{sentence}” 翻译为地道的中文，如果其中有（）围起来的部分，你应该在给出的英文翻译中也括号括出对应的内容"}
            ]
        )
        translation = completion.choices[0].message.content
        return translation

    def cluster_words(self, words):
        """
        为给定的单词生成一个二十字以内的中文句子。

        参数:
        - word: 需要生成句子的单词。

        返回:
        - 生成的句子。
        """
        client = OpenAI(api_key=self.api_key)
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system",
                 "content": "You are an assistant who are expert in English."},
                {"role": "user",
                 "content": f"根据我提供的单词和其用法“{words}”，将其中的近义词找出来，并分成若干组"}
            ]
        )
        result = completion.choices[0].message.content
        return result

    def discriminate_synonyms(self, words):
        """
        为给定的单词生成一个二十字以内的中文句子。

        参数:
        - word: 需要生成句子的单词。

        返回:
        - 生成的句子。
        """
        client = OpenAI(api_key=self.api_key)
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system",
                 "content": "You are an assistant who are expert in English."},
                {"role": "user",
                 "content": f"给出这些同义词{words}对应的中文例句，并辨析"}
            ]
        )
        result = completion.choices[0].message.content
        return result

    def polish_expression(self, utterances):
        client = OpenAI(api_key=self.api_key)
        assistant = client.beta.assistants.create(
            name="English Tutor",
            instructions="You are a personal math tutor. Write and run code to answer math questions.",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-turbo-preview"
        )
        thread = client.beta.threads.create()
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="I need to solve the equation `3x + 11 = 14`. Can you help me?"
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
            instructions="Please address the user as Jane Doe. The user has a premium account."
        )

        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )

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
                          原始对话：
                           """)

        parser = PydanticOutputParser(pydantic_object=Suggestion)

        # prompt = PromptTemplate(
        #     template="Answer the user query.\n{format_instructions}\n{query}\n",
        #     input_variables=["query"],
        #     partial_variables={"format_instructions": },
        # )

        _input = role + parser.get_format_instructions() + instruction + str(
            utterances)

        print(_input)
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system",
                 "content": "You are an assistant who are expert in English."},
                {"role": "user", "content": _input}
            ]
        )
        # 继续对话
        completion = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system",
                 "content": "You are an assistant who are expert in English."},
                {"role": "user", "content": "继续"}
            ]
        )
        result = completion.choices[0].message.content
        return result

    def basic_chat(self, message):
        """
        与 AI 进行基本对话。

        参数:
        - message: 用户发送给 AI 的消息。

        返回:
        - AI 的回复。
        """
        try:
            completion = self.client.chat.completions.create(
                model= os.getenv("LLM_MODEL_NAME_FOR_BASIC_CHAT"),
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant."},
                    {"role": "user", "content": message}
                ]
            )
            return completion.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in chat_with_ai: {e}")
            return "Sorry, I encountered an error while processing your request."


if __name__ == "__main__":
    agent = ChatGptAgent()
    print(agent.basic_chat("你好"))
