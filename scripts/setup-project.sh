#!/bin/bash

# Agent Learning Platform - 项目设置脚本
# 作者: 小老虎 🐯
# 日期: 2026-04-13

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# 日志函数
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

log_step() {
    echo -e "${MAGENTA}📋 $1${NC}"
}

# 显示横幅
show_banner() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                                                              ║"
    echo "║                Agent Learning Platform                        ║"
    echo "║                项目设置脚本 v1.0.0                           ║"
    echo "║                                                              ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
}

# 检查命令是否存在
check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "命令 '$1' 未找到，请先安装"
        return 1
    fi
    return 0
}

# 检查系统环境
check_environment() {
    log_step "检查系统环境..."
    
    # 检查操作系统
    OS=$(uname -s)
    log "操作系统: $OS"
    
    # 检查Python
    if check_command python3; then
        python_version=$(python3 --version | cut -d' ' -f2)
        log "Python 版本: $python_version"
        
        # 检查Python版本是否满足要求
        if [[ $(echo "$python_version 3.9" | tr " " "\n" | sort -V | head -n1) != "3.9" ]]; then
            log_warning "Python 版本低于 3.9，建议升级"
        fi
    fi
    
    # 检查Node.js
    if check_command node; then
        node_version=$(node --version | cut -d'v' -f2)
        log "Node.js 版本: $node_version"
        
        if [[ $(echo "$node_version 16.0.0" | tr " " "\n" | sort -V | head -n1) != "16.0.0" ]]; then
            log_warning "Node.js 版本低于 16.0.0，建议升级"
        fi
    fi
    
    # 检查npm
    if check_command npm; then
        npm_version=$(npm --version)
        log "npm 版本: $npm_version"
    fi
    
    # 检查Docker
    if check_command docker; then
        docker_version=$(docker --version | cut -d' ' -f3 | tr -d ',')
        log "Docker 版本: $docker_version"
    else
        log_warning "Docker 未安装，容器化功能将不可用"
    fi
    
    # 检查Docker Compose
    if check_command docker-compose; then
        docker_compose_version=$(docker-compose --version | cut -d' ' -f3 | tr -d ',')
        log "Docker Compose 版本: $docker_compose_version"
    fi
    
    # 检查Git
    if check_command git; then
        git_version=$(git --version | cut -d' ' -f3)
        log "Git 版本: $git_version"
    fi
    
    log_success "环境检查完成"
}

