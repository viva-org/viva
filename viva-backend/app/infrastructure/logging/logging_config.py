import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

# 这些是在函数外部定义的
log_level = os.getenv('LOG_LEVEL', 'INFO')  # 默认使用 'INFO'
numeric_level = getattr(logging, log_level.upper(), None)

def setup_logging(log_level=numeric_level):  # 这里设置了默认参数
    try:
        # 使用绝对路径
        log_dir = '/app/logs'
        print(f"Creating log directory at: {log_dir}")  # 调试信息
        
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"Created log directory: {log_dir}")  # 调试信息
        
        log_file = os.path.join(log_dir, 'app.log')
        print(f"Log file path: {log_file}")  # 调试信息
        
        # 检查文件权限
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10485760,
            backupCount=5
        )
        print("Successfully created file handler")  # 调试信息
        
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
    except Exception as e:
        print(f"Error in setup_logging: {str(e)}")  # 调试信息
        raise

# 可以在这里添加其他日志相关的配置函数
