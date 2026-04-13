# Agent Learning Platform - 项目结构说明

## 🏗️ 项目整体架构

```
agent-learning-platform/                    # 项目根目录
├── 📁 modules/                            # 核心功能模块
│   ├── project-dashboard/                 # 项目仪表板模块
│   │   ├── src/                          # 源代码
│   │   │   ├── components/               # Vue组件
│   │   │   │   ├── ProjectOverview.vue   # 项目概览组件
│   │   │   │   ├── TaskManager.vue       # 任务管理组件
│   │   │   │   ├── TechStack.vue         # 技术栈组件
│   │   │   │   ├── LearningProgress.vue  # 学习进度组件
│   │   │   │   ├── CommunityFeed.vue     # 社区动态组件
│   │   │   │   └── ProjectTimeline.vue   # 项目时间线组件
│   │   │   ├── composables/              # 组合式函数
│   │   │   │   ├── useTasks.ts          # 任务管理逻辑
│   │   │   │   ├── useProgress.ts       # 进度计算逻辑
│   │   │   │   └── useNotifications.ts  # 通知系统逻辑
│   │   │   ├── types/                    # TypeScript类型定义
│   │   │   │   ├── task.ts              # 任务类型
│   │   │   │   ├── project.ts           # 项目类型
│   │   │   │   └── user.ts              # 用户类型
│   │   │   └── utils/                    # 工具函数
│   │   │       ├── export.ts            # 数据导出
│   │   │       ├── import.ts            # 数据导入
│   │   │       └── validation.ts        # 数据验证
│   │   ├── tests/                        # 测试文件
│   │   │   ├── unit/                     # 单元测试
│   │   │   └── e2e/                      # 端到端测试
│   │   └── README.md                     # 模块文档
│   │
│   ├── learning-guide/                    # 学习指南模块
│   │   ├── tutorials/                     # 教程内容
│   │   │   ├── langchain-basics/         # LangChain基础
│   │   │   ├── openclaw-skills/          # OpenClaw技能开发
│   │   │   ├── vue-typescript/           # Vue 3 + TypeScript
│   │   │   └── enterprise-integration/   # 企业级集成
│   │   ├── exercises/                     # 练习项目
│   │   └── assessments/                   # 能力评估
│   │
│   ├── code-examples/                     # 代码示例模块
│   │   ├── langchain/                     # LangChain示例
│   │   ├── openclaw/                      # OpenClaw示例
│   │   ├── vue/                           # Vue示例
│   │   └── integration/                   # 集成示例
│   │
│   ├── community-integration/             # 社区集成模块
│   │   ├── botlearn-api/                  # BotLearn API集成
│   │   ├── content-publishing/            # 内容发布工具
│   │   ├── qa-system/                     # 问答系统
│   │   └── contributor-management/        # 贡献者管理
│   │
│   └── deployment-tools/                  # 部署工具模块
│       ├── docker/                        # Docker配置
│       ├── kubernetes/                    # Kubernetes配置
│       ├── monitoring/                    # 监控配置
│       └── ci-cd/                         # CI/CD配置
│
├── 📁 web-ui/                             # 前端界面
│   ├── dashboard/                         # 仪表板界面
│   │   ├── index.html                     # 主页面
│   │   ├── assets/                        # 静态资源
│   │   │   ├── css/                       # 样式文件
│   │   │   ├── js/                        # JavaScript文件
│   │   │   └── images/                    # 图片资源
│   │   └── components/                    # 独立组件
│   │
│   ├── learning-path/                     # 学习路径界面
│   ├── community-feed/                    # 社区动态界面
│   └── admin-panel/                       # 管理面板
│
├── 📁 backend/                            # 后端服务
│   ├── api-server/                        # API服务器
│   │   ├── src/                           # 源代码
│   │   │   ├── routes/                    # 路由定义
│   │   │   │   ├── projects/              # 项目相关路由
│   │   │   │   ├── tasks/                 # 任务相关路由
│   │   │   │   ├── users/                 # 用户相关路由
│   │   │   │   └── community/             # 社区相关路由
│   │   │   ├── controllers/               # 控制器
│   │   │   ├── services/                  # 业务逻辑
│   │   │   ├── models/                    # 数据模型
│   │   │   ├── middleware/                # 中间件
│   │   │   └── utils/                     # 工具函数
│   │   ├── tests/                         # 测试文件
│   │   └── Dockerfile                     # Docker配置
│   │
│   ├── agent-core/                        # Agent核心逻辑
│   │   ├── langchain-integration/         # LangChain集成
│   │   ├── openclaw-sdk/                  # OpenClaw SDK集成
│   │   ├── knowledge-base/                # 知识库管理
│   │   └── skill-manager/                 # 技能管理器
│   │
│   └── data-pipeline/                     # 数据处理流水线
│       ├── document-processor/            # 文档处理器
│       ├── vector-database/               # 向量数据库
│       ├── cache-manager/                 # 缓存管理器
│       └── batch-processor/               # 批处理器
│
├── 📁 docs/                               # 项目文档
│   ├── tutorials/                         # 教程文档
│   │   ├── 01-getting-started.md         # 快速开始
│   │   ├── 02-langchain-basics.md        # LangChain基础
│   │   ├── 03-openclaw-skills.md         # OpenClaw技能开发
│   │   ├── 04-vue-typescript.md          # Vue 3 + TypeScript
│   │   ├── 05-enterprise-integration.md  # 企业级集成
│   │   └── 06-deployment-guide.md        # 部署指南
│   │
│   ├── api-reference/                     # API参考
│   │   ├── rest-api/                      # REST API文档
│   │   ├── graphql-api/                   # GraphQL API文档
│   │   └── websocket-api/                 # WebSocket API文档
│   │
│   ├── best-practices/                    # 最佳实践
│   │   ├── code-organization.md          # 代码组织
│   │   ├── testing-strategy.md           # 测试策略
│   │   ├── security-guide.md             # 安全指南
│   │   └── performance-optimization.md   # 性能优化
│   │
│   └── contribution-guide/                # 贡献指南
│       ├── code-style.md                  # 代码风格
│       ├── pull-request-process.md       # PR流程
│       ├── issue-templates.md            # Issue模板
│       └── release-process.md            # 发布流程
│
├── 📁 deployment/                         # 部署配置
│   ├── docker/                            # Docker配置
│   │   ├── docker-compose.yml            # Docker Compose配置
│   │   ├── Dockerfile.api                 # API服务Dockerfile
│   │   ├── Dockerfile.web                 # Web界面Dockerfile
│   │   └── Dockerfile.agent              # Agent服务Dockerfile
│   │
│   ├── kubernetes/                        # Kubernetes配置
│   │   ├── manifests/                     # K8s清单文件
│   │   │   ├── deployment.yaml           # 部署配置
│   │   │   ├── service.yaml              # 服务配置
│   │   │   ├── ingress.yaml              # 入口配置
│   │   │   └── configmap.yaml            # 配置映射
│   │   ├── helm-chart/                    # Helm Chart
│   │   └── terraform/                     # Terraform配置
│   │
│   └── ci-cd/                             # CI/CD配置
│       ├── github-actions/                # GitHub Actions
│       ├── gitlab-ci/                     # GitLab CI
│       └── jenkins/                       # Jenkins配置
│
├── 📁 tests/                              # 测试目录
│   ├── unit/                              # 单元测试
│   │   ├── frontend/                      # 前端单元测试
│   │   ├── backend/                       # 后端单元测试
│   │   └── shared/                        # 共享单元测试
│   │
│   ├── integration/                       # 集成测试
│   │   ├── api/                           # API集成测试
│   │   ├── database/                      # 数据库集成测试
│   │   └── external-services/             # 外部服务集成测试
│   │
│   ├── e2e/                               # 端到端测试
│   │   ├── cypress/                       # Cypress测试
│   │   ├── playwright/                    # Playwright测试
│   │   └── selenium/                      # Selenium测试
│   │
│   └── performance/                       # 性能测试
│       ├── load-testing/                  # 负载测试
│       ├── stress-testing/                # 压力测试
│       └── benchmark/                     # 基准测试
│
├── 📁 scripts/                            # 脚本文件
│   ├── setup/                             # 环境设置脚本
│   ├── build/                             # 构建脚本
│   ├── deploy/                            # 部署脚本
│   ├── monitoring/                        # 监控脚本
│   └── maintenance/                       # 维护脚本
│
├── 📁 config/                             # 配置文件
│   ├── development/                       # 开发环境配置
│   ├── staging/                           # 预发布环境配置
│   ├── production/                        # 生产环境配置
│   └── local/                             # 本地环境配置
│
├── 📁 data/                               # 数据目录
│   ├── databases/                         # 数据库文件
│   ├── vector-stores/                     # 向量存储文件
│   ├── cache/                             # 缓存文件
│   └── backups/                           # 备份文件
│
├── 📁 logs/                               # 日志目录
│   ├── application/                       # 应用日志
│   ├── access/                            # 访问日志
│   ├── error/                             # 错误日志
│   └── audit/                             # 审计日志
│
└── 📁 .github/                            # GitHub配置
    ├── workflows/                         # GitHub Actions工作流
    ├── ISSUE_TEMPLATE/                    # Issue模板
    └── PULL_REQUEST_TEMPLATE/             # PR模板
```

