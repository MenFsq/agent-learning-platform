"""
简化版后端启动脚本（包含模拟的Agent功能）
"""
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import time
import random

# 创建FastAPI应用
app = FastAPI(
    title="Agent Learning Platform (简化版)",
    version="1.0.0",
    description="简化版后端API，包含用户认证、项目管理和模拟Agent功能"
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
    uptime: Optional[str] = None
    memory_usage: Optional[str] = None

class AgentInteraction(BaseModel):
    message: str

class AgentInteractionResponse(BaseModel):
    success: bool
    response: str
    conversation_id: Optional[int] = None
    error: Optional[str] = None

# 模拟Agent管理器
class MockAgentManager:
    def __init__(self):
        self.agents: Dict[str, Dict[str, Any]] = {}
        self.conversations: Dict[str, List[Dict]] = {}
        self.agent_start_times: Dict[str, float] = {}
        self._initialize_sample_agents()
    
    def _initialize_sample_agents(self):
        """初始化示例Agent"""
        sample_agents = [
            {
                "id": "agent_1",
                "name": "文档分析助手",
                "description": "使用LangChain分析文档内容，提取关键信息",
                "type": "tool-calling",
                "config": {
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "memory": True,
                    "tools": ["file-reader", "web-search"],
                    "system_prompt": "你是一个专业的文档分析助手。"
                },
                "created_at": datetime.now().isoformat(),
                "status": "stopped",
                "run_count": 12
            },
            {
                "id": "agent_2",
                "name": "代码审查助手",
                "description": "自动审查代码质量，提供改进建议",
                "type": "conversational",
                "config": {
                    "model": "gpt-3.5-turbo",
                    "temperature": 0.3,
                    "max_tokens": 1000,
                    "memory": False,
                    "tools": ["code-executor"],
                    "system_prompt": "你是一个专业的代码审查助手。"
                },
                "created_at": datetime.now().isoformat(),
                "status": "running",
                "run_count": 28,
                "uptime": "5小时30分钟",
                "memory_usage": "128MB"
            },
            {
                "id": "agent_3",
                "name": "数据分析助手",
                "description": "处理和分析结构化数据，生成可视化报告",
                "type": "planning",
                "config": {
                    "model": "gpt-4",
                    "temperature": 0.5,
                    "max_tokens": 4000,
                    "memory": True,
                    "tools": ["database-query", "calculator"],
                    "system_prompt": "你是一个专业的数据分析助手。"
                },
                "created_at": datetime.now().isoformat(),
                "status": "error",
                "run_count": 8,
                "uptime": "45分钟",
                "memory_usage": "512MB"
            }
        ]
        
        for agent in sample_agents:
            self.agents[agent["id"]] = agent
            self.conversations[agent["id"]] = []
    
    def create_agent(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """创建新的Agent"""
        agent_id = f"agent_{int(time.time())}"
        
        agent = {
            "id": agent_id,
            "name": agent_config.get("name", "未命名Agent"),
            "description": agent_config.get("description", ""),
            "type": agent_config.get("type", "conversational"),
            "config": {
                "model": agent_config.get("model", "gpt-3.5-turbo"),
                "temperature": agent_config.get("temperature", 0.7),
                "max_tokens": agent_config.get("max_tokens", 2000),
                "memory": agent_config.get("memory", False),
                "tools": agent_config.get("tools", []),
                "system_prompt": agent_config.get("system_prompt", "你是一个有帮助的AI助手。")
            },
            "created_at": datetime.now().isoformat(),
            "status": "stopped",
            "run_count": 0
        }
        
        self.agents[agent_id] = agent
        self.conversations[agent_id] = []
        
        return agent
    
    def get_agent(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """获取Agent信息"""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Dict[str, Any]]:
        """列出所有Agent"""
        return list(self.agents.values())
    
    def update_agent(self, agent_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新Agent配置"""
        if agent_id not in self.agents:
            return None
        
        agent = self.agents[agent_id]
        
        # 更新配置
        for key, value in updates.items():
            if key in ["name", "description", "type"]:
                agent[key] = value
            elif key == "config":
                agent["config"].update(value)
        
        return agent
    
    def delete_agent(self, agent_id: str) -> bool:
        """删除Agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            if agent_id in self.conversations:
                del self.conversations[agent_id]
            if agent_id in self.agent_start_times:
                del self.agent_start_times[agent_id]
            return True
        return False
    
    def start_agent(self, agent_id: str) -> bool:
        """启动Agent"""
        if agent_id not in self.agents:
            return False
        
        self.agents[agent_id]["status"] = "running"
        self.agents[agent_id]["run_count"] += 1
        self.agent_start_times[agent_id] = time.time()
        
        # 模拟运行时间和内存使用
        uptime_minutes = random.randint(1, 60)
        memory_mb = random.randint(128, 1024)
        
        self.agents[agent_id]["uptime"] = f"{uptime_minutes}分钟"
        self.agents[agent_id]["memory_usage"] = f"{memory_mb}MB"
        
        return True
    
    def stop_agent(self, agent_id: str) -> bool:
        """停止Agent"""
        if agent_id not in self.agents:
            return False
        
        self.agents[agent_id]["status"] = "stopped"
        if agent_id in self.agent_start_times:
            del self.agent_start_times[agent_id]
        
        return True
    
    def interact_with_agent(self, agent_id: str, message: str) -> Dict[str, Any]:
        """与Agent交互"""
        if agent_id not in self.agents:
            return {"error": "Agent not found"}
        
        agent = self.agents[agent_id]
        
        if agent["status"] != "running":
            return {"error": "Agent is not running"}
        
        # 模拟Agent响应
        responses = [
            f"我已收到您的消息: \"{message}\"",
            f"正在处理您的请求: {message}",
            f"根据我的分析，关于\"{message}\"的建议是...",
            f"处理完成，结果如下: 这是对\"{message}\"的模拟响应。",
            f"好的，我理解了。关于\"{message}\"，我的回答是...",
            f"这是一个很好的问题！让我思考一下\"{message}\"..."
        ]
        
        response = random.choice(responses)
        
        # 记录对话
        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": message,
            "agent": response,
            "intermediate_steps": []
        }
        
        self.conversations[agent_id].append(conversation_entry)
        
        return {
            "success": True,
            "response": response,
            "conversation_id": len(self.conversations[agent_id]) - 1
        }
    
    def get_conversation_history(self, agent_id: str, limit: int = 10) -> List[Dict]:
        """获取对话历史"""
        if agent_id not in self.conversations:
            return []
        
        return self.conversations[agent_id][-limit:]
    
    def clear_conversation_history(self, agent_id: str) -> bool:
        """清空对话历史"""
        if agent_id in self.conversations:
            self.conversations[agent_id] = []
            return True
        return False

# 全局Agent管理器实例
agent_manager = MockAgentManager()

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
        "service": "agent-platform-backend-simple",
        "version": "1.0.0",
        "database": "simulated",
        "agents": "mock",
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

# ========== Agent API ==========

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
    print("启动简化版后端服务器（包含模拟Agent功能）...")
    print("API文档: http://localhost:8005/docs")
    print("健康检查: http://localhost:8005/health")
    print("前端地址: http://localhost:5174")
    print("测试用户: testuser / testpass")
    print(f"预加载Agent数量: {len(agent_manager.list_agents())}")
    
    uvicorn.run(
        "start_simple_agent:app",
        host="0.0.0.0",
        port=8005,
        reload=True
    )