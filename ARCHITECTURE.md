# Agent Learning Platform - 前后端分离架构

## 🏗️ 架构概述

本项目采用现代化的前后端分离架构，前端使用 Vue 3 + TypeScript，后端使用 FastAPI + LangChain。

### **前端 (Frontend)**
- **技术栈**: Vue 3 + TypeScript + Vite + Pinia + Element Plus
- **开发服务器**: `localhost:5173`
- **构建工具**: Vite
- **状态管理**: Pinia
- **UI框架**: Element Plus

### **后端 (Backend)**
- **技术栈**: FastAPI + LangChain + OpenClaw SDK + PostgreSQL
- **开发服务器**: `localhost:8000`
- **API文档**: Swagger UI (`/docs`)
- **数据库**: PostgreSQL + SQLAlchemy
- **AI集成**: LangChain + OpenClaw

## 📁 目录结构

```
agent-learning-platform/
├── 📁 frontend/                    # 前端项目
│   ├── 📁 src/                    # 源代码
│   │   ├── 📁 components/         # Vue组件
│   │   ├── 📁 views/             # 页面组件
│   │   ├── 📁 composables/       # 组合式函数
│   │   ├── 📁 stores/            # Pinia状态管理
│   │   ├── 📁 types/             # TypeScript类型
│   │   ├── 📁 utils/             # 工具函数
│   │   ├── 📁 assets/            # 静态资源
│   │   ├── App.vue               # 根组件
│   │   └── main.ts               # 入口文件
│   ├── index.html                # HTML模板
│   ├── package.json              # 依赖配置
│   ├── vite.config.ts            # Vite配置
│   ├── tsconfig.json             # TypeScript配置
│   └── README.md                 # 前端文档
│
├── 📁 backend/                    # 后端项目
│   ├── 📁 src/                   # 源代码
│   │   ├── 📁 api/              # API路由
│   │   ├── 📁 core/             # 核心逻辑
│   │   ├── 📁 models/           # 数据模型
│   │   ├── 📁 services/         # 业务服务
│   │   ├── 📁 utils/            # 工具函数
│   │   ├── 📁 middleware/       # 中间件
│   │   ├── main.py              # 应用入口
│   │   └── config.py            # 配置管理
│   ├── requirements.txt          # Python依赖
│   ├── Dockerfile               # Docker配置
│   ├── alembic.ini              # 数据库迁移配置
│   └── README.md                # 后端文档
│
├── 📁 docs/                      # 项目文档
├── 📁 scripts/                   # 自动化脚本
├── 📁 docker/                    # Docker配置
├── 📄 README.md                  # 项目总览
├── 📄 ARCHITECTURE.md            # 架构说明
├── 📄 .gitignore                 # Git忽略配置
└── 📄 docker-compose.yml         # Docker编排
```

## 🔧 开发环境设置

### **前端开发**
```bash
cd frontend
npm install          # 安装依赖
npm run dev          # 启动开发服务器
```

### **后端开发**
```bash
cd backend
python -m venv venv  # 创建虚拟环境
venv\Scripts\activate # 激活虚拟环境
pip install -r requirements.txt  # 安装依赖
uvicorn src.main:app --reload    # 启动开发服务器
```

## 🌐 API接口设计

### **认证相关**
- `POST /api/auth/login` - 用户登录
- `POST /api/auth/register` - 用户注册
- `GET /api/auth/profile` - 获取用户信息

### **项目相关**
- `GET /api/projects` - 获取项目列表
- `POST /api/projects` - 创建项目
- `GET /api/projects/{id}` - 获取项目详情
- `PUT /api/projects/{id}` - 更新项目
- `DELETE /api/projects/{id}` - 删除项目

### **学习相关**
- `GET /api/learning-paths` - 获取学习路径
- `GET /api/tutorials` - 获取教程列表
- `POST /api/progress` - 更新学习进度

### **AI相关**
- `POST /api/ai/chat` - AI对话接口
- `POST /api/ai/code-review` - 代码审查
- `POST /api/ai/generate-example` - 生成代码示例

## 🐳 部署方案

### **开发环境**
```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/agent_platform
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENCLAW_API_KEY=${OPENCLAW_API_KEY}
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=agent_platform
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### **生产环境**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./frontend/dist:/usr/share/nginx/html
  
  backend:
    build: ./backend
    restart: always
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/agent_platform
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENCLAW_API_KEY=${OPENCLAW_API_KEY}
  
  db:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=agent_platform
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🔄 开发工作流

1. **前端开发**
   - 在 `frontend/` 目录中开发
   - 使用 Vite 热重载
   - 通过代理连接到后端 API

2. **后端开发**
   - 在 `backend/` 目录中开发
   - 使用 FastAPI 自动生成 API 文档
   - 使用 Alembic 管理数据库迁移

3. **API集成**
   - 前端通过 `axios` 调用后端 API
   - 使用环境变量配置 API 地址
   - 统一的错误处理

## 📊 监控与日志

### **前端监控**
- 使用 Vue DevTools 调试
- 错误边界处理
- 性能监控

### **后端监控**
- FastAPI 内置日志
- 结构化日志输出
- 性能指标收集

## 🔐 安全考虑

1. **认证授权**
   - JWT Token 认证
   - 角色权限控制
   - API 访问限制

2. **数据安全**
   - SQL 注入防护
   - XSS 防护
   - CSRF 防护

3. **API安全**
   - 请求速率限制
   - 输入验证
   - 输出过滤

## 🚀 性能优化

### **前端优化**
- 代码分割
- 懒加载路由
- 图片优化
- 缓存策略

### **后端优化**
- 数据库连接池
- 查询优化
- 缓存机制
- 异步处理

---

**最后更新**: 2026-04-13  
**架构师**: 小老虎 🐯