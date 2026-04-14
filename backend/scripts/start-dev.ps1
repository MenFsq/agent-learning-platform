# Agent Learning Platform 后端开发启动脚本 (Windows)

Write-Host "🚀 启动 Agent Learning Platform 后端开发环境..." -ForegroundColor Green

# 检查Python版本
Write-Host "📦 检查Python版本..." -ForegroundColor Cyan
python --version

# 检查虚拟环境
if (!(Test-Path "venv")) {
    Write-Host "🔧 创建虚拟环境..." -ForegroundColor Yellow
    python -m venv venv
}

# 激活虚拟环境
Write-Host "🔧 激活虚拟环境..." -ForegroundColor Cyan
.\venv\Scripts\Activate.ps1

# 安装依赖
Write-Host "📦 安装依赖..." -ForegroundColor Cyan
pip install --upgrade pip
pip install -r requirements.txt -r requirements-dev.txt

# 检查环境变量文件
if (!(Test-Path ".env")) {
    Write-Host "⚠️  警告: .env 文件不存在" -ForegroundColor Yellow
    Write-Host "📝 从 .env.example 创建 .env 文件..." -ForegroundColor Cyan
    Copy-Item .env.example .env
    Write-Host "✅ 请编辑 .env 文件并设置正确的配置值" -ForegroundColor Green
}

# 启动开发服务器
Write-Host "🚀 启动开发服务器..." -ForegroundColor Green
Write-Host "📊 API文档: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "📊 ReDoc文档: http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host "🏥 健康检查: http://localhost:8000/health" -ForegroundColor Cyan

uvicorn src.main:app --reload --host 0.0.0.0 --port 8000