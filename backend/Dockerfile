# 后端 Dockerfile — 多阶段构建
FROM python:3.12-slim AS builder

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

WORKDIR /app

# 复制依赖和源码
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY backend/ .

# 创建数据目录
RUN mkdir -p /app/data

# 环境变量（可在运行时覆盖）
ENV DATABASE_URL=sqlite+aiosqlite:///./data/agent_learning_platform.db
ENV SECRET_KEY=change-me-in-production
ENV DEBUG=false
ENV ENVIRONMENT=production
ENV DEEPSEEK_API_KEY=sk-placeholder

EXPOSE 8005

# 生产模式入口
CMD ["python", "run.py"]