# 创建项目目录结构
create_project_structure() {
    log_step "创建项目目录结构..."
    
    # 定义目录结构
    directories=(
        # 核心模块
        "modules/project-dashboard/src/components"
        "modules/project-dashboard/src/composables"
        "modules/project-dashboard/src/types"
        "modules/project-dashboard/src/utils"
        "modules/project-dashboard/tests/unit"
        "modules/project-dashboard/tests/e2e"
        
        "modules/learning-guide/tutorials/langchain-basics"
        "modules/learning-guide/tutorials/openclaw-skills"
        "modules/learning-guide/tutorials/vue-typescript"
        "modules/learning-guide/tutorials/enterprise-integration"
        "modules/learning-guide/exercises"
        "modules/learning-guide/assessments"
        
        "modules/code-examples/langchain"
        "modules/code-examples/openclaw"
        "modules/code-examples/vue"
        "modules/code-examples/integration"
        
        "modules/community-integration/botlearn-api"
        "modules/community-integration/content-publishing"
        "modules/community-integration/qa-system"
        "modules/community-integration/contributor-management"
        
        "modules/deployment-tools/docker"
        "modules/deployment-tools/kubernetes"
        "modules/deployment-tools/monitoring"
        "modules/deployment-tools/ci-cd"
        
        # 前端界面
        "web-ui/dashboard/assets/css"
        "web-ui/dashboard/assets/js"
        "web-ui/dashboard/assets/images"
        "web-ui/dashboard/components"
        
        "web-ui/learning-path"
        "web-ui/community-feed"
        "web-ui/admin-panel"
        
        # 后端服务
        "backend/api-server/src/routes/projects"
        "backend/api-server/src/routes/tasks"
        "backend/api-server/src/routes/users"
        "backend/api-server/src/routes/community"
        "backend/api-server/src/controllers"
        "backend/api-server/src/services"
        "backend/api-server/src/models"
        "backend/api-server/src/middleware"
        "backend/api-server/src/utils"
        "backend/api-server/tests"
        
        "backend/agent-core/langchain-integration"
        "backend/agent-core/openclaw-sdk"
        "backend/agent-core/knowledge-base"
        "backend/agent-core/skill-manager"
        
        "backend/data-pipeline/document-processor"
        "backend/data-pipeline/vector-database"
        "backend/data-pipeline/cache-manager"
        "backend/data-pipeline/batch-processor"
        
        # 文档
        "docs/tutorials"
        "docs/api-reference/rest-api"
        "docs/api-reference/graphql-api"
        "docs/api-reference/websocket-api"
        "docs/best-practices"
        "docs/contribution-guide"
        
        # 部署配置
        "deployment/docker"
        "deployment/kubernetes/manifests"
        "deployment/kubernetes/helm-chart"
        "deployment/kubernetes/terraform"
        "deployment/ci-cd/github-actions"
        "deployment/ci-cd/gitlab-ci"
        "deployment/ci-cd/jenkins"
        
        # 测试
        "tests/unit/frontend"
        "tests/unit/backend"
        "tests/unit/shared"
        "tests/integration/api"
        "tests/integration/database"
        "tests/integration/external-services"
        "tests/e2e/cypress"
        "tests/e2e/playwright"
        "tests/e2e/selenium"
        "tests/performance/load-testing"
        "tests/performance/stress-testing"
        "tests/performance/benchmark"
        
        # 脚本
        "scripts/setup"
        "scripts/build"
        "scripts/deploy"
        "scripts/monitoring"
        "scripts/maintenance"
        
        # 配置
        "config/development"
        "config/staging"
        "config/production"
        "config/local"
        
        # 数据
        "data/databases"
        "data/vector-stores"
        "data/cache"
        "data/backups"
        
        # 日志
        "logs/application"
        "logs/access"
        "logs/error"
        "logs/audit"
        
        # GitHub配置
        ".github/workflows"
        ".github/ISSUE_TEMPLATE"
        ".github/PULL_REQUEST_TEMPLATE"
    )
    
    # 创建目录
    for dir in "${directories[@]}"; do
        mkdir -p "$dir"
        log "创建目录: $dir"
    done
    
    # 创建必要的空文件
    touch_files=(
        # 模块初始化文件
        "modules/project-dashboard/README.md"
        "modules/project-dashboard/src/components/.gitkeep"
        "modules/project-dashboard/src/composables/.gitkeep"
        "modules/project-dashboard/src/types/.gitkeep"
        "modules/project-dashboard/src/utils/.gitkeep"
        
        # 前端文件
        "web-ui/dashboard/README.md"
        
        # 后端文件
        "backend/api-server/README.md"
        "backend/agent-core/README.md"
        "backend/data-pipeline/README.md"
        
        # 文档文件
        "docs/README.md"
        
        # 配置文件
        "config/development/.env.example"
        "config/staging/.env.example"
        "config/production/.env.example"
        "config/local/.env.example"
        
        # 数据目录占位文件
        "data/.gitkeep"
        "logs/.gitkeep"
    )
    
    for file in "${touch_files[@]}"; do
        touch "$file"
        log "创建文件: $file"
    done
    
    log_success "项目目录结构创建完成"
}

