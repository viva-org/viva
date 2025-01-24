import os
import requests
from dotenv import load_dotenv
from infrastructure.text.chat_gpt_agent import LLMModel

# 加载环境变量
load_dotenv()

class OpenRouterAgent(LLMModel):
    def __init__(self, model="anthropic/claude-3-sonnet"):
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        self.base_url = "https://openrouter.ai/api"
        self.model = model
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": os.getenv("YOUR_SITE_URL", "http://localhost:3000"),  # OpenRouter需要这个header
            "X-Title": os.getenv("YOUR_APP_NAME", "viva")  # 应用名称
        }

    def basic_chat(self, prompt):
        endpoint = f"{self.base_url}/v1/chat/completions"

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1000
        }

        try:
            response = requests.post(endpoint, json=payload,
                                   headers=self.headers)
            response.raise_for_status()
            raw_content = response.json()['choices'][0]['message']['content']
            print(f"###raw_content: {raw_content}")
            return self._clean_json_response(raw_content)
        except requests.RequestException as e:
            print(f"Error calling OpenRouter API: {e}")
            return None

    def _clean_json_response(self, content):
        """清理响应内容，提取纯JSON部分"""
        # 移除可能的markdown代码块标记
        content = content.replace('```json', '').replace('```', '')
        # 移除开头的说明文字（如果存在）
        if '{\n' in content or '{' in content:
            content = content[content.find('{'):]
        elif '[\n' in content or '[' in content:
            content = content[content.find('['):]
        # 移除结尾可能的额外文字
        if '}' in content:
            content = content[:content.rfind('}')+1]
        elif ']' in content:
            content = content[:content.rfind(']')+1]
        return content.strip()

# 使用示例
if __name__ == "__main__":
    agent = OpenRouterAgent()
    response = agent.basic_chat("Hello! How are you today?")
    print(response) 