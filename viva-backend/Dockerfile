FROM continuumio/miniconda3:latest

WORKDIR /app

# 合并 RUN 命令减少层数
RUN apt-get update && \
    apt-get install -y pkg-config default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    # 创建环境并安装依赖
    conda env create -f environment.yml && \
    # 下载 NLTK 数据
    conda run -n viva python -c "import nltk; nltk.download('wordnet', download_dir='/usr/local/share/nltk_data'); nltk.download('omw-1.4', download_dir='/usr/local/share/nltk_data')"

# 设置环境变量
ENV PATH /opt/conda/envs/viva/bin:$PATH
ENV NLTK_DATA /usr/local/share/nltk_data

# 复制应用代码
COPY . .

# 启动命令
CMD ["conda", "run", "-n", "viva", "python", "app/main.py"]