# 创建配置文件
create_config_files() {
    log_step "创建配置文件..."
    
    # 创建主配置文件
    cat > config/default.yaml << 'EOF'
# Agent Learning Platform - 默认配置

# 应用配置
app:
  name: "Agent Learning Platform"
  version: "1.0.0"
  environment: "development"
  debug: true
  port: 3000

# 数据库配置
database:
  postgres:
    host: "localhost"
    port: 5432
    database: "agent_learning"
    username: "postgres"
    password: "postgres"
    pool_size: 20
  
  redis:
    host: "localhost"
    port: 6379
    database: 0
  
  chroma:
    host: "localhost"
    port: 8000
    collection: "documents"

# API配置
api:
  base_url: "http://localhost:3000/api"
  version: "v1"
  rate_limit:
    enabled: true
    requests_per_minute: 60
  cors:
    origins:
      - "http://localhost:8080"
      - "http://localhost:3000"

# 认证配置
auth:
  jwt_secret: "your-jwt-secret-key-change-in-production"
  token_expiry: "7d"
  refresh_token_expiry: "30d"

# 外部服务配置
services:
  openai:
    api_key: "${OPENAI_API_KEY}"
    base_url: "https://api.openai.com/v1"
  
  botlearn:
    api_key: "${BOTLEARN_API_KEY}"
    base_url: "https://www.botlearn.ai/api"
  
  openclaw:
    api_key: "${OPENCLAW_API_KEY}"
    base_url: "http://localhost:8080"

# 日志配置
logging:
  level: "INFO"
  format: "json"
  output:
    console: true
    file: true
    file_path: "./logs/application.log"
  rotation:
    max_size: "100MB"
    max_files: 10

# 监控配置
monitoring:
  enabled: true
  prometheus:
    port: 9090
  grafana:
    port: 3000
  health_check:
    enabled: true
    endpoint: "/health"
    interval: "30s"

# 邮件配置
email:
  enabled: false
  smtp:
    host: "smtp.gmail.com"
    port: 587
    username: "${EMAIL_USERNAME}"
    password: "${EMAIL_PASSWORD}"
  from: "noreply@agent-learning.dev"
EOF
    
    log_success "配置文件创建完成"
}

# 创建环境变量文件
create_env_files() {
    log_step "创建环境变量文件..."
    
    # 创建.env.example文件
    cat > .env.example << 'EOF'
# Agent Learning Platform - 环境变量示例

# 应用配置
APP_NAME="Agent Learning Platform"
APP_ENV="development"
APP_DEBUG="true"
APP_PORT="3000"
APP_URL="http://localhost:3000"

# 数据库配置
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"
POSTGRES_DB="agent_learning"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="postgres"

REDIS_HOST="localhost"
REDIS_PORT="6379"
REDIS_PASSWORD=""

# 外部API密钥
OPENAI_API_KEY="your_openai_api_key_here"
BOTLEARN_API_KEY="your_botlearn_api_key_here"
OPENCLAW_API_KEY="your_openclaw_api_key_here"

# 认证配置
JWT_SECRET="your-jwt-secret-key-change-in-production"
JWT_EXPIRY="7d"
REFRESH_TOKEN_EXPIRY="30d"

# 邮件配置 (可选)
EMAIL_HOST="smtp.gmail.com"
EMAIL_PORT="587"
EMAIL_USERNAME="your_email@gmail.com"
EMAIL_PASSWORD="your_email_password"

# 监控配置
PROMETHEUS_PORT="9090"
GRAFANA_PORT="3000"

# 功能开关
FEATURE_AI_ASSISTANT="true"
FEATURE_COMMUNITY_INTEGRATION="true"
FEATURE_REAL_TIME_COLLABORATION="true"
FEATURE_ADVANCED_ANALYTICS="true"
EOF
    
    # 复制为开发环境配置
    cp .env.example .env.development
    
    log_success "环境变量文件创建完成"
    log_warning "请编辑 .env.development 文件，配置你的API密钥"
}

