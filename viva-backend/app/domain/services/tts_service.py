import os
import sys
import time

from dotenv import load_dotenv  

# 获取项目根目录路径
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(project_root)

from infrastructure.oss.AliOssAgent import OssAgent
from infrastructure.speech.eleven_labs_agent import ElevenLabsAgent
load_dotenv()

def slugify(text: str) -> str:
    """
    将文本转换为 URL 友好的格式：
    - 转换为小写
    - 将空格替换为破折号
    - 移除特殊字符
    """
    return "-".join(text.lower().split())

def tts(text: str) -> str:
    temp_file_path = None
    try:
        # 去掉可能会导致停顿的符号
        text = text.replace('(', '') \
            .replace(')', '') \
            .replace('（', '') \
            .replace('）', '') \
            .replace('"', '') \
            .replace('"', '') \
            .replace('"', '')
        print(f"Processing text: {text}")
        
        # 生成音频文件
        temp_file_path = ElevenLabsAgent().generate_and_save_audio(text, 'Leo', os.getenv('ELEVENLABS_MODEL'))
        
        # 上传到 OSS
        print("Uploading file...")
        oss_agent = OssAgent()
        # 生成文件名，限制长度为 50 个字符，并添加 .mp3 扩展名
        slug = slugify(text[:50] + ".mp3")
        url = oss_agent.upload_file(slug, temp_file_path)
        print(f"Upload successful, URL: {url}")
        
        # 等待上传完成
        time.sleep(1)
        
        return url
            
    except Exception as e:
        print(f"Error in TTS process: {str(e)}")
        return ""
        
    finally:
        # 清理临时文件
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                print(f"Temporary file {temp_file_path} removed")
            except Exception as e:
                print(f"Warning: Could not remove temporary file {temp_file_path}: {str(e)}")

if __name__ == "__main__":
    english_sentence = 'Therefore, these "small service fees" really prompt me to participate in trivial tasks.'
    print(tts(english_sentence))
    cleaned_sentence = english_sentence.replace('(', '') \
        .replace(')', '') \
        .replace('（', '') \
        .replace('）', '') \
        .replace('"', '') \
        .replace('“', '') \
        .replace('”', '')

    print(cleaned_sentence)
