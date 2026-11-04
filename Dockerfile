# 基础镜像：带 Python 3.12 的精简系统
FROM python:3.12-slim

# 容器里的工作目录
WORKDIR /app

# 先拷依赖清单装包（这样改代码时不用重新装包，构建更快）
COPY requirements.txt .
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

# 再拷全部代码
COPY . .

# 启动命令，0.0.0.0 才能从容器外访问
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]