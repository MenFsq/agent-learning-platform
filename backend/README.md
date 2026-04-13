# Agent Learning Platform - 后端项目

## 🎯 项目概述

这是 Agent Learning Platform 的后端项目，基于 FastAPI + LangChain + OpenClaw SDK 构建的高性能 API 服务。

## 🚀 快速开始

### 环境要求
- Python 3.10+
- PostgreSQL 15+
- Redis 7+ (可选，用于缓存)

### 安装依赖
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 环境配置
复制 `.env.example` 为 `.env` 并配置：
```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
# 数据库配置
DATABASE_URL=postgresql://user:password@localhost:5432/agent_platform

# 安全配置
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI服务配置
OPENAI_API_KEY=your-openai-api-key
OPENCLAW_API_KEY=your-openclaw-api-key

# 应用配置
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ORIGINS=http://localhost:5173
```

### 初始化数据库
```bash
# 创建数据库
createdb agent_platform

# 运行数据库迁移
alembic upgrade head

# 创建初始数据
python scripts/create_initial_data.py
```

### 启动开发服务器
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 访问API文档
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 📁 项目结构

```
backend/
├── 📁 src/                    # 源代码目录
│   ├── 📁 api/               # API路由
│   │   ├── 📁 v1/           # API版本1
│   │   │   ├── auth.py      # 认证相关API
│   │   │   ├── projects.py  # 项目相关API
│   │   │   ├── learning.py  # 学习相关API
│   │   │   ├── ai.py        # AI相关API
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── 📁 core/             # 核心模块
│   │   ├── config.py        # 配置管理
│   │   ├── security.py      # 安全相关
│   │   ├── database.py      # 数据库连接
│   │   └── __init__.py
│   ├── 📁 models/           # 数据模型
│   │   ├── user.py          # 用户模型
│   │   ├── project.py       # 项目模型
│   │   ├── learning.py      # 学习模型
│   │   └── __init__.py
│   ├── 📁 schemas/          # Pydantic模式
│   │   ├── user.py          # 用户模式
│   │   ├── project.py       # 项目模式
│   │   ├── learning.py      # 学习模式
│   │   └── __init__.py
│   ├── 📁 services/         # 业务服务
│   │   ├── auth_service.py  # 认证服务
│   │   ├── project_service.py # 项目服务
│   │   ├── learning_service.py # 学习服务
│   │   ├── ai_service.py    # AI服务
│   │   └── __init__.py
│   ├── 📁 utils/            # 工具函数
│   │   ├── logger.py        # 日志工具
│   │   ├── validator.py     # 验证工具
│   │   ├── formatter.py     # 格式化工具
│   │   └── __init__.py
│   ├── 📁 middleware/       # 中间件
│   │   ├── auth.py          # 认证中间件
│   │   ├── cors.py          # CORS中间件
│   │   ├── logging.py       # 日志中间件
│   │   └── __init__.py
│   ├── main.py              # 应用入口
│   └── __init__.py
├── 📁 alembic/              # 数据库迁移
│   ├── versions/            # 迁移版本
│   ├── env.py               # 迁移环境
│   └── script.py.mako       # 迁移模板
├── 📁 tests/                # 测试文件
│   ├── 📁 unit/             # 单元测试
│   ├── 📁 integration/      # 集成测试
│   └── conftest.py          # 测试配置
├── 📁 scripts/              # 脚本文件
│   ├── create_initial_data.py # 初始数据
│   ├── backup_database.py   # 数据库备份
│   └── health_check.py      # 健康检查
├── requirements.txt         # Python依赖
├── requirements-dev.txt     # 开发依赖
├── .env.example             # 环境变量示例
├── .env                     # 环境变量
├── alembic.ini              # 迁移配置
├── Dockerfile               # Docker配置
└── README.md                # 项目文档
```

## 🔧 技术栈

### 核心框架
- **FastAPI** - 高性能 Python Web 框架
- **SQLAlchemy** - Python SQL 工具包和 ORM
- **Alembic** - 数据库迁移工具

### 数据库
- **PostgreSQL** - 关系型数据库
- **Redis** - 缓存数据库 (可选)

