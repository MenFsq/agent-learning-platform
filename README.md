# 🚀 Agent Learning Platform - 下一代AI Agent开发平台

> **企业级AI Agent开发框架 · 完整LangChain集成 · 现代化前后端架构**

![Vue 3](https://img.shields.io/badge/Frontend-Vue%203-42b883?style=for-the-badge&logo=vuedotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178c6?style=for-the-badge&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/AI-LangChain-1c3c3c?style=for-the-badge&logo=python&logoColor=white)
![OpenClaw](https://img.shields.io/badge/Platform-OpenClaw-FF6B35?style=for-the-badge&logo=github&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Container-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## 🌟 项目宣言

**Agent Learning Platform** 不仅仅是一个学习平台，它是**AI Agent开发的新范式**。我们致力于构建一个集学习、实践、部署、协作为一体的完整生态系统，让每一位开发者都能轻松构建、管理和扩展自己的智能Agent。

### 🎯 核心使命
- **降低AI Agent开发门槛**：提供完整的开发框架和最佳实践
- **加速Agent应用落地**：从原型到生产的一站式解决方案
- **构建开发者社区**：促进知识共享和技术创新
- **推动AI Agent标准化**：建立行业认可的架构规范和接口标准

### 🏆 项目特色
- ✅ **完整LangChain集成**：预置3个智能Agent，支持工具调用和对话历史
- ✅ **企业级前后端架构**：Vue 3 + TypeScript + FastAPI + PostgreSQL
- ✅ **响应式UI设计**：实时状态更新，卓越用户体验
- ✅ **容器化部署**：Docker支持，一键部署
- ✅ **完整API文档**：Swagger UI，开发者友好
- ✅ **开源协作**：MIT协议，欢迎社区贡献

GitHub 仓库：[MenFsq/agent-learning-platform](https://github.com/MenFsq/agent-learning-platform)
Demo 地址：[Agent Learning](https://menfsq.github.io/agent-learning-platform/)

---

## 🚀 快速开始

### 5分钟快速启动

```bash
# 1. 克隆项目
git clone https://github.com/MenFsq/agent-learning-platform.git
cd agent-learning-platform

# 2. 配置后端环境变量
cd backend
cp .env.example .env
# 然后在 .env 中至少填写：
# DEEPSEEK_API_KEY=your-deepseek-api-key

# 3. 启动后端服务（统一入口）
cd backend
pip install -r requirements.txt
python start_unified.py
# 服务运行在 http://localhost:8004

# 4. 启动前端服务
cd frontend
npm install
npm run dev
# 服务运行在 http://localhost:5174

# 5. 访问平台
# 打开浏览器访问 http://localhost:5174/agent
```

### DeepSeek 配置

统一后端默认兼容 DeepSeek 的 OpenAI 协议，推荐在 `backend/.env` 中配置：

```env
DEEPSEEK_API_KEY=your-deepseek-api-key
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEFAULT_CHAT_MODEL=deepseek-chat
DEFAULT_REASONER_MODEL=deepseek-reasoner
```

说明：
- `start_unified.py` 会优先使用 `DEEPSEEK_API_KEY`
- 如果未配置 DeepSeek key，后端才会回退到 `OPENAI_API_KEY`
- 不要把真实 key 提交到仓库，建议只保存在本地 `.env`

### 📊 系统状态验证

```bash
# 验证后端健康
curl http://localhost:8004/health
# 响应: {"status": "healthy", "langchain": "integrated"}

# 验证Agent列表
curl http://localhost:8004/api/v1/agents
# 响应: 3个预加载LangChain Agent
```

---

## 🏗️ 企业级架构设计

### 🎨 前端架构 - 现代化用户体验

**技术栈**: Vue 3 + TypeScript + Vite + Element Plus

#### 核心特性
- **响应式设计**: 实时状态更新，无需手动刷新
- **TypeScript安全**: 完整的类型定义，减少运行时错误
- **组件化开发**: 高度可复用的UI组件库
- **状态管理**: Pinia提供可预测的状态管理
- **路由系统**: Vue Router支持SPA无缝导航
- **开发体验**: Vite热重载，极速开发

#### 架构优势
```typescript
// 类型安全的Agent接口
type Agent = {
  id: string;           // 字符串ID，支持完整版LangChain
  name: string;
  status: 'running' | 'stopped';
  model: string;
  tools: string[];
  // ... 完整类型定义
}

// 响应式状态管理
const activeAgent = ref<Agent | null>(null)
const agents = ref<Agent[]>([])
```

### ⚙️ 后端架构 - 高性能AI服务

**技术栈**: FastAPI + LangChain + PostgreSQL + Redis

#### 核心模块
1. **Agent管理模块**
   - Agent生命周期管理（创建、启动、停止、删除）
   - 状态监控和健康检查
   - 资源使用统计

2. **LangChain集成层**
   - 预加载智能Agent（3个专业Agent）
   - 工具调用系统（Web搜索、计算器、代码执行等）
   - 对话历史管理
   - 记忆系统支持

3. **API网关层**
   - RESTful API设计
   - 身份验证和授权
   - 速率限制和请求验证
   - 完整的Swagger文档

4. **数据持久层**
   - PostgreSQL关系数据库
   - Redis缓存和会话管理
   - 异步任务队列

#### 架构优势
```python
# FastAPI + LangChain 集成示例
@app.post("/api/v1/agents/{agent_id}/interact")
async def interact_with_agent(agent_id: str, message: str):
    """与智能Agent交互"""
    agent = get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # LangChain处理
    response = await agent.chain.arun(message)
    return {"response": response}
```

## 🎯 架构设计哲学

### 1. 分离关注点原则
- **前端专注用户体验**: 响应式UI、状态管理、交互逻辑
- **后端专注业务逻辑**: AI处理、数据管理、系统集成
- **数据层专注持久化**: 数据存储、缓存优化、事务管理

### 2. 微服务就绪架构
- **独立部署**: 前后端可独立部署和扩展
- **API契约**: 严格的接口定义和版本管理
- **服务发现**: 为未来微服务拆分预留接口

### 3. 可观测性设计
- **健康检查**: 实时系统状态监控
- **日志系统**: 结构化日志记录
- **性能指标**: 关键性能指标收集
- **错误追踪**: 完整的错误堆栈和上下文

### 4. 安全第一原则
- **输入验证**: 所有API输入严格验证
- **身份认证**: JWT令牌认证系统
- **权限控制**: 细粒度的访问控制
- **数据加密**: 敏感数据加密存储

## 🔥 核心功能亮点

### 1. 🤖 智能Agent管理平台
- **Agent仪表板**: 可视化Agent状态监控
- **一键启停**: 实时控制Agent运行状态
- **资源监控**: CPU、内存、运行时间统计
- **对话历史**: 完整的交互记录和上下文管理

### 2. 🧠 LangChain深度集成
- **预置智能Agent**: 3个专业级LangChain Agent
- **工具调用系统**: Web搜索、计算器、代码执行等
- **记忆系统**: 短期和长期记忆管理
- **链式调用**: 复杂的任务分解和执行

### 3. 💬 实时交互系统
- **WebSocket支持**: 实时消息推送
- **流式响应**: Token级别的流式输出
- **对话管理**: 多轮对话上下文保持
- **情绪识别**: Agent情绪状态反馈

### 4. 📊 监控和分析
- **性能指标**: 响应时间、成功率、错误率
- **使用统计**: Agent使用频率和模式分析
- **成本控制**: Token使用统计和成本估算
- **质量评估**: 交互质量评分和反馈

### 5. 🔧 开发者工具
- **API文档**: 完整的Swagger UI文档
- **SDK支持**: Python和JavaScript SDK
- **CLI工具**: 命令行管理工具
- **测试套件**: 单元测试和集成测试

## 📁 项目结构 - 企业级标准

```text
agent-learning-platform/
├── frontend/                    # 现代化前端项目
│   ├── src/
│   │   ├── views/               # 页面视图层
│   │   │   ├── Agent.vue        # Agent管理页面（核心）
│   │   │   ├── Community.vue    # 社区页面
│   │   │   └── Dashboard.vue    # 仪表板
│   │   ├── components/          # 可复用组件库
│   │   │   ├── AgentCard.vue    # Agent卡片组件
│   │   │   ├── Console.vue      # 交互控制台
│   │   │   └── StatusIndicator.vue # 状态指示器
│   │   ├── stores/              # Pinia状态管理
│   │   │   └── agentStore.ts    # Agent状态管理
│   │   ├── types/               # TypeScript类型定义
│   │   │   └── agent.ts         # Agent相关类型
│   │   ├── utils/               # 工具函数
│   │   │   └── api.ts           # API客户端
│   │   └── router/              # 路由配置
│   ├── public/                  # 静态资源
│   │   ├── index.html           # 主页面
│   │   └── test-*.html          # 功能测试页面
│   ├── package.json             # 依赖配置
│   ├── vite.config.ts           # Vite构建配置
│   └── tsconfig.json            # TypeScript配置
│
├── backend/                     # 高性能后端服务
│   ├── src/
│   │   ├── api/                 # API路由层
│   │   │   ├── v1/              # API版本1
│   │   │   │   ├── agents.py    # Agent管理API
│   │   │   │   └── health.py    # 健康检查API
│   │   │   └── __init__.py
│   │   ├── core/                # 核心配置
│   │   │   ├── config.py        # 应用配置
│   │   │   ├── database.py      # 数据库连接
│   │   │   └── middleware.py    # 中间件
│   │   ├── models/              # 数据模型
│   │   │   └── agent.py         # Agent数据模型
│   │   ├── services/            # 业务服务层
│   │   │   ├── agent_service.py # Agent业务逻辑
│   │   │   └── langchain_service.py # LangChain集成
│   │   └── main.py              # 应用入口
│   ├── start_unified.py         # 统一启动脚本
│   ├── requirements.txt         # Python依赖
│   └── check_status_simple.py   # 系统状态检查
│
├── docs/                        # 项目文档
│   ├── ARCHITECTURE.md          # 详细架构设计
│   ├── API-REFERENCE.md         # API参考文档
│   ├── DEPLOYMENT.md            # 部署指南
│   └── DEVELOPMENT.md           # 开发指南
│
├── docker/                      # Docker配置
│   ├── Dockerfile.frontend      # 前端Dockerfile
│   ├── Dockerfile.backend       # 后端Dockerfile
│   └── docker-compose.yml       # 容器编排
│
├── tests/                       # 测试套件
│   ├── frontend/                # 前端测试
│   └── backend/                 # 后端测试
│
├── .github/                     # GitHub工作流
│   └── workflows/               # CI/CD配置
│
├── README.md                    # 项目主文档（本文件）
├── LICENSE                      # MIT许可证
└── CONTRIBUTING.md              # 贡献指南
```

### 🏆 结构设计原则

1. **清晰的层次分离**
   - 前端/后端完全分离
   - API契约严格定义
   - 数据模型独立维护

2. **模块化组织**
   - 功能模块按目录组织
   - 可复用组件集中管理
   - 配置与代码分离

3. **开发友好**
   - 完整的类型定义
   - 详细的代码注释
   - 完善的测试覆盖

4. **部署就绪**
   - Docker容器化支持
   - 环境配置管理
   - 监控和日志集成

---

## 🛠️ 开发指南

### 🚀 本地开发环境

#### 1. 环境要求
- **Node.js** 18+ (前端)
- **Python** 3.9+ (后端)
- **PostgreSQL** 14+ (数据库)
- **Redis** 7+ (缓存)

#### 2. 快速启动

```bash
# 克隆项目
git clone https://github.com/MenFsq/agent-learning-platform.git
cd agent-learning-platform

# 启动后端服务（统一入口）
cd backend
pip install -r requirements.txt
python start_unified.py
# 访问 http://localhost:8004/docs 查看API文档

# 启动前端服务（新终端）
cd frontend
npm install
npm run dev
# 访问 http://localhost:5174/agent 使用平台
```

#### 3. 开发模式

```bash
# 前端热重载开发
cd frontend
npm run dev

# 后端热重载开发
cd backend
uvicorn src.main:app --reload --port 8004

# 运行测试
cd frontend && npm run test
cd backend && python -m pytest
```

### 📚 API文档

- **Swagger UI**: http://localhost:8004/docs
- **ReDoc**: http://localhost:8004/redoc
- **OpenAPI规范**: http://localhost:8004/openapi.json

### 🔍 调试工具

```bash
# 检查系统状态
cd backend
python check_status_simple.py

# 测试API端点
curl http://localhost:8004/health
curl http://localhost:8004/api/v1/agents

# 前端开发工具
cd frontend
npm run lint    # 代码检查
npm run build   # 生产构建
npm run preview # 预览构建
```

---

## 🐳 容器化部署

### 1. Docker快速部署

```bash
# 使用Docker Compose一键部署
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 2. Docker Compose配置

```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - VITE_API_BASE_URL=http://backend:8004
    depends_on:
      - backend

  backend:
    build: ./backend
    ports:
      - "8004:8004"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/agent_platform
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=agent_platform
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 3. 生产环境部署

#### Kubernetes部署
```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-platform
spec:
  replicas: 3
  selector:
    matchLabels:
      app: agent-platform
  template:
    metadata:
      labels:
        app: agent-platform
    spec:
      containers:
      - name: frontend
        image: menfsq/agent-platform-frontend:latest
        ports:
        - containerPort: 80
      - name: backend
        image: menfsq/agent-platform-backend:latest
        ports:
        - containerPort: 8004
```

#### 云原生特性
- **自动扩缩容**: 基于CPU/内存使用率
- **服务网格**: Istio流量管理
- **监控告警**: Prometheus + Grafana
- **日志收集**: ELK/EFK栈
- **安全扫描**: Trivy镜像扫描

### 4. 持续集成/持续部署

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build and push Docker images
      run: |
        docker build -t ${{ secrets.DOCKER_USERNAME }}/agent-platform-frontend:latest ./frontend
        docker build -t ${{ secrets.DOCKER_USERNAME }}/agent-platform