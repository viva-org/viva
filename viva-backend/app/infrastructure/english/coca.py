import json
from pathlib import Path
from typing import Dict, Optional

class CocaService:
    # 静态类属性
    _word_rank_dict: Dict[str, int] = {}
    _is_initialized: bool = False
    
    @classmethod
    def _initialize(cls) -> None:
        """初始化词频字典（仅在第一次使用时加载）"""
        if not cls._is_initialized:
            # 获取当前文件所在目录
            current_dir = Path(__file__).parent
            file_path = current_dir / 'word_frequency_table.json'
            
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    cls._word_rank_dict = json.load(file)
                cls._is_initialized = True
            except FileNotFoundError:
                raise FileNotFoundError(f"词频表文件未找到: {file_path}")
            except json.JSONDecodeError:
                raise ValueError(f"词频表文件格式错误: {file_path}")

    @classmethod
    def get_word_rank(cls, word: str) -> int:
        """获取单词在 COCA 语料库中的词频排名
        
        Args:
            word: 要查询的���词
        
        Returns:
            int: 词频排名，如果未找到则返回 66666
        """
        if not cls._is_initialized:
            cls._initialize()
        return cls._word_rank_dict.get(word.lower(), 66666)

    @classmethod
    def is_common_word(cls, word: str, threshold: int = 5000) -> bool:
        """判断是否为常用词（基于词频排名）
        
        Args:
            word: 要判断的单词
            threshold: 词频排名阈值，默认前5000名为常用词
        
        Returns:
            bool: 是否为常用词
        """
        rank = cls.get_word_rank(word)
        return rank <= threshold

    @classmethod
    def get_frequency_level(cls, word: str) -> str:
        """获取单词的使用频率级别
        
        Args:
            word: 要查询的单词
            
        Returns:
            str: 频率级别描述
        """
        rank = cls.get_word_rank(word)
        if rank <= 1000:
            return "极高频词"
        elif rank <= 3000:
            return "高频词"
        elif rank <= 5000:
            return "中高频词"
        elif rank <= 10000:
            return "中频词"
        elif rank <= 20000:
            return "中低频词"
        else:
            return "低频词"
        
# 在类定义之外添加包装函数
def get_word_rank(word: str) -> int:
    """获取单词词频排名的包装函数"""
    return CocaService.get_word_rank(word)

def is_common_word(word: str, threshold: int = 5000) -> bool:
    """判断是否为常用词的包装函数"""
    return CocaService.is_common_word(word, threshold)

def get_frequency_level(word: str) -> str:
    """获取词频级别的包装函数"""
    return CocaService.get_frequency_level(word)

if __name__ == "__main__":
    
    print(CocaService.get_word_rank("happy"))
    print(CocaService.is_common_word("happy"))
    print(CocaService.get_frequency_level("happy"))