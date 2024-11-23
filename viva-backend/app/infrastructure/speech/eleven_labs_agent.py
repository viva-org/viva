import os
from dotenv import load_dotenv
from elevenlabs import play
from elevenlabs.client import ElevenLabs

class ElevenLabsAgent:
    def __init__(self):
        # 加载环境变量
        load_dotenv("./.env")
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        self.client = ElevenLabs(api_key=self.api_key)

    def generate_and_save_audio(self, text, voice, model):
        print('text:', text)
        audio = self.client.generate(
            text=text,
            voice=voice,
            model=model
        )
        file_path = 'audio/' + text[:50] + '.mp3'
        # 检查路径是否存在，不存在则创建
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # 保存音频文件
        with open(file_path, 'wb') as f:
            for chunk in audio:
                f.write(chunk)
        
        return file_path

    def generate_and_play_audio(self, text, voice, model):
        audio = self.client.generate(
            text=text,
            voice=voice,
            model=model
        )
        play(audio)