### AI集成
- **LangChain** - AI应用开发框架
- **OpenClaw SDK** - OpenClaw 平台集成
- **OpenAI API** - GPT模型集成

### 安全认证
- **JWT** - JSON Web Tokens
- **OAuth2** - 认证授权
- **bcrypt** - 密码哈希

### 开发工具
- **Pydantic** - 数据验证
- **Pytest** - 测试框架
- **Black** - 代码格式化
- **Flake8** - 代码检查

## 🌐 API设计

### RESTful API 规范
- 使用 HTTP 方法: GET, POST, PUT, DELETE
- 资源命名使用复数形式
- 版本控制: `/api/v1/`
- 统一响应格式

### 响应格式
```json
{
  "success": true,
  "data": {...},
  "message": "操作成功",
  "code": 200
}
```

### 错误处理
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "输入数据验证失败",
    "details": {...}
  }
}
```

## 🔐 安全架构

### 认证流程
1. 用户登录获取 JWT Token
2. Token 存储在 HTTP Only Cookie
3. 后续请求携带 Token
4. 服务端验证 Token

### 权限控制
- 基于角色的访问控制 (RBAC)
- 资源级别的权限检查
- API 访问频率限制

### 数据安全
- SQL 注入防护
- XSS 防护
- CSRF 防护
- 输入验证和清理

## 🗄️ 数据库设计

### 核心表结构
```sql
-- 用户表
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 项目表
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 学习进度表
CREATE TABLE learning_progress (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    module_id VARCHAR(100) NOT NULL,
    progress INTEGER DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 数据库迁移
```bash
# 创建新迁移
alembic revision --autogenerate -m "添加新功能"

# 应用迁移
alembic upgrade head

# 回滚迁移
alembic downgrade -1
```

## 🤖 AI集成

### LangChain 集成
```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

# 创建LLM链
llm = OpenAI(temperature=0.7)
prompt = PromptTemplate(
    input_variables=["topic"],
    template="请解释{topic}的概念"
)
chain = LLMChain(llm=llm, prompt=prompt)

# 执行链
result = chain.run(topic="机器学习")
```

### OpenClaw 集成
```python
from openclaw import OpenClawClient

# 初始化客户端
client = OpenClawClient(api_key=settings.OPENCLAW_API_KEY)

# 调用技能
response = client.skills.execute(
    skill_name="code-reviewer",
    input={"code": "def hello(): print('world')"}
)
```

## 📊 监控与日志

### 日志配置
- 结构化日志输出
- 日志级别控制
- 日志文件轮转

### 性能监控
- 请求响应时间
- 数据库查询性能
- 内存使用情况

### 健康检查
```bash
# 健康检查端点
GET /health

# 响应
{
  "status": "healthy",
  "timestamp": "2026-04-13T15:42:00Z",
  "services": {
    "database": "connected",
    "redis": "connected",
    "ai_service": "available"
  }
}
```

## 🚀 性能优化

### 数据库优化
- 连接池配置
- 查询优化
- 索引优化
- 缓存策略

### API优化
- 响应压缩
- 分页查询
- 懒加载
- 异步处理

### 缓存策略
- Redis 缓存热点数据
- 内存缓存常用配置
- CDN 缓存静态资源

## 🐳 部署

### Docker部署
```dockerfile
# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 运行应用
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/agent_platform
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=agent_platform
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

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
pytest

# 运行单元测试
pytest tests/unit/

# 运行集成测试
pytest tests/integration/

# 生成测试报告
pytest --cov=src --cov-report=html
```

### 测试覆盖率
- 单元测试覆盖率 > 85%
- 集成测试关键路径
- API 端点测试

## 🔄 CI/CD

### GitHub Actions
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r requirements.txt -r requirements-dev.txt
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 🤝 贡献指南

1. 阅读开发规范
2. 创建功能分支
3. 编写测试用例
4. 提交代码审查
5. 等待合并

## 📞 支持与反馈

- 问题反馈: GitHub Issues
- 安全漏洞: 安全邮件
- 功能建议: GitHub Discussions

---

**最后更新**: 2026-04-13  
**维护者**: 小老虎 🐯