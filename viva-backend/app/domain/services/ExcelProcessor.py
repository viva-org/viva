import json

import pandas as pd


class ExcelProcessor:

    # 读取 Excel 文件
    def read_excel_to_dict(self, file_path):
        # 读取 Excel 文件，假设数据在第一个 sheet 上
        df = pd.read_excel(file_path)

        # 清理和预处理数据
        df[' WORD'] = df['WORD'].str.strip()  # 去除可能的前后空白

        # 使用字典来去重和存储数据
        # 以 'RANK #' 为键，'WORD' 为值
        result_dict = {}
        seen_words = set()  # 用来记录已经看到的单词，确保去重

        for _, row in df.iterrows():
            word = row['WORD']
            if word not in seen_words:  # 如果单词尚未添加
                result_dict[word.lower().strip().strip("()")] = row['RANK']
                seen_words.add(word)  # 标记该单词已处理

        self.save_dict_as_json(result_dict, 'word_frequency_table.json')
        return result_dict.__len__()

    def save_dict_as_json(self, data, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)




if __name__ == "__main__":
    ExcelProcessor().read_excel_to_dict("/Users/liuyishou/tmp/COCA初始版.xlsx")