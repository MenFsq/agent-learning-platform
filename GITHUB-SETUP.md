# GitHub 设置指南

## 🚀 快速开始

### 步骤1: 在GitHub上创建仓库
1. 登录到 [GitHub](https://github.com)
2. 点击右上角的 "+" 图标，选择 "New repository"
3. 填写仓库信息:
   - **Repository name**: `agent-learning-platform`
   - **Description**: `A complete learning platform for AI Agent development based on LangChain + OpenClaw + Vue 3`
   - **Visibility**: Public (推荐) 或 Private
   - **Initialize with README**: ❌ 不要勾选 (我们已经有README.md)
   - **Add .gitignore**: 选择 "Node" 或 "Python"
   - **Add a license**: 选择 "MIT License"
4. 点击 "Create repository"

### 步骤2: 获取仓库URL
创建仓库后，你会看到类似这样的URL:
```
https://github.com/你的用户名/agent-learning-platform.git
```

### 步骤3: 使用推送脚本
```powershell
# 进入项目目录
cd agent-learning-platform

# 运行推送脚本
.\push-to-github.ps1
```

按照脚本提示输入你的GitHub仓库URL。

## 🔧 手动推送方法

如果你更喜欢手动操作:

### 1. 添加远程仓库
```bash
git remote add origin https://github.com/你的用户名/agent-learning-platform.git
```

### 2. 推送代码
```bash
git push -u origin master
```

### 3. 验证推送
```bash
git remote -v
git branch -vv
```

## 📁 项目文件结构

推送后，GitHub仓库将包含以下核心文件:

```
agent-learning-platform/
├── 📄 README.md                    # 项目说明文档
├── 📄 CONTRIBUTING.md              # 贡献指南
├── 📄 PROJECT-STRUCTURE.md         # 详细项目结构
├── 📄 GITHUB-SETUP.md              # GitHub设置指南 (本文件)
├── 📄 push-to-github.ps1           # GitHub推送脚本
├── 📁 scripts/                     # 自动化脚本
│   └── setup-project.sh           # 项目设置脚本
└── 📁 web-ui/                      # 前端界面
    └── 📁 dashboard/               # 仪表板界面
        └── index.html             # 交互式仪表板
```

## 🎯 推送后的操作

### 1. 设置GitHub Pages (可选)
如果你想展示项目仪表板:
1. 进入仓库的 "Settings" 页面
2. 选择 "Pages" 选项
3. 设置 Source 为 "master branch" 或 "gh-pages branch"
4. 保存后访问: `https://你的用户名.github.io/agent-learning-platform/web-ui/dashboard/`

### 2. 配置GitHub Actions
项目已包含 `.github/workflows/ci.yml` 配置，自动启用:
- 代码检查 (linting)
- 测试运行
- Docker镜像构建
- 自动部署

### 3. 邀请贡献者
1. 进入仓库的 "Settings" 页面
2. 选择 "Collaborators" 选项
3. 添加其他开发者的GitHub用户名
4. 设置适当的权限级别

### 4. 创建Issue模板
项目已包含:
- `.github/ISSUE_TEMPLATE/bug_report.md`
- `.github/ISSUE_TEMPLATE/feature_request.md`

## 🔒 安全注意事项

### 敏感信息保护
确保以下文件**不**推送到GitHub:
- `.env` 或 `.env.*` 文件 (包含API密钥)
- `credentials.json` 文件
- 任何包含密码、密钥、令牌的文件

### 使用.gitignore
项目已配置 `.gitignore` 文件，自动排除:
- 依赖目录 (`node_modules/`, `venv/`)
- 构建产物 (`dist/`, `build/`)
- 日志文件 (`logs/`)
- 环境配置文件 (`.env`)

## 🌟 最佳实践

### 提交信息规范
使用 Conventional Commits 格式:
```
feat: 添加新功能
fix: 修复bug
docs: 更新文档
style: 代码格式调整
refactor: 代码重构
test: 添加测试
chore: 构建过程或辅助工具变动
```

### 分支策略
- `master`: 稳定版本分支
- `develop`: 开发分支
- `feature/*`: 功能开发分支
- `bugfix/*`: bug修复分支
- `release/*`: 发布分支

### 代码审查
- 所有更改通过Pull Request进行
- 至少需要一名审查者批准
- 通过所有CI检查后才能合并

## ❓ 常见问题

### Q: 推送时出现权限错误?
A: 确保:
1. GitHub仓库URL正确
2. 你有推送权限
3. 已正确配置SSH密钥或使用HTTPS凭据

### Q: 如何更新已存在的仓库?
A: 使用:
```bash
git pull origin master  # 拉取最新更改
git push origin master  # 推送本地更改
```

### Q: 如何回滚错误的提交?
A: 使用:
```bash
git revert <commit-hash>  # 创建撤销提交
git push origin master    # 推送撤销
```

### Q: 如何添加更多文件?
A: 使用:
```bash
git add <file-name>      # 添加文件
git commit -m "message"  # 提交更改
git push origin master   # 推送到GitHub
```

## 📞 获取帮助

如果遇到问题:
1. 查看 [GitHub文档](https://docs.github.com)
2. 检查错误信息中的提示
3. 搜索相关错误解决方案
4. 在项目Issue中提问

---
*最后更新: 2026-04-13 | 维护者: 小老虎 🐯*