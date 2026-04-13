# 贡献指南

感谢你考虑为 Agent Learning Platform 做出贡献！

## 🎯 如何贡献

### 1. 报告Bug
- 使用 [GitHub Issues](https://github.com/your-username/agent-learning-platform/issues) 报告bug
- 确保bug尚未被报告
- 提供详细的bug描述和重现步骤

### 2. 请求新功能
- 使用 [GitHub Issues](https://github.com/your-username/agent-learning-platform/issues) 请求新功能
- 描述功能的使用场景和预期行为
- 如果可能，提供设计思路或原型

### 3. 提交代码
1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 📝 开发规范

### 代码风格
- **前端**: 遵循 ESLint 和 Prettier 配置
- **后端**: 使用 Black 进行代码格式化
- **提交信息**: 使用 Conventional Commits 规范

### 测试要求
- 新功能必须包含单元测试
- Bug修复必须包含回归测试
- 确保所有测试通过后再提交PR

### 文档要求
- 新功能必须更新相关文档
- API变更必须更新API文档
- 复杂功能需要添加使用示例

## 🚀 开发流程

### 1. 设置开发环境
```bash
# 克隆项目
git clone https://github.com/your-username/agent-learning-platform.git
cd agent-learning-platform

# 安装依赖
make install

# 启动开发环境
make dev
```

### 2. 创建功能分支
```bash
git checkout -b feature/your-feature-name
```

### 3. 开发功能
- 编写代码
- 添加测试
- 更新文档

### 4. 提交更改
```bash
git add .
git commit -m "feat(scope): description of changes"
```

### 5. 创建Pull Request
- 确保代码通过所有检查
- 添加详细的PR描述
- 等待代码审查

## 📊 项目结构

详细的项目结构请查看 [PROJECT-STRUCTURE.md](PROJECT-STRUCTURE.md)。

## ❓ 常见问题

### Q: 如何运行测试？
A: 使用 `make test` 命令运行所有测试。

### Q: 如何格式化代码？
A: 使用 `make format` 命令格式化代码。

### Q: 如何部署到生产环境？
A: 查看 [部署指南](docs/deployment-guide.md)。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---
*最后更新: 2026-04-13*