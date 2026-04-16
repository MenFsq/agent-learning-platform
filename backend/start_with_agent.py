"""
完整的后端启动脚本（包含LangChain Agent功能）
"""
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# 导入LangChain Agent模块
from langchain_agent_simple import agent_manager

# 创建FastAPI应用
app = FastAPI(
    title="Agent Learning Platform (完整版 + LangChain)",
    version="1.0.0",
    description="完整版后端API，包含用户认证、项目管理和LangChain Agent功能"
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

class AgentCreate(BaseModel):
    name: str
    description: str
    type: str = "conversational"
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.7
    max_tokens: int = 2000
    memory: bool = False
    tools: List[str] = []
    system_prompt: Optional[str] = None

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None
    memory: Optional[bool] = None
    tools: Optional[List[str]] = None
    system_prompt: Optional[str] = None

class AgentResponse(BaseModel):
    id: str
    name: str
    description: str
    type: str
    config: dict
    created_at: str
    status: str
    run_count: int

class AgentInteraction(BaseModel):
    message: str

class AgentInteractionResponse(BaseModel):
    success: bool
    response: str
    conversation_id: Optional[int] = None
    error: Optional[str] = None

# 内存数据库
users_db = []
projects_db = []
current_user_id = 1
current_project_id = 1

# 健康检查
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "agent-platform-backend-complete",
        "version": "1.0.0",
        "database": "simulated",
        "langchain": "integrated",
        "timestamp": datetime.utcnow().isoformat()
    }

# 用户注册
@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register(user: UserCreate):
    global current_user_id
    
    # 检查用户名是否已存在
    for u in users_db:
        if u["username"] == user.username:
            raise HTTPException(status_code=400, detail="Username already exists")
    
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
    
    raise HTTPException(status_code=401, detail="Invalid credentials")

# 获取当前用户
@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_current_user(token: str = "mock_token"):
    # 模拟令牌验证
    if not token.startswith("mock_token"):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # 从令牌中提取用户ID
    try:
        user_id = int(token.split("_")[2])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # 查找用户
    for user in users_db:
        if user["id"] == user_id:
            return user
    
    raise HTTPException(status_code=404, detail="User not found")

# 创建项目
@app.post("/api/v1/projects", response_model=ProjectResponse)
async def create_project(project: ProjectCreate, token: str = "mock_token"):
    global current_project_id
    
    # 验证令牌
    if not token.startswith("mock_token"):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        owner_id = int(token.split("_")[2])
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
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
    
    raise HTTPException(status_code=404, detail="Project not found")

# 系统信息
@app.get("/api/v1/system/info")
async def system_info():
    return {
        "users_count": len(users_db),
        "projects_count": len(projects_db),
        "public_projects_count": len([p for p in projects_db if p["is_public"]]),
        "agents_count": len(agent_manager.list_agents()),
        "active_since": datetime.utcnow().isoformat()
    }

# ========== LangChain Agent API ==========

# 获取所有Agent
@app.get("/api/v1/agents", response_model=List[AgentResponse])
async def get_agents():
    agents = agent_manager.list_agents()
    return agents

# 获取单个Agent
@app.get("/api/v1/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

# 创建Agent
@app.post("/api/v1/agents", response_model=AgentResponse)
async def create_agent(agent: AgentCreate):
    agent_config = {
        "name": agent.name,
        "description": agent.description,
        "type": agent.type,
        "model": agent.model,
        "temperature": agent.temperature,
        "max_tokens": agent.max_tokens,
        "memory": agent.memory,
        "tools": agent.tools,
        "system_prompt": agent.system_prompt
    }
    
    new_agent = agent_manager.create_agent(agent_config)
    return new_agent

# 更新Agent
@app.put("/api/v1/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, updates: AgentUpdate):
    # 过滤掉None值
    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    
    updated_agent = agent_manager.update_agent(agent_id, update_data)
    if not updated_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return updated_agent

# 删除Agent
@app.delete("/api/v1/agents/{agent_id}")
async def delete_agent(agent_id: str):
    success = agent_manager.delete_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"success": True, "message": "Agent deleted"}

# 启动Agent
@app.post("/api/v1/agents/{agent_id}/start")
async def start_agent(agent_id: str):
    success = agent_manager.start_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"success": True, "message": "Agent started"}

# 停止Agent
@app.post("/api/v1/agents/{agent_id}/stop")
async def stop_agent(agent_id: str):
    success = agent_manager.stop_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"success": True, "message": "Agent stopped"}

# 与Agent交互
@app.post("/api/v1/agents/{agent_id}/interact", response_model=AgentInteractionResponse)
async def interact_with_agent(agent_id: str, interaction: AgentInteraction):
    result = agent_manager.interact_with_agent(agent_id, interaction.message)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return AgentInteractionResponse(
        success=result["success"],
        response=result["response"],
        conversation_id=result.get("conversation_id")
    )

# 获取Agent对话历史
@app.get("/api/v1/agents/{agent_id}/conversations")
async def get_agent_conversations(agent_id: str, limit: int = 10):
    history = agent_manager.get_conversation_history(agent_id, limit)
    if history is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return history

# 清空Agent对话历史
@app.delete("/api/v1/agents/{agent_id}/conversations")
async def clear_agent_conversations(agent_id: str):
    success = agent_manager.clear_conversation_history(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"success": True, "message": "Conversation history cleared"}

if __name__ == "__main__":
    print("启动完整版后端服务器（包含LangChain Agent功能）...")
    print("API文档: http://localhost:8004/docs")
    print("健康检查: http://localhost:8004/health")
    print("前端地址: http://localhost:5174")
    print("测试用户: testuser / testpass")
    print(f"预加载Agent数量: {len(agent_manager.list_agents())}")
    
    uvicorn.run(
        "start_with_agent:app",
        host="0.0.0.0",
        port=8004,
        reload=True
    )