# 创建Docker配置
create_docker_config() {
    log_step "创建Docker配置..."
    
    # 创建Dockerfile
    cat > Dockerfile << 'EOF'
# Agent Learning Platform - Docker镜像
# 多阶段构建

# 第一阶段: 构建前端
FROM node:18-alpine AS frontend-builder

WORKDIR /app

# 复制前端代码
COPY web-ui/dashboard/package*.json ./
RUN npm ci --only=production

COPY web-ui/dashboard/ .
RUN npm run build

# 第二阶段: 构建后端
FROM python:3.9-slim AS backend-builder

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制后端代码
COPY backend/api-server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/api-server/ .

# 第三阶段: 运行环境
FROM python:3.9-slim

WORKDIR /app

# 安装运行时依赖
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 创建非root用户
RUN useradd -m -u 1000 agent && chown -R agent:agent /app
USER agent

# 从构建阶段复制文件
COPY --from=frontend-builder /app/dist ./web-ui/dist
COPY --from=backend-builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=backend-builder /app .

# 复制配置文件
COPY config/default.yaml ./config/
COPY .env.production ./.env

# 暴露端口
EXPOSE 3000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:3000/health || exit 1

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
EOF
    
    # 创建docker-compose.yml
    cat > docker-compose.yml << 'EOF'
# Agent Learning Platform - Docker Compose配置
version: '3.8'

services:
  # 数据库服务
  postgres:
    image: postgres:15-alpine
    container_name: agent-learning-postgres
    environment:
      POSTGRES_DB: agent_learning
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Redis缓存服务
  redis:
    image: redis:7-alpine
    container_name: agent-learning-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Chroma向量数据库
  chroma:
    image: chromadb/chroma:latest
    container_name: agent-learning-chroma
    ports:
      - "8000:8000"
    environment:
      IS_PERSISTENT: "TRUE"
      PERSIST_DIRECTORY: "/chroma/chroma"
    volumes:
      - chroma-data:/chroma
    restart: unless-stopped

  # 主应用服务
  app:
    build: .
    container_name: agent-learning-app
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/agent_learning
      - REDIS_URL=redis://redis:6379
      - CHROMA_URL=http://chroma:8000
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
      - ./config:/app/config
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      chroma:
        condition: service_started
    env_file:
      - .env.development
    restart: unless-stopped

  # Nginx反向代理
  nginx:
    image: nginx:alpine
    container_name: agent-learning-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./deployment/nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./deployment/nginx/ssl:/etc/nginx/ssl
      - ./web-ui/dashboard/dist:/usr/share/nginx/html
    depends_on:
      - app
    restart: unless-stopped

  # 监控服务 - Prometheus
  prometheus:
    image: prom/prometheus:latest
    container_name: agent-learning-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./deployment/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped

  # 监控服务 - Grafana
  grafana:
    image: grafana/grafana:latest
    container_name: agent-learning-grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana-data:/var/lib/grafana
      - ./deployment/monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./deployment/monitoring/grafana/datasources:/etc/grafana/provisioning/datasources
    depends_on:
      - prometheus
    restart: unless-stopped

volumes:
  postgres-data:
  redis-data:
  chroma-data:
  prometheus-data:
  grafana-data:
EOF
    
    log_success "Docker配置创建完成"
}

