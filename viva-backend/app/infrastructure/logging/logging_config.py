import logging
import os
from logging.handlers import RotatingFileHandler

# 获取环境变量中的日志级别，默认为 INFO
log_level = os.getenv('LOG_LEVEL', 'INFO')
numeric_level = getattr(logging, log_level.upper(), logging.INFO)  # 默认使用 INFO

def setup_logging(log_level=numeric_level):
    try:
        print(f"Setting up logging with level: {log_level}")  # 调试信息
        
        log_dir = '/app/logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"Created log directory: {log_dir}")
        
        log_file = os.path.join(log_dir, 'app.log')
        
        # 清理任何现有的处理器
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # 设置根日志记录器级别
        root_logger.setLevel(log_level)
        
        # 配置文件处理器
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        
        # 配置格式化器
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        # 配置控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)
        
        print(f"Logging setup completed with level: {log_level}")
        return root_logger
    except Exception as e:
        print(f"Error in setup_logging: {str(e)}")
        raise

# 可以在这里添加其他日志相关的配置函数
