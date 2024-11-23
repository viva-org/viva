FROM continuumio/miniconda3:latest

WORKDIR /app

# 复制环境文件
COPY environment.yml .

# 创建 conda 环境
RUN conda env create -f environment.yml

# 激活环境
SHELL ["conda", "run", "-n", "viva", "/bin/bash", "-c"]

# 复制应用代码
COPY . .

EXPOSE 8000

# 启动应用
CMD ["conda", "run", "-n", "viva", "python", "app/main.py"]
