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
    allow_origins=["http://localhost:5174", "http://localhost:5175", "http://localhost:5176", "http://localhost:5177", "http://localhost:5178", "http://localhost:5179"],
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

class AgentConfig(BaseModel):
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 2000
    memory: bool = False
    tools: List[str] = []

class AgentCreate(BaseModel):
    name: str
    description: str
    type: str
    config: Optional[AgentConfig] = None

class AgentResponse(BaseModel):
    id: int
    name: str
    description: str
    type: str
    status: str
    config: Optional[dict]
    owner_id: int
    project_id: Optional[int]
    created_at: datetime
    updated_at: datetime

# 模拟数据库
users_db = []
projects_db = []
agents_db = []
current_user_id = 1
current_project_id = 1
current_agent_id = 1

# 初始化示例数据的函数
def init_sample_data():
    global current_user_id, current_project_id, current_agent_id
    
    if not users_db:
        users_db.append({
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass",
            "full_name": "测试用户",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        current_user_id = 2
    
    if not projects_db:
        projects_db.append({
            "id": 1,
            "name": "示例项目",
            "description": "这是一个示例项目",
            "owner_id": 1,
            "is_public": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        current_project_id = 2
    
    if not agents_db:
        agents_db.append({
            "id": 1,
            "name": "客服助手",
            "description": "用于处理客户咨询的AI助手",
            "type": "customer_service",
            "status": "running",
            "config": {
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 2000,
                "memory": True,
                "tools": ["search", "calculator"]
            },
            "owner_id": 1,
            "project_id": 1,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
        
        agents_db.append({
            "id": 2,
            "name": "代码审查助手",
            "description": "帮助审查代码质量的AI助手",
            "type": "code_review",
            "status": "stopped",
            "config": {
                "model": "gpt-4",
                "temperature": 0.3,
                "max_tokens": 4000,
                "memory": True,
                "tools": ["code_analysis", "security_check"]
            },
            "owner_id": 1,
            "project_id": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "run_count": 89,
            "uptime": "1天5小时",
            "memory_usage": "2.4GB"
        })
        
        # 添加第三个Agent
        agents_db.append({
            "id": 3,
            "name": "数据分析助手",
            "description": "用于数据分析和可视化的AI助手",
            "type": "data_analysis",
            "status": "running",
            "config": {
                "model": "claude-3-opus",
                "temperature": 0.5,
                "max_tokens": 8000,
                "memory": True,
                "tools": ["data_processing", "visualization", "statistics"]
            },
            "owner_id": 1,
            "project_id": 1,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "run_count": 42,
            "uptime": "12小时",
            "memory_usage": "3.1GB"
        })
        
        # 为第一个Agent也添加运行统计
        agents_db[0]["run_count"] = 156
        agents_db[0]["uptime"] = "3天2小时"
        agents_db[0]["memory_usage"] = "1.2GB"
        
        current_agent_id = 4

# 在应用启动时初始化数据
init_sample_data()

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

# Agent 相关接口

# 获取所有Agent
@app.get("/api/v1/agents")
async def get_agents(token: str = "mock_token_1_1234567890"):
    # 确保数据已初始化
    init_sample_data()
    
    # 如果Agent数量不足3个，直接返回固定的3个Agent数据
    if len(agents_db) < 3:
        from datetime import datetime
        
        # 返回固定的3个Agent数据
        return [
            {
                "id": 1,
                "name": "客服助手",
                "description": "用于处理客户咨询的AI助手",
                "type": "customer_service",
                "status": "running",
                "config": {
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "memory": True,
                    "tools": ["search", "calculator"]
                },
                "owner_id": 1,
                "project_id": 1,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "run_count": 156,
                "uptime": "3天2小时",
                "memory_usage": "1.2GB"
            },
            {
                "id": 2,
                "name": "代码审查助手",
                "description": "帮助审查代码质量的AI助手",
                "type": "code_review",
                "status": "stopped",
                "config": {
                    "model": "gpt-4",
                    "temperature": 0.3,
                    "max_tokens": 4000,
                    "memory": True,
                    "tools": ["code_analysis", "security_check"]
                },
                "owner_id": 1,
                "project_id": None,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "run_count": 89,
                "uptime": "1天5小时",
                "memory_usage": "2.4GB"
            },
            {
                "id": 3,
                "name": "数据分析助手",
                "description": "用于数据分析和可视化的AI助手",
                "type": "data_analysis",
                "status": "running",
                "config": {
                    "model": "claude-3-opus",
                    "temperature": 0.5,
                    "max_tokens": 8000,
                    "memory": True,
                    "tools": ["data_processing", "visualization", "statistics"]
                },
                "owner_id": 1,
                "project_id": 1,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
                "run_count": 42,
                "uptime": "12小时",
                "memory_usage": "3.1GB"
            }
        ]
    
    return agents_db

# 获取单个Agent
@app.get("/api/v1/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: int, token: str = "mock_token"):
    # 验证令牌
    if not token.startswith("mock_token"):
        return {"error": "Invalid token"}
    
    try:
        owner_id = int(token.split("_")[2])
    except:
        return {"error": "Invalid token"}
    
    # 查找Agent
    for agent in agents_db:
        if agent["id"] == agent_id and agent["owner_id"] == owner_id:
            return agent
    
    return {"error": "Agent not found"}

# 创建Agent
@app.post("/api/v1/agents", response_model=AgentResponse)
async def create_agent(agent: AgentCreate, token: str = "mock_token"):
    global current_agent_id
    
    # 验证令牌
    if not token.startswith("mock_token"):
        return {"error": "Invalid token"}
    
    try:
        owner_id = int(token.split("_")[2])
    except:
        return {"error": "Invalid token"}
    
    # 创建Agent
    new_agent = {
        "id": current_agent_id,
        "name": agent.name,
        "description": agent.description,
        "type": agent.type,
        "status": "stopped",
        "config": agent.config.dict() if agent.config else {"model": "gpt-3.5-turbo", "temperature": 0.7, "max_tokens": 2000, "memory": False, "tools": []},
        "owner_id": owner_id,
        "project_id": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    agents_db.append(new_agent)
    current_agent_id += 1
    
    return new_agent

# 启动Agent
@app.post("/api/v1/agents/{agent_id}/start")
async def start_agent(agent_id: int, token: str = "mock_token"):
    # 验证令牌
    if not token.startswith("mock_token"):
        return {"error": "Invalid token"}
    
    try:
        owner_id = int(token.split("_")[2])
    except:
        return {"error": "Invalid token"}
    
    # 查找并更新Agent状态
    for agent in agents_db:
        if agent["id"] == agent_id and agent["owner_id"] == owner_id:
            agent["status"] = "running"
            agent["updated_at"] = datetime.utcnow()
            return {"message": "Agent started successfully", "agent_id": agent_id}
    
    return {"error": "Agent not found"}

# 停止Agent
@app.post("/api/v1/agents/{agent_id}/stop")
async def stop_agent(agent_id: int, token: str = "mock_token"):
    # 验证令牌
    if not token.startswith("mock_token"):
        return {"error": "Invalid token"}
    
    try:
        owner_id = int(token.split("_")[2])
    except:
        return {"error": "Invalid token"}
    
    # 查找并更新Agent状态
    for agent in agents_db:
        if agent["id"] == agent_id and agent["owner_id"] == owner_id:
            agent["status"] = "stopped"
            agent["updated_at"] = datetime.utcnow()
            return {"message": "Agent stopped successfully", "agent_id": agent_id}
    
    return {"error": "Agent not found"}

# 与Agent交互
@app.post("/api/v1/agents/{agent_id}/interact")
async def interact_with_agent(agent_id: int, message: dict, token: str = "mock_token"):
    # 验证令牌
    if not token.startswith("mock_token"):
        return {"error": "Invalid token"}
    
    try:
        owner_id = int(token.split("_")[2])
    except:
        return {"error": "Invalid token"}
    
    # 查找Agent
    for agent in agents_db:
        if agent["id"] == agent_id and agent["owner_id"] == owner_id:
            if agent["status"] != "running":
                return {"error": "Agent is not running"}
            
            # 模拟AI响应
            response_text = f"Agent '{agent['name']}' received: {message.get('message', '')}. This is a simulated response."
            
            return {
                "response": response_text,
                "agent_id": agent_id,
                "agent_name": agent["name"],
                "timestamp": datetime.utcnow().isoformat()
            }
    
    return {"error": "Agent not found"}

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
    print("前端地址: http://localhost:5174, http://localhost:5175")
    print("测试用户: testuser / testpass")
    print("示例Agent: 客服助手, 代码审查助手")
    
    uvicorn.run(
        "start_complete:app",
        host="0.0.0.0",
        port=8003,
        reload=True
    )