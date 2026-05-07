# Render 部署用 Dockerfile（构建上下文 = 仓库根目录）
# CI 用的是 backend/Dockerfile（构建上下文 = 仓库根目录，通过 file: backend/Dockerfile）

FROM python:3.12-slim

WORKDIR /app

# 安装依赖
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制后端代码
COPY backend/ .

# 复制启动脚本
COPY scripts/render-start.sh /app/render-start.sh
RUN chmod +x /app/render-start.sh

# 预创建运行时目录
RUN mkdir -p /app/data /app/logs /app/uploads /app/temp

EXPOSE 8005

# Render 启动入口（自动处理 docker 端口映射，HOST/PORT 由 Render 注入）
CMD ["/app/render-start.sh"]
