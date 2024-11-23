import logging
import os
from pathlib import Path

def setup_logging():
    # 获取项目根目录
    root_dir = Path(__file__).parent.parent.parent

    # 创建日志目录（如果不存在）
    log_dir = root_dir / 'logs'
    log_dir.mkdir(exist_ok=True)

    # 配置根日志记录器
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # 创建文件处理器
    file_handler = logging.FileHandler(log_dir / 'app.log')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # 获取根日志记录器并添加处理器
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger

# 可以在这里添加其他日志相关的配置函数
