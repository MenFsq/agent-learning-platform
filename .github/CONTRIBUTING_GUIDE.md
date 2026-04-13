# 贡献者指南 - 详细版

## 🎯 欢迎贡献！

感谢你对 Agent Learning Platform 项目的关注！本指南将帮助你了解如何参与项目贡献。

## 📋 贡献流程

### 1. 准备工作
- Fork 项目仓库到你的 GitHub 账户
- 克隆到本地：`git clone https://github.com/你的用户名/agent-learning-platform.git`
- 添加上游仓库：`git remote add upstream https://github.com/MenFsq/agent-learning-platform.git`

### 2. 创建分支
```bash
# 从最新的 master 分支创建新分支
git checkout master
git pull upstream master
git checkout -b 分支类型/简短描述

# 分支命名规范：
# feature/xxx    - 新功能开发
# fix/xxx        - Bug修复
# docs/xxx       - 文档更新
# refactor/xxx   - 代码重构
# test/xxx       - 测试相关
```

### 3. 开发规范

#### 代码规范
- 前端代码遵循 Vue 3 + TypeScript 最佳实践
- 后端代码遵循 PEP 8 Python 代码规范
- 提交前运行代码格式化工具

#### 提交信息规范
使用约定式提交格式：
```
类型(范围): 描述

详细说明（可选）

关闭 #Issue编号
```

**类型说明：**
- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具变动

**示例：**
```
feat(frontend): 添加用户登录界面

- 实现用户登录表单组件
- 添加表单验证逻辑
- 集成API调用

关闭 #123
```

### 4. 提交 Pull Request

#### PR 检查清单
- [ ] 代码通过所有测试
- [ ] 更新了相关文档
- [ ] 提交信息符合规范
- [ ] 分支名称符合规范
- [ ] 没有引入新的警告

#### PR 描述模板
请使用提供的 PR 模板，确保包含：
- 清晰的描述
- 相关 Issue 链接
- 测试步骤
- 影响范围分析

### 5. 代码审查流程

#### 审查标准
1. **代码质量**
   - 代码清晰易读
   - 遵循项目规范
   - 有适当的注释

2. **功能完整性**
   - 实现需求的所有功能
   - 处理了边界情况
   - 有相应的测试

3. **文档更新**
   - 更新了相关文档
   - 添加了使用示例
   - 说明了变更影响

#### 审查反馈
- 审查者会在 3 个工作日内提供反馈
- 可能需要多次修改才能合并
- 请及时响应审查意见

## 🏆 贡献者等级

### 初学者
- 完成第一个成功的 PR
- 熟悉项目开发流程
- 能够修复简单的 bug

### 贡献者
- 提交过 3 个以上 PR
- 能够独立开发小功能
- 参与过代码审查

### 核心贡献者
- 提交过 10 个以上 PR
- 负责特定模块的开发
- 有代码合并权限
- 参与项目决策

### 维护者
- 长期活跃贡献者
- 深度理解项目架构
- 有发布版本权限
- 领导项目发展方向

## 🛠️ 开发环境设置

### 前端开发
```bash
cd frontend
npm install
npm run dev  # 开发服务器
npm run build  # 生产构建
npm run test  # 运行测试
```

### 后端开发
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn src.main:app --reload  # 开发服务器
pytest  # 运行测试
```

## 📚 学习资源

### 技术栈学习
- [Vue 3 官方文档](https://vuejs.org/)
- [TypeScript 手册](https://www.typescriptlang.org/docs/)
- [FastAPI 文档](https://fastapi.tiangolo.com/)
- [LangChain 指南](https://python.langchain.com/docs/)

### 项目相关
- [项目架构文档](../ARCHITECTURE.md)
- [API 设计规范](./API_DESIGN.md)
- [部署指南](./DEPLOYMENT.md)

## 🐛 报告问题

### Bug 报告
1. 在 Issues 中搜索是否已有类似问题
2. 使用 Bug 报告模板
3. 提供详细的重现步骤
4. 包含环境信息和错误日志

### 功能请求
1. 描述清楚需求背景
2. 说明期望的功能
3. 提供使用场景
4. 评估优先级

## 🤝 社区交流

### 沟通渠道
- **GitHub Issues**: 技术讨论和问题反馈
- **GitHub Discussions**: 功能讨论和设计决策
- **Pull Requests**: 代码审查和合并

### 行为准则
- 尊重他人的意见和贡献
- 建设性讨论，避免人身攻击
- 保持专业和技术导向
- 帮助新贡献者融入社区

## 📅 发布周期

### 版本规划
- **主版本 (v1.0, v2.0)**: 重大架构变更
- **次版本 (v1.1, v1.2)**: 新功能发布
- **修订版本 (v1.0.1, v1.0.2)**: Bug修复

### 发布流程
1. 功能冻结
2. 测试和修复
3. 文档更新
4. 版本发布
5. 发布公告

## 🎉 致谢

感谢所有贡献者的付出！你的每一行代码、每一个建议都在让这个项目变得更好。

让我们共同打造优秀的 AI Agent 学习平台！🚀