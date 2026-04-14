# Agent Learning Platform Frontend

## 项目概述

这是 `Agent Learning Platform` 的前端工程，基于 `Vue 3 + TypeScript + Vite` 构建，当前重点实现的是一个偏工作台形态的 AI Agent 学习与项目协作界面。

目前已经成型的核心体验包括：

- 仪表板首页：展示项目进度、学习进度、快捷入口和社区动态
- 学习工作台：用可交互的知识地图串联阶段、节点、资料和学习动作
- 顶部工作台导航：统一承载搜索、通知、主题切换和用户入口
- 全局视觉系统：暗色默认、支持亮色切换，统一使用设计 token 和玻璃态面板风格

## 环境要求

- `Node.js >= 24`
- `npm >= 10`

以上要求以 `package.json` 中的 `engines` 配置为准。

## 快速开始

### 安装依赖

```bash
npm install
```

### 启动开发环境

```bash
npm run dev
```

默认使用 Vite 本地服务：

- 地址：`http://localhost:5174`
- API 代理：`/api -> http://localhost:8000`

### 构建生产包

```bash
npm run build
```

### 本地预览构建结果

```bash
npm run preview
```

### 其他常用脚本

```bash
npm run lint
npm run format
npm run type-check
npm run test
npm run test:ui
npm run test:coverage
```

## 当前页面与路由

| 路由 | 页面 | 当前状态 |
| --- | --- | --- |
| `/` | 仪表板 `Dashboard.vue` | 已完成主要展示结构 |
| `/learning` | 学习工作台 `Learning.vue` | 已完成核心交互和地图工作区 |
| `/projects` | 项目管理 `Projects.vue` | 预留占位页 |
| `/community` | 社区动态 `Community.vue` | 预留占位页 |
| `/settings` | 系统设置 `Settings.vue` | 预留占位页 |
| `/login` | 登录页 `Login.vue` | 独立页面，不显示主头部 |
| `/:pathMatch(.*)*` | 404 `NotFound.vue` | 兜底路由 |

## 当前实现重点

### 1. 仪表板首页

首页位于 `src/views/Dashboard.vue`，目前由多个卡片化模块组成：

- `DashboardHero`：顶部欢迎区和关键指标
- `OverviewStats`：进度、任务、学习完成率、运行次数等概览
- `ProjectShowcase`：项目进展卡片
- `LearningRail`：学习路径横向卡片流
- `QuickEntryGrid`：快捷入口
- `CommunityTicker`：社区动态播报

页面还集成了 `tsparticles` 背景粒子效果，以及基于 `IntersectionObserver` 的滚动 reveal 动画。

### 2. 学习工作台

学习页位于 `src/views/Learning.vue`，围绕 “先看整体，再钻细节” 的使用路径组织：

- 顶部 Hero 区：学习主题说明和快捷动作按钮
- 学习概览：阶段数量、节点数量等总览指标
- 阶段节奏：推荐学习顺序和时间预期
- 核心工作区：交互式知识地图
- 学习原则：总结当前页面的学习方式

知识地图工作区由 `src/components/LangChainMindMap.vue` 负责组装，内部主要包含：

- `LearningMapCanvas`：基于 `@vue-flow/core` 的节点/连线画布
- `LearningStagePanel`：阶段视图与节点切换
- `LearningNodeDetail`：当前节点详细说明
- `LearningResourcePanel`：资料面板
- `LearningLegend`：图例说明

### 3. 顶部工作台导航

顶部导航位于 `src/components/Layout/AppHeader.vue`，当前包含：

- 主导航入口：仪表板、项目、学习、社区、设置
- 搜索框：用于统一搜索入口展示
- 主题切换：深浅色切换
- 通知预览：下拉通知卡片
- 用户菜单：个人资料、偏好和系统设置入口

## 技术栈

### 框架与基础设施

- `Vue 3`
- `TypeScript`
- `Vite`
- `Vue Router`
- `Pinia`

### UI 与交互

