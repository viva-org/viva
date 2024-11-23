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

# 启动应用（确保您的后端应用监听在 8080 端口）
CMD ["conda", "run", "-n", "viva", "python", "app/main.py"]
