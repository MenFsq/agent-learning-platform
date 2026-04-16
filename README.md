# Agent Learning Platform

> 前后端分离的 AI Agent 学习平台架构设计

![Vue 3](https://img.shields.io/badge/Frontend-Vue%203-42b883?style=for-the-badge&logo=vuedotjs&logoColor=white)
![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178c6?style=for-the-badge&logo=typescript&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![LangChain](https://img.shields.io/badge/AI-LangChain-1c3c3c?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)

`Agent Learning Platform` 是一个面向 AI Agent 开发者的学习与实践平台，目标是通过结构化学习路径、完整项目架构和社区协作方式，帮助开发者更系统地学习 `LangChain`、`OpenClaw` 以及现代 Agent 应用开发。

GitHub 仓库：[MenFsq/agent-learning-platform](https://github.com/MenFsq/agent-learning-platform)

## 🎯 项目愿景

在 AI Agent 快速发展的今天，我们发现很多开发者面临几个共同问题：

- 学习曲线陡峭，`LangChain`、`OpenClaw` 等工具上手成本较高
- 实践机会有限，缺少从架构到功能落地的完整项目案例
- 社区交流分散，缺少系统化的知识沉淀与协作空间

因此，我们希望通过这个项目：

- 提供结构化的学习路径
- 展示完整的项目架构设计
- 促进社区技术交流与开源协作

## 🏗️ 项目架构概述

项目采用前后端分离架构，围绕“学习平台 + Agent 实践 + 社区协作”三个方向展开设计。

### 前端架构 Frontend

前端负责承载学习工作台、项目仪表板、交互式界面和社区入口，强调现代化开发体验与组件化组织。

- `Vue 3`：现代化前端框架
- `TypeScript`：增强类型安全与可维护性
- `Vite`：提供高效开发与构建体验
- `Element Plus`：企业级 UI 组件库
- `Pinia`：轻量级状态管理
- `Vue Router`：前端路由管理

### 后端架构 Backend

后端负责 API 服务、业务逻辑、Agent 能力集成、数据存储与系统支撑能力。

- `FastAPI`：高性能 Python API 框架
- `LangChain`：AI Agent 开发框架
- `OpenClaw SDK`：技能开发与平台集成工具
- `PostgreSQL`：关系型数据库
- `Redis`：缓存与消息能力支撑

## 🌟 架构设计原则

### 1. 前后端分离优势

- 技术栈独立，前后端可以选择最适合自身场景的技术
- 支持并行开发，提升团队协作效率
- 部署方式灵活，便于独立扩展与演进
- 职责边界清晰，降低维护复杂度

### 2. 模块化设计

- 前端采用组件化与页面化组织方式
- 后端采用路由、服务、模型分层设计
- 数据访问通过 ORM 抽象
- API 设计遵循标准化与可扩展原则

### 3. 可扩展性考虑

- 支持后续增加更多 Agent 能力和业务模块
- 支持通过配置管理不同环境
- 为日志、监控、安全与权限体系预留扩展空间
- 支持向插件化、服务化方向持续演进

## 🚀 核心功能模块

### 1. 项目仪表板

- 可视化项目管理
- 进度跟踪与统计分析
- 团队协作入口

### 2. 学习管理系统

- 结构化学习路径
- 交互式教程与知识地图
- 学习进度跟踪

### 3. 代码实验室与实践

- 面向 Agent 开发的实践空间
- 代码示例与实验能力扩展
- 面向真实项目的开发演练

### 4. 社区集成

- 社区交流入口
- 技术讨论与经验分享
- 面向开源协作的参与机制

## 📁 项目结构亮点

```text
agent-learning-platform/
├── frontend/                    # 前端项目
│   ├── src/
│   │   ├── views/               # 页面组件（仪表板、项目、学习等）
│   │   ├── components/          # 可复用组件
│   │   ├── stores/              # Pinia 状态管理
│   │   └── types/               # TypeScript 类型定义
│   └── vite.config.ts           # Vite 配置
│
├── backend/                     # 后端项目
│   ├── src/
│   │   ├── api/                 # API 路由
│   │   ├── core/                # 核心配置与基础能力
│   │   ├── models/              # 数据模型
│   │   └── services/            # 业务服务
│   └── requirements.txt         # Python 依赖
│
├── ARCHITECTURE.md              # 详细架构说明
├── QUICK-START.md               # 快速启动文档
├── PROJECT-STRUCTURE.md         # 目录结构说明
└── PROGRESS.md                  # 项目进度记录
```

## 🔧 开发体验

### 前端开发

```bash
cd frontend
npm install
npm run dev
```

### 后端开发

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### API 文档

- Swagger UI：`http://localhost:8000/docs`
- ReDoc：`http://localhost:8000/redoc`

更多本地启动说明见 `QUICK-START.md`。

## 🐳 部署方案

项目支持本地开发、容器化部署和后续生产环境扩展。

### Docker 开发环境

```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "5173:5173"

  backend:
    build: ./backend
    ports:
      - "8000:8000"

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=agent_platform
```

### 生产环境部署

- `Nginx` 反向代理
- `HTTPS` 配置
- 数据库备份
- 日志与监控告警

## 🤝 开源协作模式

### 贡献者等级体系

- 初学者：完成教程，提交第一个 PR
- 贡献者：修复问题，补充小功能
- 核心贡献者：参与模块开发与代码审查
- 维护者：参与项目方向、版本发布与协作管理

### 社区参与方式

- 报告问题：通过 GitHub Issues 反馈
- 提交代码：Fork 仓库并发起 Pull Request
- 完善文档：补充教程、说明和示例
- 分享经验：围绕 Agent 开发与实践展开交流

## 📚 学习资源

### 入门教程系列

- 从零开始搭建第一个 AI Agent
- `LangChain` 核心概念与应用方式
- `OpenClaw` 技能开发指南
- `Vue 3 + TypeScript` 工程实践

### 实战项目案例

- 智能文档助手
- 代码审查 Agent
- 学习进度跟踪系统

## 🎯 技术影响力建设

通过这个项目，我们希望：

- 为 AI Agent 开发提供可参考的架构设计
- 通过真实项目帮助开发者提升工程实践能力
- 促进社区内围绕 Agent 技术的交流与沉淀
- 为开源 AI Agent 生态贡献一套持续演进的平台基础

## 🔗 相关链接

- GitHub 仓库：[https://github.com/MenFsq/agent-learning-platform](https://github.com/MenFsq/agent-learning-platform)
- 架构文档：[https://github.com/MenFsq/agent-learning-platform/blob/main/ARCHITECTURE.md](https://github.com/MenFsq/agent-learning-platform/blob/main/ARCHITECTURE.md)
- 问题反馈：[https://github.com/MenFsq/agent-learning-platform/issues](https://github.com/MenFsq/agent-learning-platform/issues)

让我们共同打造一个优秀的 AI Agent 学习生态系统！🚀
