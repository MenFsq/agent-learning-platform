#!/bin/bash

# Agent Learning Platform 后端开发启动脚本

set -e

echo "🚀 启动 Agent Learning Platform 后端开发环境..."

# 检查Python版本
echo "📦 检查Python版本..."
python --version

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "🔧 创建虚拟环境..."
    python -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  警告: .env 文件不存在"
    echo "📝 从 .env.example 创建 .env 文件..."
    cp .env.example .env
    echo "✅ 请编辑 .env 文件并设置正确的配置值"
fi

# 启动开发服务器
echo "🚀 启动开发服务器..."
echo "📊 API文档: http://localhost:8000/docs"
echo "📊 ReDoc文档: http://localhost:8000/redoc"
echo "🏥 健康检查: http://localhost:8000/health"

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000