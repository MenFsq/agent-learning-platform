# Agent Learning Platform 快速启动指南

> 生成时间: 2026-04-15 00:10
> 系统状态: ✅ 运行正常

## 🚀 立即访问

### 1. 前端应用
- **地址**: http://localhost:5175
- **技术栈**: Vue 3 + TypeScript + Element Plus
- **状态**: ✅ 运行中 (200 OK)

### 2. 后端API服务
- **地址**: http://localhost:8001
- **技术栈**: FastAPI + Uvicorn
- **状态**: ✅ 运行中

### 3. API文档
- **Swagger UI**: http://localhost:8001/docs
- **状态**: ✅ 可访问

## 📋 已验证功能

### 前端功能
- ✅ 应用首页可访问
- ✅ Vite开发服务器运行正常
- ✅ 热重载功能启用

### 后端API端点
- ✅ `GET /` - 根端点 (系统信息)
- ✅ `GET /health` - 健康检查
- ✅ `POST /api/v1/auth/test` - 认证测试
- ✅ `GET /api/v1/projects` - 项目列表

### 开发环境
- ✅ Node.js v24.14.0
- ✅ npm 11.9.0
- ✅ Python 3.14.4
- ✅ 虚拟环境配置完成

## 🔧 快速测试命令

### 测试前端
```bash
# 检查前端状态
curl http://localhost:5175

# 或使用浏览器直接访问
# http://localhost:5175
```

### 测试后端API
```bash
# 系统信息
curl http://localhost:8001/

# 健康检查
curl http://localhost:8001/health

# 认证测试
curl -X POST http://localhost:8001/api/v1/auth/test

# 获取项目列表
curl http://localhost:8001/api/v1/projects
```

### PowerShell测试
```powershell
# 测试所有端点
$endpoints = @("/", "/health", "/api/v1/auth/test", "/api/v1/projects")
foreach ($endpoint in $endpoints) {
    $url = "http://localhost:8001$endpoint"
    $method = if ($endpoint -eq "/api/v1/auth/test") { "POST" } else { "GET" }
    try {
        $response = Invoke-WebRequest -Uri $url -Method $method -UseBasicParsing
        Write-Host "$endpoint : $($response.StatusCode) OK"
    } catch {
        Write-Host "$endpoint : ERROR"
    }
}
```

## 🎯 立即可以做的事

### 1. 探索前端界面
打开浏览器访问 http://localhost:5175，查看：
- 现代化登录页面
- 应用仪表板
- 响应式设计

### 2. 查看API文档
访问 http://localhost:8001/docs，了解：
- 所有可用API端点
- 请求/响应格式
- 在线测试功能

### 3. 测试API调用
使用以下工具测试API：
- **Postman**: 导入OpenAPI规范
- **curl**: 命令行测试
- **浏览器**: 直接访问端点

### 4. 开始开发
#### 前端开发
```bash
cd frontend
npm run dev          # 启动开发服务器
npm run build        # 构建生产版本
npm run lint         # 代码检查
```

#### 后端开发
```bash
cd backend
# 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 启动开发服务器
python start-simple.py

# 或使用完整后端
python src/main.py
```

## 📁 项目结构

```
agent-learning-platform/
├── frontend/                 # Vue 3前端
│   ├── src/views/           # 页面组件
│   │   ├── Login.vue        # 登录页面
│   │   ├── Dashboard.vue    # 仪表板
│   │   └── Learning.vue     # 学习页面
│   ├── package.json         # 前端依赖
│   └── vite.config.ts       # 构建配置
├── backend/                  # FastAPI后端
│   ├── src/                 # 源代码
│   │   ├── main.py          # 应用入口
│   │   ├── core/            # 核心模块
│   │   ├── api/v1/          # API路由
│   │   └── middleware/      # 中间件
│   ├── start-simple.py      # 简化启动脚本
│   ├── requirements.txt     # Python依赖
│   └── .env                 # 环境配置
├── docs/                    # 文档
│   └── technical-share-01.md # 技术分享
└── QUICK-START.md          # 本指南
```

## 🔄 开发工作流

### 1. 启动开发环境
```bash
# 终端1: 启动前端
cd frontend
npm run dev

# 终端2: 启动后端
cd backend
.\venv\Scripts\Activate.ps1
python start-simple.py
```

### 2. 代码修改和测试
- 修改前端代码 → 自动热重载
- 修改后端代码 → 自动重启
- 测试API端点 → 使用API文档

### 3. 构建和部署
```bash
# 构建前端
cd frontend
npm run build

# 部署后端
cd backend
# 使用Docker或直接部署
```

## ⚠️ 故障排除

### 前端无法访问
1. 检查端口是否被占用
2. 检查Node.js和npm是否安装
3. 查看控制台错误信息

### 后端无法启动
1. 检查Python虚拟环境
2. 检查依赖是否安装
3. 检查端口冲突

### API调用失败
1. 检查后端是否运行
2. 检查CORS配置
3. 查看服务器日志

## 📞 技术支持

### 日志查看
```bash
# 前端日志 (浏览器控制台)
F12 打开开发者工具

# 后端日志
查看控制台输出
```

### 问题报告
1. 描述问题现象
2. 提供错误信息
3. 说明复现步骤

## 🎉 恭喜！

你的 Agent Learning Platform 已经成功启动并运行。现在可以：

1. **立即体验**: 访问前端应用和API文档
2. **开始开发**: 基于现有架构添加新功能
3. **学习探索**: 研究技术实现细节
4. **分享交流**: 在BotLearn社区分享经验

祝开发愉快！ 🚀

---
**最后更新**: 2026-04-15  
**维护者**: 小老虎 🐯  
**项目状态**: ✅ 运行正常