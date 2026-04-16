# Agent Learning Platform Architecture

## 架构说明

这份文档只回答两个问题：

1. 当前仓库实际上已经实现了什么。
2. 目标中的 `LangChain Agent` 集成应该怎么接进现有工程。

之前文档里把不少“计划中的 AI 能力”写成了“现有架构的一部分”，这会误导阅读者。这里按代码现状重新描述。

## 当前实际架构

### 前端

前端目前是一个以工作台为核心的 `Vue 3` 单页应用，主要承担展示和交互职责。

- 技术栈：`Vue 3` + `TypeScript` + `Vite` + `Pinia` + `Element Plus`
- 已有页面：仪表板、学习页、登录页、项目页/社区页/设置页占位
- 当前重点：学习内容展示、工作台导航、视觉系统、知识地图交互

前端里和 `LangChain` 最相关的部分，当前主要还是“学习内容与知识地图”，不是 Agent 运行能力本身。

### 后端

后端目前是一个 `FastAPI` 应用骨架，已经具备一些通用工程基础：

- 应用入口与生命周期管理
- 路由注册
- CORS / 日志 / 认证中间件
- 数据库初始化与健康检查
- 认证、项目、学习等 API 模块

但要注意，现有很多后端接口仍然偏“骨架态”或“模拟态”：

- 认证模块里有多处模拟返回
- 项目模块主要基于内存数据
- AI 相关能力并没有形成独立的后端服务层

### 数据与基础设施

当前基础设施设计倾向于：

- 数据库：`PostgreSQL` + `SQLAlchemy`
- 认证：`JWT`
- 缓存：预留 `Redis`
- AI 依赖：`langchain`、`openai`、`openclaw-sdk`

这里的重点是“依赖和方向已经声明”，不等于“功能已经完成”。

## 当前仓库中已经存在的能力边界

可以把当前代码理解成下面这套结构：

```text
Frontend UI
  -> 展示仪表板、学习工作台、导航和基础交互

Backend API
  -> 提供认证、项目、学习等基础接口

Data Layer
  -> 数据库配置、模型、基础持久化准备

AI Layer
  -> 目前仅有依赖声明和文案预留，尚未形成真实执行链
```

也就是说，项目现在最强的是“前端工作台 + 后端基础骨架”，最缺的是“真实 Agent 能力层”。

## 目标 Agent 架构

项目后续如果要真正完成 `LangChain Agent` 集成，建议采用下面这条分层：

```text
Frontend
  -> Agent Chat / Task UI / Run Status / Result View

API Layer (FastAPI)
  -> 请求入口、鉴权、参数校验、会话管理

Agent Application Layer
  -> AgentService / SessionService / RunService

LangChain Orchestration Layer
  -> Prompt / Tools / Memory / Agent Executor / Callbacks

Integration Layer
  -> LLM Provider / Vector Store / External APIs / Business Tools

Persistence Layer
  -> User / Session / Message / Run / Feedback / Evaluation
```

## 推荐的后端模块拆分

为了避免把 Agent 逻辑堆在路由文件里，后端建议新增类似结构：

```text
backend/src/
├── agent/
│   ├── prompts/
│   ├── tools/
│   ├── memory/
│   ├── chains/
│   ├── executors/
│   └── callbacks/
├── services/
│   ├── agent_service.py
│   ├── chat_service.py
│   └── session_service.py
└── api/v1/
    └── agent.py
```

各层职责建议如下：

- `api/v1/agent.py`：只处理 HTTP 输入输出，不写复杂业务逻辑
- `services/agent_service.py`：负责编排一次 Agent 调用流程
- `agent/prompts/`：维护系统提示词与任务模板
- `agent/tools/`：封装数据库查询、检索、外部 API、业务工具
- `agent/memory/`：管理会话历史和上下文裁剪
- `agent/callbacks/`：记录日志、trace、tokens、错误信息

## 第一阶段最小可运行链路

在当前项目阶段，不建议一开始就做很重的多 Agent 架构。更合理的是先打通一个最小闭环：

1. 前端提交一个用户问题
2. 后端 `/api/v1/agent/chat` 接收请求
3. `AgentService` 组装 prompt 和可用 tools
4. `LangChain` 执行单 Agent 调用
5. 返回文本结果、工具调用记录和耗时
6. 将会话与执行记录落库

只要这条链路真实可运行，项目就从“有 AI 方向”进入“有 AI 主能力”。

## 后续演进路线

### 阶段 1：单 Agent 可运行

- 支持单轮/多轮对话
- 接入基础模型
- 至少实现 1 到 2 个真实 tools
- 保存会话和运行日志

### 阶段 2：Agent 工程化

- 流式输出
- 可观测性和 trace
- Prompt 版本管理
- 失败重试和限流

### 阶段 3：更复杂的 Agent 能力

- RAG
- 多步骤任务执行
- 多 Agent 协作
- 评估与反馈闭环

## 当前架构结论

当前仓库适合被描述为：

- 一个已经完成前后端基础搭建的 Agent 平台雏形
- 一个已有较完整 `LangChain` 学习内容呈现的前端工作台
- 一个尚未真正接入 `LangChain Agent` 执行链的后端工程骨架

因此，后续架构工作的重心应放在 AI 能力层落地，而不是继续扩充“看起来很完整”的说明文档。