#!/bin/bash
# Render startup script
# 将 Render 提供的 PostgreSQL URL (postgres://...) 转换为 SQLAlchemy async 格式

set -e

echo "[render-start] Bootstrapping..."

# 转换 DATABASE_URL: postgres:// → postgresql+asyncpg://
if [ -n "$DATABASE_URL" ]; then
    echo "[render-start] DATABASE_URL detected, converting to async format..."
    export DATABASE_URL=$(echo "$DATABASE_URL" | sed 's|^postgres://|postgresql+asyncpg://|; s|^postgresql://|postgresql+asyncpg://|')
    echo "[render-start] DATABASE_URL=$(echo $DATABASE_URL | sed 's|://.*|://***|')"
else
    echo "[render-start] WARNING: DATABASE_URL not set, using SQLite fallback"
fi

# 预创建必要目录
mkdir -p /app/data /app/logs /app/uploads /app/temp

echo "[render-start] Starting application on port ${PORT:-8005}..."
exec python run.py