- `Element Plus`
- `lucide-vue-next`
- `@vue-flow/core`
- `particles.vue3`
- `@tsparticles/slim`

### 工程化

- `ESLint`
- `Prettier`
- `Vitest`
- `Vue Test Utils`
- `vue-tsc`

## 项目结构

当前项目结构更接近下面这种组织方式：

```text
frontend/
├── src/
│   ├── App.vue
│   ├── main.ts
│   ├── router/
│   │   └── index.ts
│   ├── store/
│   │   └── app.ts
│   ├── views/
│   │   ├── Dashboard.vue
│   │   ├── Learning.vue
│   │   ├── Projects.vue
│   │   ├── Community.vue
│   │   ├── Settings.vue
│   │   ├── Login.vue
│   │   └── NotFound.vue
│   ├── components/
│   │   ├── Layout/
│   │   │   └── AppHeader.vue
│   │   ├── dashboard/
│   │   │   ├── DashboardHero.vue
│   │   │   ├── OverviewStats.vue
│   │   │   ├── ProjectShowcase.vue
│   │   │   ├── LearningRail.vue
│   │   │   ├── QuickEntryGrid.vue
│   │   │   ├── CommunityTicker.vue
│   │   │   ├── SectionHeader.vue
│   │   │   ├── AnimatedNumber.vue
│   │   │   └── types.ts
│   │   ├── learning/
│   │   │   ├── LearningMapCanvas.vue
│   │   │   ├── LearningStagePanel.vue
│   │   │   ├── LearningNodeDetail.vue
│   │   │   ├── LearningResourcePanel.vue
│   │   │   └── LearningLegend.vue
│   │   └── LangChainMindMap.vue
│   ├── composables/
│   │   └── useCountUp.ts
│   └── styles/
│       ├── global.scss
│       ├── mixins.scss
│       └── tokens.scss
├── vite.config.ts
├── package.json
└── README.md
```

## 样式与主题

样式系统主要分为三层：

- `src/styles/tokens.scss`：定义颜色、圆角、间距、动效、字体与 Element Plus 变量映射
- `src/styles/mixins.scss`：沉淀可复用的面板、滚动条、悬停等样式 mixin
- `src/styles/global.scss`：全局 reset、页面背景、渐变文本、reveal 动画等基础样式

主题默认是 `dark`，并通过 `Pinia` 中的 `app` store 负责：

- 读取本地 `theme`
- 切换 `light` / `dark`
- 同步 `document.documentElement[data-theme]`

## 路由与认证说明

- 页面标题在路由守卫中动态设置
- 开发环境会跳过认证检查
- 开发环境启动时会自动写入一个模拟 `token` 和 `user`
- 生产环境下，访问需要认证的页面时会检查 `localStorage` 中的 `token`

这意味着本地联调时几乎可以直接进入工作台页面，无需额外登录流程。

## 构建与部署说明

- 构建输出目录为 `dist/`
- 生产环境 `base` 会切换为 `/agent-learning-platform/`
- 已配置基础的 `manualChunks`，将 `vue`、`element-plus` 和 `utils` 相关依赖拆分输出
- 构建默认生成 `sourcemap`

如果部署到 GitHub Pages，当前 `vite.config.ts` 已包含对应的基础路径处理。

## 开发建议

- 优先在 `views/` 组织页面层结构，在 `components/dashboard/` 和 `components/learning/` 中承载模块化 UI
- 全局主题相关改动优先从 `tokens.scss` 入手，避免直接写死颜色
- 如果新增学习地图能力，优先沿用现有 “地图画布 + 节点详情 + 阶段面板 + 资料面板” 的工作区拆分方式
- `dist/` 和构建产物属于生成文件，不建议手动修改

## 仓库信息

- Repository: [MenFsq/agent-learning-platform](https://github.com/MenFsq/agent-learning-platform)
- Homepage: [https://menfsq.github.io/agent-learning-platform/](https://menfsq.github.io/agent-learning-platform/)

---

最后更新：`2026-04-14`