import json
import os
import time
import dotenv
from datetime import datetime

from jmespath.functions import Functions
from openai import OpenAI
dotenv.load_dotenv()
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

LOGFILE = 'AssistantLog.md'  # We'll store all interactions in this file
AI_RESPONSE = '-AIresponse-'  # GUI event key for Assistant responses


def show_json(data):
    """
    Converts a Python object to a JSON formatted string and prints it.

    Args:
    data: A Python object (e.g., dict, list) to be converted into JSON.
    """
    # Convert the Python object to a JSON formatted string
    json_data = json.dumps(data, indent=4)

    # Print the JSON formatted string
    print(json_data)

class Assistant:
    def __init__(self):
        # 环境变量
        while OpenAI.api_key is None:
            input("Hey! Couldn't find OPENAI_API_KEY. Put it in .env then press any key to try again...")
            dotenv.load_dotenv()
            OpenAI.api_key = os.getenv('OPENAI_API_KEY')

        # 初始化要素
        self.client = OpenAI()
        self.assistant = None
        self.run = None
        self.message = None

        # 初始化assistant
        self.assistant = self.client.beta.assistants.create(
            name="English Assistant",
            instructions="Format your responses in markdown. you are a anssistant who can output 128k tokens",
            model="gpt-4-turbo-preview",
        )

        # 初始化thread
        self.create_AI_thread()

    def create_AI_thread(self):
        """Creates an OpenAI Assistant thread, which maintains context for a user's interactions."""
        print('Creating llm_client thread...')
        self.thread = self.client.beta.threads.create()
        print(self.thread)
        with open(LOGFILE, 'a+') as f:
            f.write(f'# {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\nBeginning {self.thread.id}\n\n')

    def wait_on_run(self):
        """Waits for an OpenAI llm_client run to finish and handles the response."""
        print('Waiting for llm_client response...')
        while self.run.status == "queued" or self.run.status == "in_progress":
            self.run = self.client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=self.run.id)
            time.sleep(1)
        if self.run.status == "requires_action":
            print(f'\nASSISTANT REQUESTS {len(self.run.required_action.submit_tool_outputs.tool_calls)} TOOLS:')
            tool_outputs = []
            for tool_call in self.run.required_action.submit_tool_outputs.tool_calls:
                tool_call_id = tool_call.id
                name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                print(f'\nAssistant requested {name}({arguments})')
                output = getattr(Functions, name)(**arguments)
                tool_outputs.append({"tool_call_id": tool_call_id, "output": json.dumps(output)})
                print(f'\n\tReturning {output}')
            self.run = self.client.beta.threads.runs.submit_tool_outputs(thread_id=self.thread.id,
                                                                         run_id=self.run.id,
                                                                         tool_outputs=tool_outputs)
            self.wait_on_run()
        else:
            # Get messages added after our last user message
            new_messages = self.client.beta.threads.messages.list(thread_id=self.thread.id, order="asc",
                                                                  after=self.message.id)
            with open(LOGFILE, 'a+') as f:
                f.write('\n**Assistant**:\n')
                for m in new_messages:
                    f.write(m.content[0].text.value)
                f.write('\n\n---\n')

    def send_message(self, message_text: str):
        """
        Send a message to the llm_client.

        Parameters
        ----------
        window : PySimpleGUI.window
            GUI element with .write_event_value() callback method, which will receive the Assistant's response.
        message_text : str
        """
        self.message = self.client.beta.threads.messages.create(self.thread.id,role="user",content=message_text)
        print('\nSending:\n' + str(self.message))
        with open(LOGFILE, 'a+') as f:
            f.write(f'**User:** `{message_text}`\n')

        self.run = self.client.beta.threads.runs.create(thread_id=self.thread.id, assistant_id=self.assistant.id)
        self.wait_on_run()



if __name__ == "__main__":
    assistant = Assistant()  # 懒汉式初始化 assistant和thread
    with open("/infrastructure/text/llm_client/instruction.txt", "r") as f:
        instruction = f.read()
    with open("/Users/liuyishou/Library/Mobile Documents/com~apple~CloudDocs/B-口语之路/utterances.txt", "r") as f:
        utterances = f.read()
    assistant.send_message(instruction + utterances)
    assistant.send_message("继续接着从你处理到的位置矫正，直到矫正完我的所有轮的英语表达")


