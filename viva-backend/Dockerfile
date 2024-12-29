FROM continuumio/miniconda3:latest

WORKDIR /app

# 复制预下载的 NLTK 数据
COPY nltk_data /root/nltk_data

# 合并 RUN 命令减少层数
RUN apt-get update && \
    apt-get install -y pkg-config default-libmysqlclient-dev build-essential && \
    rm -rf /var/lib/apt/lists/* && \
    # 创建环境并安装依赖
    conda env create -f environment.yml

# 设置环境变量
ENV PATH /opt/conda/envs/viva/bin:$PATH
ENV NLTK_DATA /root/nltk_data

# 复制应用代码
COPY . .

# 启动命令
CMD ["conda", "run", "-n", "viva", "python", "app/main.py"]