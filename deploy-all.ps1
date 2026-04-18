# Agent Learning Platform 全栈一键部署脚本
# 作者: 小老虎 🐯
# 功能: 自动部署前后端服务到本地或远程服务器

param(
    [string]$Target = "local",  # local, docker, server
    [string]$ServerIP = "",
    [string]$ServerUser = "root",
    [string]$ServerKey = "",
    [switch]$SkipTests = $false,
    [switch]$Force = $false
)

Write-Host "🐯 Agent Learning Platform 全栈部署脚本" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# 颜色定义
$ErrorColor = "Red"
$SuccessColor = "Green"
$WarningColor = "Yellow"
$InfoColor = "Cyan"

# 检查必要工具
function Check-Tools {
    Write-Host "🔍 检查必要工具..." -ForegroundColor $InfoColor
    
    $tools = @("git", "node", "npm", "python", "pip", "docker", "docker-compose")
    $missing = @()
    
    foreach ($tool in $tools) {
        try {
            $null = Get-Command $tool -ErrorAction Stop
            Write-Host "   ✅ $tool" -ForegroundColor $SuccessColor
        } catch {
            Write-Host "   ❌ $tool 未安装" -ForegroundColor $ErrorColor
            $missing += $tool
        }
    }
    
    if ($missing.Count -gt 0) {
        Write-Host "❌ 缺少必要工具，请先安装: $($missing -join ', ')" -ForegroundColor $ErrorColor
        exit 1
    }
    
    Write-Host "✅ 所有必要工具已安装" -ForegroundColor $SuccessColor
}

# 构建前端
function Build-Frontend {
    Write-Host "🔄 构建前端..." -ForegroundColor $InfoColor
    
    Set-Location "frontend"
    
    # 清理旧构建
    if (Test-Path "dist") {
        Remove-Item -Recurse -Force "dist"
    }
    
    # 安装依赖
    Write-Host "   📦 安装依赖..." -ForegroundColor $InfoColor
    npm ci --no-audit --no-fund
    
    # 构建
    Write-Host "   🔨 构建项目..." -ForegroundColor $InfoColor
    $env:NODE_ENV = "production"
    npm run build
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 前端构建失败" -ForegroundColor $ErrorColor
        exit 1
    }
    
    Write-Host "✅ 前端构建完成" -ForegroundColor $SuccessColor
    Set-Location ".."
}

# 构建后端
function Build-Backend {
    Write-Host "🔄 构建后端..." -ForegroundColor $InfoColor
    
    Set-Location "backend"
    
    # 创建虚拟环境
    if (-not (Test-Path "venv")) {
        Write-Host "   🐍 创建Python虚拟环境..." -ForegroundColor $InfoColor
        python -m venv venv
    }
    
    # 激活虚拟环境
    Write-Host "   📦 安装依赖..." -ForegroundColor $InfoColor
    & "venv\Scripts\activate"
    pip install -r requirements.txt
    
    # 运行测试（可选）
    if (-not $SkipTests) {
        Write-Host "   🧪 运行测试..." -ForegroundColor $InfoColor
        python -m pytest tests/ -v
    }
    
    Write-Host "✅ 后端构建完成" -ForegroundColor $SuccessColor
    Set-Location ".."
}

# Docker部署
function Deploy-Docker {
    Write-Host "🐳 使用Docker部署..." -ForegroundColor $InfoColor
    
    # 构建前端镜像
    Write-Host "   🔨 构建前端Docker镜像..." -ForegroundColor $InfoColor
    Set-Location "frontend"
    docker build -t agent-platform-frontend:latest .
    Set-Location ".."
    
    # 构建后端镜像
    Write-Host "   🔨 构建后端Docker镜像..." -ForegroundColor $InfoColor
    Set-Location "backend"
    docker build -t agent-platform-backend:latest .
    Set-Location ".."
    
    # 创建docker-compose文件
    Write-Host "   📄 创建docker-compose.yml..." -ForegroundColor $InfoColor
    $composeContent = @"
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    container_name: agent-platform-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./frontend/nginx.conf:/etc/nginx/nginx.conf
      - ./frontend/dist:/usr/share/nginx/html
    depends_on:
      - backend
    networks:
      - agent-network
    restart: unless-stopped

  backend:
    image: agent-platform-backend:latest
    container_name: agent-platform-backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/agent_platform
      - REDIS_URL=redis://redis:6379/0
      - DEBUG=False
      - ENVIRONMENT=production
    volumes:
      - ./backend/logs:/app/logs
      - ./backend/uploads:/app/uploads
    depends_on:
      - db
      - redis
    networks:
      - agent-network
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: agent-platform-db
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=agent_platform
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - agent-network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: agent-platform-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - agent-network
    restart: unless-stopped

networks:
  agent-network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
"@
    
    $composeContent | Out-File -FilePath "docker-compose.yml" -Encoding UTF8
    
    # 启动服务
    Write-Host "   🚀 启动Docker服务..." -ForegroundColor $InfoColor
    docker-compose down
    docker-compose up -d
    
    # 检查服务状态
    Write-Host "   🔍 检查服务状态..." -ForegroundColor $InfoColor
    Start-Sleep -Seconds 10
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost/health" -TimeoutSec 5
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ 部署成功！" -ForegroundColor $SuccessColor
            Write-Host "🌐 前端访问: http://localhost" -ForegroundColor $SuccessColor
            Write-Host "🔧 后端API: http://localhost:8000" -ForegroundColor $SuccessColor
            Write-Host "📊 数据库: localhost:5432" -ForegroundColor $SuccessColor
            Write-Host "🔴 Redis: localhost:6379" -ForegroundColor $SuccessColor
        }
    } catch {
        Write-Host "⚠️  服务启动中，请稍后访问..." -ForegroundColor $WarningColor
        Write-Host "📋 查看日志: docker-compose logs" -ForegroundColor $InfoColor
    }
}

