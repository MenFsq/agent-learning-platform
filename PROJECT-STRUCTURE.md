# Project Structure

该文档仅描述当前仓库的目录职责，不再包含启动步骤、进展和部署说明。

## 根目录

```text
agent-learning-platform/
├── .github/                    # Issue / PR 模板与工作流配置
├── backend/                    # FastAPI 后端代码
├── docs/                       # 额外文档与技术分享
├── frontend/                   # Vue 3 前端代码
├── scripts/                    # 自动化脚本
├── web-ui/                     # 历史或独立 UI 资源
├── README.md                   # 文档入口
├── QUICK-START.md              # 快速启动
├── ARCHITECTURE.md             # 架构说明
├── PROGRESS.md                 # 进展主文档
└── CONTRIBUTING.md             # 贡献指南
```

## 前端目录（`frontend/`）

- `src/components/`：可复用组件
- `src/views/`：页面级组件
- `src/router/`：路由定义
- `src/stores/`：状态管理
- `src/utils/`：工具函数
- `README.md`：前端模块说明

## 后端目录（`backend/`）

- `src/api/`：API 路由
- `src/core/`：核心配置与基础能力
- `src/models/`：数据库模型
- `src/services/`：业务服务层
- `src/middleware/`：中间件
- `README.md`：后端模块说明

## 文档分工原则

- 入口导航：`README.md`
- 启动步骤：`QUICK-START.md`
- 架构解释：`ARCHITECTURE.md`
- 进展记录：`PROGRESS.md`

遵循该分工可以避免同一内容在多个文档重复维护。
