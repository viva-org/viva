FROM continuumio/miniconda3:latest

WORKDIR /app

RUN mkdir -p /app/logs && chmod 777 /app/logs

# 安装系统依赖
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制环境文件
COPY environment.yml .

# 创建 conda 环境
RUN conda env create -f environment.yml

# 激活环境
SHELL ["conda", "run", "-n", "viva", "/bin/bash", "-c"]

# 复制应用代码
COPY . .

# 下载必要的nltk数据
RUN conda run -n viva python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
# 确保pip包正确安装
RUN conda run -n viva pip install --no-cache-dir oss2
# 设置环境变量
ENV PATH /opt/conda/envs/viva/bin:$PATH

# 启动命令
CMD ["conda", "run", "-n", "viva", "python", "app/main.py"]