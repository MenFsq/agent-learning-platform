# Agent Learning Platform - 前端项目

## 🎯 项目概述

这是 Agent Learning Platform 的前端项目，基于 Vue 3 + TypeScript + Vite 构建的现代化 Web 应用。

## 🚀 快速开始

### 环境要求
- Node.js 18+ 
- npm 9+ 或 yarn 1.22+ 或 pnpm 8+

### 安装依赖
```bash
npm install
# 或
yarn install
# 或
pnpm install
```

### 启动开发服务器
```bash
npm run dev
# 或
yarn dev
# 或
pnpm dev
```

### 构建生产版本
```bash
npm run build
# 或
yarn build
# 或
pnpm build
```

### 预览生产版本
```bash
npm run preview
# 或
yarn preview
# 或
pnpm preview
```

## 📁 项目结构

```
frontend/
├── 📁 src/                    # 源代码目录
│   ├── 📁 assets/            # 静态资源
│   │   ├── 📁 images/        # 图片资源
│   │   ├── 📁 styles/        # 样式文件
│   │   └── 📁 fonts/         # 字体文件
│   ├── 📁 components/        # 公共组件
│   │   ├── 📁 common/        # 通用组件
│   │   ├── 📁 layout/        # 布局组件
│   │   └── 📁 ui/            # UI组件
│   ├── 📁 views/             # 页面组件
│   │   ├── Home.vue          # 首页
│   │   ├── Dashboard.vue     # 仪表板
│   │   ├── Learning.vue      # 学习页面
│   │   ├── Projects.vue      # 项目页面
│   │   └── Community.vue     # 社区页面
│   ├── 📁 composables/       # 组合式函数
│   │   ├── useApi.ts         # API调用
│   │   ├── useAuth.ts        # 认证逻辑
│   │   ├── useProjects.ts    # 项目管理
│   │   └── useLearning.ts    # 学习管理
│   ├── 📁 stores/            # Pinia状态管理
│   │   ├── auth.ts           # 认证状态
│   │   ├── projects.ts       # 项目状态
│   │   ├── learning.ts       # 学习状态
│   │   └── ui.ts             # UI状态
│   ├── 📁 types/             # TypeScript类型定义
│   │   ├── api.ts            # API类型
│   │   ├── project.ts        # 项目类型
│   │   ├── user.ts           # 用户类型
│   │   └── learning.ts       # 学习类型
│   ├── 📁 utils/             # 工具函数
│   │   ├── api.ts            # API工具
│   │   ├── validation.ts     # 数据验证
│   │   ├── formatter.ts      # 数据格式化
│   │   └── constants.ts      # 常量定义
│   ├── 📁 router/            # 路由配置
│   │   └── index.ts          # 路由定义
│   ├── App.vue               # 根组件
│   └── main.ts               # 应用入口
├── index.html                # HTML模板
├── package.json              # 项目配置
├── vite.config.ts            # Vite配置
├── tsconfig.json             # TypeScript配置
├── .env                      # 环境变量
├── .env.development          # 开发环境变量
├── .env.production           # 生产环境变量
└── README.md                 # 项目文档
```

## 🔧 技术栈

### 核心框架
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全的 JavaScript 超集
- **Vite** - 下一代前端构建工具

### 状态管理
- **Pinia** - Vue 官方推荐的状态管理库

### UI框架
- **Element Plus** - 基于 Vue 3 的组件库
- **Vue Router** - 官方路由管理器

### 开发工具
- **ESLint** - 代码检查
- **Prettier** - 代码格式化
- **Husky** - Git hooks
- **Commitlint** - Commit 消息规范

### 测试工具
- **Vitest** - 单元测试框架
- **Vue Test Utils** - Vue 组件测试工具
- **Cypress** - E2E 测试框架

## 🌐 API集成

### 配置
在 `.env` 文件中配置后端 API 地址：
```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TIMEOUT=30000
```

### API调用示例
```typescript
import { api } from '@/utils/api'

// 获取项目列表
const projects = await api.get('/projects')

// 创建项目
const newProject = await api.post('/projects', {
  name: '新项目',
  description: '项目描述'
})

// 更新项目
const updatedProject = await api.put(`/projects/${id}`, {
  name: '更新后的项目名'
})

// 删除项目
await api.delete(`/projects/${id}`)
```

## 🎨 样式方案

### CSS预处理器
- **Sass/SCSS** - CSS 预处理器

### 设计系统
- **CSS Variables** - 自定义属性
- **BEM命名规范** - 组件样式命名
- **响应式设计** - 移动端优先

### 主题系统
支持亮色/暗色主题切换，通过 CSS 变量实现。

## 📱 响应式设计

### 断点定义
```scss
$breakpoints: (
  'xs': 0,
  'sm': 576px,
  'md': 768px,
  'lg': 992px,
  'xl': 1200px,
  'xxl': 1400px
);
```

### 移动端优化
- 触摸友好的交互
- 移动端导航菜单
- 图片懒加载
- 性能优化

## 🔐 安全考虑

### 认证授权
- JWT Token 存储
- 路由守卫
- 权限控制

### 数据安全
- XSS 防护
- CSRF 防护
- 输入验证

### 代码安全
- 依赖安全扫描
- 代码审查
- 安全最佳实践

## 🚀 性能优化

### 构建优化
- 代码分割
- 懒加载路由
- 图片压缩
- Tree Shaking

### 运行时优化
- 虚拟滚动
- 防抖节流
- 缓存策略
- 预加载

### 监控分析
- 性能监控
- 错误追踪
- 用户行为分析

## 📊 开发规范

### 代码规范
- ESLint + Prettier 统一代码风格
- TypeScript 严格模式
- 组件命名规范

### Git规范
- Conventional Commits
- 分支管理策略
- Code Review 流程

### 测试规范
- 单元测试覆盖率 > 80%
- E2E 测试关键路径
- 集成测试 API

## 🐳 部署

### 构建命令
```bash
# 开发环境
npm run build:dev

# 生产环境
npm run build:prod

# 预览
npm run preview
```

### Docker部署
```dockerfile
# Dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 发起 Pull Request
5. 等待 Code Review

## 📞 支持与反馈

- 问题反馈: GitHub Issues
- 功能建议: GitHub Discussions
- 文档改进: Pull Request

---

**最后更新**: 2026-04-13  
**维护者**: 小老虎 🐯