# 创建GitHub Actions工作流
create_github_workflows() {
    log_step "创建GitHub Actions工作流..."
    
    # 创建CI工作流
    mkdir -p .github/workflows
    
    cat > .github/workflows/ci.yml << 'EOF'
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
        cache: 'npm'
        cache-dependency-path: web-ui/dashboard/package-lock.json
    
    - name: Install frontend dependencies
      run: |
        cd web-ui/dashboard
        npm ci
    
    - name: Lint frontend code
      run: |
        cd web-ui/dashboard
        npm run lint
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        cache: 'pip'
    
    - name: Install backend dependencies
      run: |
        cd backend/api-server
        pip install -r requirements.txt
        pip install black flake8 mypy
    
    - name: Lint backend code
      run: |
        cd backend/api-server
        black --check .
        flake8 .
        mypy .

  test:
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:15-alpine
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      
      redis:
        image: redis:7-alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install backend dependencies
      run: |
        cd backend/api-server
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run backend tests
      env:
        DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
        REDIS_URL: redis://localhost:6379
      run: |
        cd backend/api-server
        pytest tests/ --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./backend/api-server/coverage.xml
        fail_ci_if_error: true

  build-docker:
    runs-on: ubuntu-latest
    needs: test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to DockerHub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          ${{ secrets.DOCKER_USERNAME }}/agent-learning-platform:latest
          ${{ secrets.DOCKER_USERNAME }}/agent-learning-platform:${{ github.sha }}
        cache-from: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/agent-learning-platform:buildcache
        cache-to: type=registry,ref=${{ secrets.DOCKER_USERNAME }}/agent-learning-platform:buildcache,mode=max

  deploy:
    runs-on: ubuntu-latest
    needs: build-docker
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # 这里添加实际的部署命令
        # 例如: kubectl apply -f deployment/kubernetes/
      env:
        KUBECONFIG: ${{ secrets.KUBECONFIG }}
EOF
    
    # 创建Issue模板
    mkdir -p .github/ISSUE_TEMPLATE
    
    cat > .github/ISSUE_TEMPLATE/bug_report.md << 'EOF'
---
name: Bug报告
about: 报告一个bug
title: '[BUG] '
labels: bug
assignees: ''

---

**描述bug**
清晰简洁地描述bug是什么。

**重现步骤**
重现行为的步骤：
1. 进入 '...'
2. 点击 '....'
3. 滚动到 '....'
4. 看到错误

**预期行为**
清晰简洁地描述你期望发生的事情。

**截图**
如果适用，添加截图以帮助解释你的问题。

**环境信息：**
 - 操作系统: [例如: Windows 10]
 - 浏览器: [例如: Chrome 90]
 - 版本: [例如: v1.0.0]

**附加信息**
在此处添加有关问题的任何其他信息。
EOF
    
    cat > .github/ISSUE_TEMPLATE/feature_request.md << 'EOF'
---
name: 功能请求
about: 为这个项目提出一个想法
title: '[FEATURE] '
labels: enhancement
assignees: ''

---

**你的功能请求是否与问题相关？请描述。**
清晰简洁地描述问题是什么。例如：当我[...]时，我总是感到沮丧

**描述你想要的解决方案**
清晰简洁地描述你希望发生什么。

**描述你考虑过的替代方案**
清晰简洁地描述你考虑过的任何替代解决方案或功能。

**附加信息**
在此处添加有关功能请求的任何其他信息或截图。
EOF
    
    log_success "GitHub Actions工作流创建完成"
}

# 创建Makefile
create_makefile() {
    log_step "创建Makefile..."
    
    cat > Makefile << 'EOF'
# Agent Learning Platform - Makefile

.PHONY: help install dev build test lint clean deploy

# 默认目标
help:
	@echo "Agent Learning Platform - 开发命令"
	@echo ""
	@echo "可用命令:"
	@echo "  make install     安装所有依赖"
	@echo "  make dev         启动开发环境"
	@echo "  make build       构建生产版本"
	@echo "  make test        运行测试"
	@echo "  make lint        代码检查"
	@echo "  make clean       清理构建文件"
	@echo "  make deploy      部署到生产环境"
	@echo "  make docker-up   启动Docker服务"
	@echo "  make docker-down 停止Docker服务"

# 安装依赖
install:
	@echo "安装前端依赖..."
	cd web-ui/dashboard && npm install
	@echo "安装后端依赖..."
	cd backend/api-server && pip install -r requirements.txt
	@echo "安装开发工具..."
	pip install black flake8 mypy pytest

# 启动开发环境
dev:
	@echo "启动开发环境..."
	@echo "前端: http://localhost:8080"
	@echo "后端API: http://localhost:3000"
	@echo "监控: http://localhost:3001"
	@echo ""
	@echo "使用 Ctrl+C 停止所有服务"
	
	# 启动所有服务
	docker-compose up

# 构建生产版本
build:
	@echo "构建前端..."
	cd web-ui/dashboard && npm run build
	@echo "构建Docker镜像..."
	docker-compose build

# 运行测试
test:
	@echo "运行前端测试..."
	cd web-ui/dashboard && npm test
	@echo "运行后端测试..."
	cd backend/api-server && pytest

# 代码检查
lint:
	@echo "检查前端代码..."
	cd web-ui/dashboard && npm run lint
	@echo "检查后端代码..."
	cd backend/api-server && black --check . && flake8 . && mypy .

# 清理构建文件
clean:
	@echo "清理构建文件..."
	rm -rf web-ui/dashboard/dist
	rm -rf web-ui/dashboard/node_modules
	rm -rf backend/api-server/__pycache__
	rm -rf backend/api-server/.pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	docker-compose down -v

# 部署到生产环境
deploy:
	@echo "部署到生产环境..."
	# 这里添加实际的部署命令
	# kubectl apply -f deployment/kubernetes/

# Docker命令
docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-restart:
	docker-compose restart

# 数据库命令
db-migrate:
	cd backend/api-server && alembic upgrade head

db-rollback:
	cd backend/api-server && alembic downgrade -1

db-reset:
	docker-compose down -v
	docker-compose up -d postgres redis chroma
	sleep 10
	make db-migrate

# 监控命令
monitor:
	@echo "打开监控面板..."
	open http://localhost:3001 || xdg-open http://localhost:3001 || echo "请手动访问: http://localhost:3001"

# 开发工具
format:
	cd backend/api-server && black .
	cd web-ui/dashboard && npm run format

check-security:
	@echo "安全检查..."
	# 这里添加安全检查命令
	# npm audit
	# pip-audit
EOF
    
    log_success "Makefile创建完成"
}