# 本地部署
function Deploy-Local {
    Write-Host "💻 本地部署..." -ForegroundColor $InfoColor
    
    # 启动后端
    Write-Host "   🚀 启动后端服务..." -ForegroundColor $InfoColor
    Start-Process -FilePath "python" -ArgumentList "backend/start_simple.py" -WindowStyle Hidden
    
    # 启动前端开发服务器
    Write-Host "   🚀 启动前端开发服务器..." -ForegroundColor $InfoColor
    Start-Process -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory "frontend" -WindowStyle Hidden
    
    Write-Host "✅ 本地服务已启动" -ForegroundColor $SuccessColor
    Write-Host "🌐 前端: http://localhost:5173" -ForegroundColor $SuccessColor
    Write-Host "🔧 后端: http://localhost:8000" -ForegroundColor $SuccessColor
    Write-Host "📋 停止服务: Ctrl+C" -ForegroundColor $InfoColor
}

# 远程服务器部署
function Deploy-Remote {
    param(
        [string]$ServerIP,
        [string]$ServerUser,
        [string]$ServerKey
    )
    
    if ([string]::IsNullOrEmpty($ServerIP)) {
        Write-Host "❌ 请指定服务器IP地址" -ForegroundColor $ErrorColor
        exit 1
    }
    
    Write-Host "🌐 部署到远程服务器: $ServerIP" -ForegroundColor $InfoColor
    
    # 创建部署包
    Write-Host "   📦 创建部署包..." -ForegroundColor $InfoColor
    $deployDir = "deploy-package-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    New-Item -ItemType Directory -Path $deployDir -Force
    
    # 复制文件
    Copy-Item -Path "frontend/dist" -Destination "$deployDir/frontend-dist" -Recurse
    Copy-Item -Path "backend" -Destination "$deployDir/backend" -Recurse -Exclude "venv", "__pycache__", "*.pyc"
    Copy-Item -Path "docker-compose.yml" -Destination "$deployDir/"
    Copy-Item -Path "frontend/nginx.conf" -Destination "$deployDir/"
    
    # 创建部署脚本
    $deployScript = @"
#!/bin/bash
set -e

echo "🚀 开始部署 Agent Learning Platform..."

# 检查Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装"
    exit 1
fi

# 停止旧服务
echo "🔄 停止旧服务..."
docker-compose down || true

# 启动新服务
echo "🚀 启动服务..."
docker-compose up -d

# 等待启动
echo "⏳ 等待服务启动..."
sleep 15

# 检查状态
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ 部署成功！"
    echo "🌐 访问地址: http://$ServerIP"
else
    echo "❌ 部署失败"
    docker-compose logs
    exit 1
fi
"@
    
    $deployScript | Out-File -FilePath "$deployDir/deploy.sh" -Encoding UTF8
    
    # 压缩部署包
    Compress-Archive -Path "$deployDir/*" -DestinationPath "deploy-package.zip" -Force
    
    Write-Host "✅ 部署包已创建: deploy-package.zip" -ForegroundColor $SuccessColor
    Write-Host "📋 手动部署步骤:" -ForegroundColor $InfoColor
    Write-Host "   1. 上传 deploy-package.zip 到服务器" -ForegroundColor $InfoColor
    Write-Host "   2. 解压: unzip deploy-package.zip" -ForegroundColor $InfoColor
    Write-Host "   3. 运行: chmod +x deploy.sh && ./deploy.sh" -ForegroundColor $InfoColor
}

# 主流程
try {
    # 检查工具
    Check-Tools
    
    # 构建
    Build-Frontend
    Build-Backend
    
    # 根据目标部署
    switch ($Target) {
        "local" {
            Deploy-Local
        }
        "docker" {
            Deploy-Docker
        }
        "server" {
            Deploy-Remote -ServerIP $ServerIP -ServerUser $ServerUser -ServerKey $ServerKey
        }
        default {
            Write-Host "❌ 未知部署目标: $Target" -ForegroundColor $ErrorColor
            Write-Host "可用目标: local, docker, server" -ForegroundColor $InfoColor
            exit 1
        }
    }
    
    Write-Host "🎉 部署完成！" -ForegroundColor Cyan
} catch {
    Write-Host "❌ 部署失败: $_" -ForegroundColor $ErrorColor
    exit 1
}