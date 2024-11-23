import os
import shutil

# 定义源目录和目标目录
source_dir = "/Users/liuyishou/usr/obsidian_data/brain.liugongzi.org/brain/1 最近项目/++Vue学习"
target_dir = "/Users/liuyishou/usr/obsidian_data/brain.liugongzi.org/brain/2 第二大脑/1 知识/CS/软件开发/前端/vue"

# 确保目标目录存在
os.makedirs(target_dir, exist_ok=True)

# 遍历源目录中的所有文件
for filename in os.listdir(source_dir):
    source_file = os.path.join(source_dir, filename)
    target_file = os.path.join(target_dir, filename)

    # 检查是否为文件（而不是子目录）
    if os.path.isfile(source_file):
        # 移动文件
        shutil.move(source_file, target_file)
        print(f"已移动: {filename}")

print("所有文件移动完成。")