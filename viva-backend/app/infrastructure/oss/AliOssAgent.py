import os
import time
import logging
from typing import Tuple, Optional

import oss2
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class OssAgent:
    def __init__(self):
        # 加载环境变量
        # 正确设置相对于当前文件的路径
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        load_dotenv(dotenv_path)
        self.access_key_id = os.getenv('ACCESS_KEY_ID')
        self.access_key_secret = os.getenv('ACCESS_KEY_SECRET')
        self.bucket_name = os.getenv('BUCKET_NAME')
        self.endpoint = os.getenv('ENDPOINT')
        # 初始化认证信息
        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        # 初始化Bucket
        self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)

    def upload_file(self, file_name: str, local_path: str, 
                   retry_times: int = 3, timeout: int = 120) -> str:
        """
        上传文件到 OSS
        Args:
            file_name: OSS中的文件名
            local_path: 本地文件路径
            retry_times: 重试次数
            timeout: 超时时间（秒）
        Returns:
            Tuple[str, Optional[str]]: (url, error_message)
            - 成功时返回 (url, None)
            - 失败时返回 ("", error_message)
        """
        for attempt in range(retry_times):
            try:
                # 上传文件
                result = self.bucket.put_object_from_file(
                    file_name, 
                    local_path
                )
                
                # 检查上传是否成功
                if result.status == 200:
                    # 构建 URL
                    url = f'https://{self.bucket_name}.{self.endpoint}/{file_name}'
                    return url
                else:
                    error_msg = f"Upload failed with status: {result.status}"
                    logger.warning(f"Attempt {attempt + 1}: {error_msg}")
                    
                    # 最后一次尝试失败
                    if attempt == retry_times - 1:
                        return ""
                    
            except Exception as e:
                error_msg = f"Upload error: {str(e)}"
                logger.warning(f"Attempt {attempt + 1}: {error_msg}")
                
                # 最后一次尝试失败
                if attempt == retry_times - 1:
                    return ""
            
            # 重试前等待，使用指数退避
            if attempt < retry_times - 1:
                wait_time = min(2 ** attempt, 30)  # 最多等待30秒
                time.sleep(wait_time)
        
        return ""
    def download_file(self, file_name, local_path):
        # 下载文件
        result = self.bucket.get_object_to_file(file_name, local_path)
        return result.status

    def list_files(self, prefix=''):
        # 列出文件
        return [obj.key for obj in oss2.ObjectIterator(self.bucket, prefix=prefix)]

    def delete_file(self, file_name):
        # 删除文件
        result = self.bucket.delete_object(file_name)
        return result.status

# 使用例子
if __name__ == "__main__":
    agent = OssAgent()
    print("Uploading file...")
    status, error = agent.upload_file('Her (brilliant) idea solved the problem..mp3', '/Users/liuyishou/usr/obsidian_data/brain.liugongzi.org/brain/daily_summary_2024-09-28.txt')
    if error:
        print(f"Upload failed: {error}")
    else:
        print(f"Upload successful. URL: {status}")


