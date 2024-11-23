import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()

log_level = os.getenv('LOG_LEVEL', 'INFO')
numeric_level = getattr(logging, log_level.upper(), None)
if not isinstance(numeric_level, int):
    raise ValueError(f'Invalid log level: {log_level}')


def setup_logging(log_level=numeric_level):
    # 创建 logs 目录（如果不存在）
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # 配置根日志记录器
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # 创建文件处理器
    file_handler = RotatingFileHandler(
        'logs/app.log', maxBytes=10485760, backupCount=5
    )
    file_handler.setLevel(log_level)

    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # 将处理器添加到根日志记录器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
