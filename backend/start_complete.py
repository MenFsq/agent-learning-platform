"""
完整的后端启动脚本
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# 创建FastAPI应用
app = FastAPI(
    title="Agent Learning Platform (完整版)",
    version="1.0.0",
    description="完整版后端API，包含用户认证和项目管理"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5175", "http://localhost:5176", "http://localhost:5177"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str]
    created_at: datetime

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    owner_id: int
    is_public: bool
    created_at: datetime
    updated_at: datetime

# 模拟数据库
users_db = []
projects_db = []
current_user_id = 1
current_project_id = 1

# 根端点
@app.get("/")
async def root():
    return {
        "message": "Agent Learning Platform 完整后端API",
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
        "service": "agent-platform-backend-complete",
        "version": "1.0.0",
        "database": "simulated",
        "timestamp": datetime.utcnow().isoformat()
    }

# 用户注册
@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    global current_user_id
    
    # 检查用户是否已存在
    for u in users_db:
        if u["username"] == user.username or u["email"] == user.email:
            return {"error": "User already exists"}
    
    # 创建新用户
    new_user = {
        "id": current_user_id,
        "username": user.username,
        "email": user.email,
        "password": user.password,  # 注意：实际应用中应该哈希密码
        "full_name": user.full_name,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    users_db.append(new_user)
    current_user_id += 1
    
    return new_user

# 用户登录
@app.post("/api/v1/auth/login")
async def login(credentials: UserLogin):
    # 查找用户
    for user in users_db:
        if user["username"] == credentials.username and user["password"] == credentials.password:
            # 生成模拟令牌
            return {
                "access_token": f"mock_token_{user['id']}_{datetime.utcnow().timestamp()}",
                "refresh_token": f"mock_refresh_{user['id']}_{datetime.utcnow().timestamp()}",
                "token_type": "bearer",
                "user": {
                    "id": user["id"],
                    "username": user["username"],
                    "email": user["email"],
                    "full_name": user["full_name"]
                }
            }
    
    return {"error": "Invalid credentials"}

# 获取当前用户
@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_current_user(token: str = "mock_token"):
    # 模拟令牌验证
    if not token.startswith("mock_token"):
        return {"error": "Invalid token"}
    
    # 从令牌中提取用户ID
    try:
        user_id = int(token.split("_")[2])
    except:
        return {"error": "Invalid token"}
    
    # 查找用户
    for user in users_db:
        if user["id"] == user_id:
            return user
    
    return {"error": "User not found"}

# 创建项目
@app.post("/api/v1/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, token: str = "mock_token"):
    global current_project_id
    
    # 验证令牌
    if not token.startswith("mock_token"):
        return {"error": "Invalid token"}
    
    try:
        owner_id = int(token.split("_")[2])
    except:
        return {"error": "Invalid token"}
    
    # 创建项目
    new_project = {
        "id": current_project_id,
        "name": project.name,
        "description": project.description,
        "owner_id": owner_id,
        "is_public": project.is_public,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    projects_db.append(new_project)
    current_project_id += 1
    
    return new_project

# 获取用户项目
@app.get("/api/v1/projects/my", response_model=List[ProjectResponse])
async def get_my_projects(token: str = "mock_token"):
    # 验证令牌
    if not token.startswith("mock_token"):
        return []
    
    try:
        user_id = int(token.split("_")[2])
    except:
        return []
    
    # 获取用户项目
    user_projects = [p for p in projects_db if p["owner_id"] == user_id]
    return user_projects

# 获取所有公开项目
@app.get("/api/v1/projects/public", response_model=List[ProjectResponse])
async def get_public_projects():
    public_projects = [p for p in projects_db if p["is_public"]]
    return public_projects

# 获取项目详情
@app.get("/api/v1/projects/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    for project in projects_db:
        if project["id"] == project_id:
            return project
    
    return {"error": "Project not found"}

# 系统信息
@app.get("/api/v1/system/info")
async def system_info():
    return {
        "users_count": len(users_db),
        "projects_count": len(projects_db),
        "public_projects_count": len([p for p in projects_db if p["is_public"]]),
        "active_since": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    print("启动完整版后端服务器...")
    print("API文档: http://localhost:8003/docs")
    print("健康检查: http://localhost:8003/health")
    print("前端地址: http://localhost:5174")
    print("测试用户: testuser / testpass")
    
    uvicorn.run(
        "start_complete:app",
        host="0.0.0.0",
        port=8003,
        reload=True
    )