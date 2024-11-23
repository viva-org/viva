import os

import requests
from dotenv import load_dotenv

from infrastructure.text.chat_gpt_agent import LLMModel

# 加载环境变量
load_dotenv()


class ClaudeAgent(LLMModel):
    def __init__(self):
        self.api_key = os.getenv("CLAUDE_API_KEY")
        self.base_url = "https://api.gptsapi.net"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def basic_chat(self, prompt):
        endpoint = f"{self.base_url}/v1/chat/completions"

        payload = {
            "model": "claude-3-sonnet-20240229",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }

        try:
            response = requests.post(endpoint, json=payload,
                                     headers=self.headers)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except requests.RequestException as e:
            print(f"Error calling Claude API: {e}")
            return None


# 使用示例
if __name__ == "__main__":
    agent = ClaudeAgent()
    response = agent.chat_with_ai("Hello, Claude! How are you today?")
    print(response)
