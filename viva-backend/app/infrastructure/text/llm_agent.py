import sys
import os

from dotenv import load_dotenv

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录（假设 infrastructure 是在项目根目录下的一个文件夹）
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

# 将项目根目录添加到 Python 路径
sys.path.insert(0, project_root)

# 现在你可以导入 infrastructure 模块了
from infrastructure.text.chat_gpt_agent import ChatGptAgent
from infrastructure.text.claude_agent import ClaudeAgent
from infrastructure.text.open_router_agent import OpenRouterAgent
# 加载环境变量
load_dotenv()


class LLMAgent:
    def __init__(self, model_type=None):
        if model_type is None or model_type == "":
            model_type = os.getenv("LLM_MODEL_TYPE", "openrouter").lower()
        else:
            model_type = model_type.lower()

        print(f"Initializing LLMAgent with model_type: {model_type}")

        if model_type == "chatgpt":
            self.model = ChatGptAgent()
        elif model_type == "claude":
            self.model = ClaudeAgent()
        elif model_type == "openrouter":
            self.model = OpenRouterAgent()
        else:
            raise ValueError(
                f"Unsupported model type: {model_type}. Supported types are 'chatgpt' and 'claude' and 'openrouter'.")

    def chat(self, prompt):
        return self.model.basic_chat(prompt)


# 使用示例
if __name__ == "__main__":
    # 从环境变量或配置文件中读取模型类型
    model_type = os.getenv("LLM_MODEL_TYPE", "openrouter")  # 默认使用 openrouter

    agent = LLMAgent(model_type)
    response = agent.chat("Hello! How are you today?")
    print(response)
