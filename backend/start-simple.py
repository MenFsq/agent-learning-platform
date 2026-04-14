"""
简化的后端启动脚本 - 用于快速测试
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 创建FastAPI应用
app = FastAPI(
    title="Agent Learning Platform (简化版)",
    version="1.0.0",
    description="简化版后端API，用于快速测试"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5175", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 根端点
@app.get("/")
async def root():
    return {
        "message": "Agent Learning Platform 后端API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

# 健康检查端点
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "agent-platform-backend",
        "version": "1.0.0"
    }

# 测试认证端点
@app.post("/api/v1/auth/test")
async def test_auth():
    return {
        "success": True,
        "message": "认证API测试成功",
        "data": {
            "user_id": "test_user_123",
            "username": "testuser",
            "token": "test_jwt_token_123456"
        }
    }

# 测试项目端点
@app.get("/api/v1/projects")
async def get_projects():
    return {
        "success": True,
        "data": [
            {
                "id": "project_1",
                "name": "Vue 3学习项目",
                "description": "学习Vue 3和TypeScript",
                "status": "active",
                "created_at": "2026-04-14T10:00:00Z"
            },
            {
                "id": "project_2",
                "name": "AI Agent集成",
                "description": "集成LangChain和OpenClaw",
                "status": "active",
                "created_at": "2026-04-14T11:00:00Z"
            }
        ]
    }

if __name__ == "__main__":
    print("启动简化版后端服务器...")
    print("API文档: http://localhost:8002/docs")
    print("健康检查: http://localhost:8002/health")
    print("前端地址: http://localhost:5174")
    
    uvicorn.run(
        "start-simple:app",
        host="0.0.0.0",
        port=8002,
        reload=True
    )