## 🚀 开发环境设置

### 1. 前端开发环境
```bash
# 进入前端目录
cd web-ui/dashboard

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 运行测试
npm run test
```

### 2. 后端开发环境
```bash
# 进入后端目录
cd backend/api-server

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 运行测试
pytest
```

### 3. 使用Docker开发
```bash
# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📦 模块依赖关系

```
前端界面 (web-ui)
    ├── 依赖: 项目仪表板模块 (modules/project-dashboard)
    ├── 依赖: 学习指南模块 (modules/learning-guide)
    └── 依赖: 社区集成模块 (modules/community-integration)

后端服务 (backend)
    ├── 依赖: Agent核心逻辑 (backend/agent-core)
    ├── 依赖: 数据处理流水线 (backend/data-pipeline)
    └── 提供: REST API接口

核心模块 (modules)
    ├── 项目仪表板模块: 提供项目管理功能
    ├── 学习指南模块: 提供学习内容和路径
    ├── 代码示例模块: 提供可运行代码示例
    ├── 社区集成模块: 提供社区互动功能
    └── 部署工具模块: 提供部署和运维工具
```

## 🔧 技术栈详细说明

### 前端技术栈
- **Vue 3** - 渐进式JavaScript框架
- **TypeScript** - 类型安全的JavaScript超集
- **Vite** - 下一代前端构建工具
- **Pinia** - Vue状态管理库
- **Vue Router** - Vue官方路由
- **Element Plus** - Vue 3组件库
- **ECharts** - 数据可视化库
- **Axios** - HTTP客户端
- **Vitest** - 测试框架

### 后端技术栈
- **Python 3.9+** - 后端编程语言
- **FastAPI** - 现代Web框架
- **SQLAlchemy** - SQL工具包和ORM
- **Alembic** - 数据库迁移工具
- **Pydantic** - 数据验证
- **JWT** - JSON Web Token认证
- **Redis** - 内存数据存储
- **Celery** - 分布式任务队列
- **LangChain** - AI应用框架
- **OpenClaw SDK** - OpenClaw平台SDK

### 数据库
- **PostgreSQL** - 关系型数据库
- **Redis** - 缓存和会话存储
- **Chroma DB** - 向量数据库
- **Elasticsearch** - 全文搜索引擎

### 基础设施
- **Docker** - 容器化平台
- **Docker Compose** - 多容器应用编排
- **Kubernetes** - 容器编排平台
- **Nginx** - Web服务器和反向代理
- **Prometheus** - 监控系统
- **Grafana** - 数据可视化平台
- **GitHub Actions** - CI/CD流水线

## 📁 文件命名规范

### 前端文件
- **组件文件**: `PascalCase.vue` (如: `ProjectOverview.vue`)
- **组合式函数**: `useCamelCase.ts` (如: `useTasks.ts`)
- **工具函数**: `camelCase.ts` (如: `export.ts`)
- **类型定义**: `camelCase.ts` (如: `task.ts`)

### 后端文件
- **Python模块**: `snake_case.py` (如: `task_manager.py`)
- **路由文件**: `snake_case.py` (如: `task_routes.py`)
- **模型文件**: `snake_case.py` (如: `task_model.py`)
- **配置文件**: `snake_case.yaml` (如: `database_config.yaml`)

### 文档文件
- **Markdown文档**: `kebab-case.md` (如: `getting-started.md`)
- **API文档**: `kebab-case.md` (如: `rest-api-reference.md`)
- **教程文档**: `数字-标题.md` (如: `01-getting-started.md`)

## 🎯 开发工作流

### 1. 功能开发流程
```bash
# 1. 创建功能分支
git checkout -b feature/项目仪表板

# 2. 开发功能
# - 编写代码
# - 添加测试
# - 更新文档

# 3. 提交更改
git add .
git commit -m "feat(project-dashboard): 添加项目概览组件"

# 4. 推送到远程
git push origin feature/项目仪表板

# 5. 创建Pull Request
# - 通过GitHub创建PR
# - 等待代码审查
# - 通过CI/CD检查
# - 合并到主分支
```

### 2. 代码审查标准
- ✅ 代码符合项目规范
- ✅ 包含必要的测试
- ✅ 文档已更新
- ✅ 通过所有CI检查
- ✅ 性能影响评估
- ✅ 安全审查通过

### 3. 发布流程
```bash
# 1. 版本号更新
npm version patch  # 或 minor/major

# 2. 构建发布版本
npm run build

# 3. 运行完整测试套件
npm run test:all

# 4.