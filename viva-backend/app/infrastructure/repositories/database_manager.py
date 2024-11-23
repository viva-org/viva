import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

class DatabaseManager:
    _instance = None  # 用于实现单例模式

    def __new__(cls):
        # 单例模式实现：确保只创建一个 DatabaseManager 实例
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        # 初始化数据库连接
        load_dotenv()  # 加载 .env 文件中的环境变量
        db_url = os.getenv('DATABASE_URL')
        if db_url is None:
            raise ValueError("DATABASE_URL not found in environment variables.")
        
        # 创建数据库引擎，配置连接池
        self.engine = create_engine(db_url, poolclass=QueuePool, pool_size=5, max_overflow=10)
        # 创建线程安全的会话工厂
        self.SessionFactory = scoped_session(sessionmaker(bind=self.engine))

    @contextmanager
    def session_scope(self):
        # 上下文管理器，用于管理数据库会话
        session = self.SessionFactory()
        try:
            yield session  # 将会话提供给调用者
            session.commit()  # 如果没有异常，提交事务
        except:
            session.rollback()  # 如果有异常，回滚事务
            raise
        finally:
            session.close()  # 无论如何，确保关闭会话

# 创建 DatabaseManager 的全局实例
db_manager = DatabaseManager()