# 创建项目文档
create_project_docs() {
    log_step "创建项目文档..."
    
    # 创建主README
    cat > README.md << 'EOF'
# Agent Learning Platform 🚀

**学习搭建AI Agent的完整实践平台** - 基于LangChain + OpenClaw + Vue 3的技术栈

## 🎯 快速开始

### 环境要求
- Node.js 16+
- Python 3.9+
- Docker 20+
- Git

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/your-username/agent-learning-platform.git
cd agent-learning-platform

# 2. 运行设置脚本
chmod +x scripts/setup-project.sh
./scripts/setup-project.sh

# 3. 配置环境变量
cp .env.example .env.development
# 编辑 .env.development 文件，配置API密钥

# 4. 启动开发环境
make dev
```

### 访问地址
- 前端界面: http://localhost:8080
- 后端API: http://localhost:3000
- API文档: http://localhost:3000/docs
- 监控面板: http://localhost:3001

## 📚 文档

详细文档请查看 [docs/](docs/) 目录：

- [快速开始指南](docs/tutorials/01-getting-started.md)
- [架构设计](docs/architecture.md)
- [API参考](docs/api-reference/)
- [贡献指南](docs/contribution-guide/)
- [部署指南](docs/deployment-guide/)

## 🤝 贡献

我们欢迎所有形式的贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何开始。

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系我们

- GitHub Issues: [问题报告](https://github.com/your-username/agent-learning-platform/issues)
- 邮箱: contact@agent-learning.dev
- 社区: [Discord服务器](https://discord.gg/agent-learning)

---

**让我们一起构建未来AI Agent开发的学习生态系统！** 🚀
EOF
    
    # 创建贡献指南
    cat > CONTRIBUTING.md << 'EOF'
# 贡献指南

感谢你考虑为 Agent Learning Platform 做出贡献！

## 🎯 如何贡献

### 1. 报告Bug
- 使用 [GitHub Issues](https://github.com/your-username/agent-learning-platform/issues) 报告bug
- 确保bug尚未被报告
- 提供详细的bug描述和重现步骤

### 2. 请求新功能
- 使用 [GitHub Issues](https://github.com/your-username/agent-learning-platform/issues) 请求新功能
- 描述功能的使用场景和预期行为
- 如果可能，提供设计思路或原型

### 3. 提交代码
1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📝 开发规范

### 代码风格
- 前端: 遵循 ESLint 和 Prettier 配置
- 后端: 使用 Black 进行代码格式化
- 提交信息: 使用 Conventional Commits 规范

### 测试要求
- 新功能必须包含单元测试
- Bug修复必须包含回归测试
- 确保所有测试通过后再提交PR

### 文档要求
- 新功能必须更新相关文档
- API变更必须更新API文档
- 复杂功能需要添加使用示例

## 🚀 开发流程

### 1. 设置开发环境
```bash
# 克隆项目
git clone https://github.com/your-username/agent-learning-platform.git
cd agent-learning-platform

# 安装依赖
make install

# 启动开发环境
make dev
```

### 2. 创建功能分支
```bash
git checkout -b feature/your-feature-name
```

### 3. 开发功能
- 编写代码
- 添加测试
- 更新文档

### 4. 提交更改
```bash
git add .
git commit -m "feat(scope): description of changes"
```

### 5. 创建Pull Request
- 确保代码通过所有检查
- 添加详细的PR描述
- 等待代码审查

## 📊 项目结构

详细的项目结构请查看 [PROJECT-STRUCTURE.md](PROJECT-STRUCTURE.md)。

## ❓ 常见问题

### Q: 如何运行测试？
A: 使用 `make test` 命令运行所有测试。

### Q: 如何格式化代码？
A: 使用 `make format` 命令格式化代码。

### Q: 如何部署到生产环境？
A: 查看 [部署指南](docs/deployment-guide.md)。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---
*最后更新: 2026-04-13*
EOF
    
    log_success "项目文档创建完成"
}

# 显示完成信息
show_completion() {
    echo ""
    echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}                   项目设置完成！                            ${NC}"
    echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    echo -e "${CYAN}🎉 恭喜！Agent Learning Platform 项目已成功设置。${NC}"
    echo ""
    
    echo -e "${BLUE}📁 项目结构已创建:${NC}"
    echo "  • 核心模块: modules/"
    echo "  • 前端界面: web-ui/"
    echo "  • 后端服务: backend/"
    echo "  • 项目文档: docs/"
    echo "  • 部署配置: deployment/"
    echo ""
    
    echo -e "${BLUE}🚀 下一步操作:${NC}"
    echo "  1. ${YELLOW}配置环境变量${NC}"
    echo "     cp .env.example .env.development"
    echo "     # 编辑 .env.development 文件，配置API密钥"
    echo ""
    echo "  2. ${YELLOW}启动开发环境${NC}"
    echo "     make dev"
    echo ""
    echo "  3. ${YELLOW}访问应用${NC}"
    echo "     • 前端界面: http://localhost:8080"
    echo "     • 后端API: http://localhost:3000"
    echo "     • API文档: http://localhost:3000/docs"
    echo "     • 监控面板: http://localhost:3001"
    echo ""
    
    echo -e "${BLUE}🔧 常用命令:${NC}"
    echo "  make install      # 安装依赖"
    echo "  make dev          # 启动开发环境"
    echo "  make build        # 构建生产版本"
    echo "  make test         # 运行测试"
    echo "  make lint         # 代码检查"
    echo "  make clean        # 清理构建文件"
    echo "  make docker-up    # 启动Docker服务"
    echo "  make docker-down  # 停止Docker服务"
    echo ""
    
    echo -e "${BLUE}📚 重要文件:${NC}"
    echo "  • README.md              # 项目说明"
    echo "  • CONTRIBUTING.md        # 贡献指南"
    echo "  • PROJECT-STRUCTURE.md   # 项目结构"
    echo "  • Makefile               # 开发命令"
    echo "  • docker-compose.yml     # Docker配置"
    echo ""
    
    echo -e "${YELLOW}⚠️  重要提示:${NC}"
    echo "  • 确保已安装 Docker 和 Docker Compose"
    echo "  • 配置正确的API密钥（OpenAI、BotLearn等）"
    echo "  • 首次启动可能需要几分钟下载Docker镜像"
    echo ""
    
    echo -e "${GREEN}🌟 开始你的AI Agent学习之旅吧！${NC}"
    echo ""
}

# 主函数
main() {
    show_banner
    check_environment
    create_project_structure
    create_config_files
    create_env_files
    create_docker_config
    create_github_workflows
    create_makefile
    create_project_docs
    show_completion
}

# 执行主函数
main "$@"
