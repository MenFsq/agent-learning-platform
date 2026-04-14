# API文档访问指南

> 生成时间: 2026-04-15 00:50
> 状态: ✅ 完全可用

## 🎯 访问方式

### 1. 直接访问后端API文档
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc
- **健康检查**: http://localhost:8001/health
- **应用信息**: http://localhost:8001/info

### 2. 通过前端Dashboard访问
1. 打开前端应用: http://localhost:5176
2. 在Dashboard的"快速入口"区域，点击"API 文档"
3. 或在"社区动态"区域，点击"API 文档"条目

### 3. 命令行测试
```bash
# 测试API根端点
curl http://localhost:8001/

# 健康检查
curl http://localhost:8001/health

# 获取项目列表
curl http://localhost:8001/api/v1/projects

# 测试认证API
curl -X POST http://localhost:8001/api/v1/auth/test
```

## 📊 可用功能

### Swagger UI (推荐)
- **地址**: http://localhost:8001/docs
- **功能**:
  - 交互式API文档
  - 在线API测试
  - 自动生成请求代码
  - 参数验证和提示

### ReDoc
- **地址**: http://localhost:8001/redoc
- **功能**:
  - 美观的文档展示
  - 响应式设计
  - 离线阅读支持
  - 更好的可读性

## 🔧 API端点列表

### 系统端点
- `GET /` - 系统信息
- `GET /health` - 健康检查
- `GET /info` - 应用信息
- `GET /docs` - Swagger UI
- `GET /redoc` - ReDoc

### 认证端点
- `POST /api/v1/auth/test` - 认证测试

### 项目端点
- `GET /api/v1/projects` - 获取项目列表

## 🚀 快速开始

### 1. 验证后端服务
```bash
# 检查后端是否运行
curl http://localhost:8001/health

# 预期响应
{
  "status": "healthy",
  "service": "agent-platform-backend",
  "version": "1.0.0"
}
```

### 2. 测试API端点
```bash
# 获取系统信息
curl http://localhost:8001/

# 测试认证
curl -X POST http://localhost:8001/api/v1/auth/test

# 获取项目列表
curl http://localhost:8001/api/v1/projects
```

### 3. 使用Swagger UI
1. 打开 http://localhost:8001/docs
2. 浏览API端点
3. 点击"Try it out"测试API
4. 查看请求和响应

## 📱 前端集成

### Dashboard快速入口
- **位置**: Dashboard页面的"快速入口"区域
- **名称**: API 文档
- **描述**: 查看后端API文档和测试接口
- **链接**: 直接打开Swagger UI

### 社区动态提醒
- **位置**: Dashboard页面的"社区动态"区域
- **标题**: API 文档
- **详情**: 后端API文档已就绪，支持在线测试
- **链接**: 直接打开Swagger UI

## 🔍 功能特性

### 交互式文档
- 实时API测试
- 参数自动补全
- 请求示例生成
- 响应格式预览

### 开发者工具
- 多种语言代码生成
- cURL命令复制
- 请求历史记录
- 错误诊断信息

### 用户体验
- 响应式设计
- 深色/浅色主题
- 键盘快捷键
- 离线支持

## ⚠️ 注意事项

### 开发环境
- **后端端口**: 8001
- **前端端口**: 5176
- **API地址**: http://localhost:8001
- **文档地址**: http://localhost:8001/docs

### 生产环境
- 需要配置正确的域名和HTTPS
- 考虑API文档的访问权限
- 监控API使用情况

### 安全考虑
- 开发环境文档公开访问
- 生产环境可能需要认证
- 敏感API端点需要保护
- 请求频率限制

## 🔄 维护指南

### 更新API文档
1. 修改后端代码注释
2. FastAPI自动更新文档
3. 重启后端服务
4. 刷新浏览器查看更新

### 添加新端点
1. 在FastAPI中定义新路由
2. 添加详细的文档字符串
3. 指定请求/响应模型
4. 测试端点功能

### 故障排除
```bash
# 检查端口占用
netstat -ano | findstr :8001

# 检查服务日志
# 查看后端控制台输出

# 验证网络连接
ping localhost
```

## 🎯 最佳实践

### 文档编写
- 为每个端点添加详细描述
- 说明参数类型和约束
- 提供请求/响应示例
- 标注认证要求和权限

### 测试策略
- 使用Swagger UI进行手动测试
- 编写自动化API测试
- 监控API性能和可用性
- 定期更新测试用例

### 版本管理
- 使用API版本控制
- 维护变更日志
- 提供向后兼容性
- 计划废弃旧版本

## 📈 扩展计划

### 短期改进
1. 完善API端点文档
2. 添加更多示例代码
3. 优化响应格式
4. 增强错误处理

### 中期计划
1. 实现完整的认证系统
2. 添加项目管理功能
3. 集成学习系统API
4. 实现社区功能API

### 长期愿景
1. 完整的API生态系统
2. 第三方集成支持
3. API监控和分析
4. 开发者门户网站

## 📞 技术支持

### 常见问题
1. **API无法访问**: 检查后端服务状态
2. **文档不显示**: 检查FastAPI配置
3. **测试失败**: 查看请求参数和格式
4. **性能问题**: 监控服务器资源

### 调试工具
- 浏览器开发者工具
- 后端服务日志
- 网络请求监控
- API测试工具

### 联系支持
- 查看项目文档
- 检查GitHub Issues
- 参与社区讨论
- 提交问题报告

---

**文档版本**: 1.0.0  
**最后更新**: 2026-04-15  
**维护者**: 小老虎 🐯  
**项目**: Agent Learning Platform  
**状态**: ✅ API文档完全可用  
**访问地址**: http://localhost:8001/docs