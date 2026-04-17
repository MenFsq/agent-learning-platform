"""
简化的后端启动脚本 - 无LangChain依赖
"""
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# 创建FastAPI应用
app = FastAPI(
    title="Agent Learning Platform (简化版)",
    version="1.0.0",
    description="简化版后端API，无LangChain依赖"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，方便开发
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class Agent(BaseModel):
    id: str
    name: str
    description: str
    status: str = "stopped"
    model: str = "gpt-3.5-turbo"
    tools: List[str] = []
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class AgentStartRequest(BaseModel):
    agent_id: str

class AgentStopRequest(BaseModel):
    agent_id: str

class AgentInteractRequest(BaseModel):
    agent_id: str
    message: str

class AgentInteractResponse(BaseModel):
    agent_id: str
    agent_name: str
    response: str
    timestamp: str

# 模拟Agent数据
MOCK_AGENTS = {
    "agent_1776365387.509348": Agent(
        id="agent_1776365387.509348",
        name="智能文档助手",
        description="专业的文档处理和分析助手",
        status="stopped",
        model="gpt-3.5-turbo",
        tools=["文档解析", "文本摘要", "关键词提取"],
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z"
    ),
    "agent_1776365388.123456": Agent(
        id="agent_1776365388.123456",
        name="代码审查专家",
        description="专业的代码审查和质量分析助手",
        status="stopped",
        model="gpt-4",
        tools=["代码分析", "漏洞检测", "最佳实践建议"],
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z"
    ),
    "agent_1776365389.789012": Agent(
        id="agent_1776365389.789012",
        name="学习进度跟踪",
        description="学习进度跟踪和个性化推荐助手",
        status="stopped",
        model="gpt-3.5-turbo",
        tools=["进度分析", "个性化推荐", "学习计划"],
        created_at="2024-01-01T00:00:00Z",
        updated_at="2024-01-01T00:00:00Z"
    )
}

# API端点
@app.get("/")
async def root():
    return {
        "message": "Agent Learning Platform API",
        "version": "1.0.0",
        "status": "running",
        "langchain": "simulated"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "agent-learning-platform",
        "langchain": "simulated"
    }

@app.get("/api/v1/agents")
async def get_agents():
    """获取所有Agent"""
    agents = list(MOCK_AGENTS.values())
    return {
        "agents": agents,
        "count": len(agents),
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/agents/{agent_id}")
async def get_agent(agent_id: str):
    """获取特定Agent"""
    agent = MOCK_AGENTS.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@app.post("/api/v1/agents/{agent_id}/start")
async def start_agent(agent_id: str):
    """启动Agent"""
    agent = MOCK_AGENTS.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # 更新状态
    agent.status = "running"
    agent.updated_at = datetime.now().isoformat()
    
    return {
        "success": True,
        "message": f"Agent {agent.name} started successfully",
        "agent_id": agent_id,
        "status": "running"
    }

@app.post("/api/v1/agents/{agent_id}/stop")
async def stop_agent(agent_id: str):
    """停止Agent"""
    agent = MOCK_AGENTS.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # 更新状态
    agent.status = "stopped"
    agent.updated_at = datetime.now().isoformat()
    
    return {
        "success": True,
        "message": f"Agent {agent.name} stopped successfully",
        "agent_id": agent_id,
        "status": "stopped"
    }

@app.post("/api/v1/agents/{agent_id}/interact")
async def interact_with_agent(agent_id: str, request: AgentInteractRequest):
    """与Agent交互"""
    agent = MOCK_AGENTS.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    if agent.status != "running":
        raise HTTPException(status_code=400, detail=f"Agent {agent.name} is not running")
    
    # 模拟响应
    responses = {
        "agent_1776365387.509348": f"智能文档助手: 已收到您的文档查询: '{request.message}'。我会帮您分析文档内容，提供结构分析和关键信息提取。",
        "agent_1776365388.123456": f"代码审查专家: 已收到您的代码: '{request.message[:50]}...'。我会进行代码质量审查，检查潜在漏洞和最佳实践。",
        "agent_1776365389.789012": f"学习进度跟踪: 已记录您的学习进度: '{request.message}'。我会为您分析学习效果，提供个性化学习建议。"
    }
    
    response = responses.get(agent_id, f"Agent响应: {request.message}")
    
    return AgentInteractResponse(
        agent_id=agent_id,
        agent_name=agent.name,
        response=response,
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/v1/system/status")
async def system_status():
    """系统状态检查"""
    running_agents = [a for a in MOCK_AGENTS.values() if a.status == "running"]
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents": {
            "total": len(MOCK_AGENTS),
            "running": len(running_agents),
            "stopped": len(MOCK_AGENTS) - len(running_agents)
        },
        "services": {
            "api": "running",
            "database": "simulated",
            "langchain": "simulated"
        }
    }

if __name__ == "__main__":
    print("启动Agent Learning Platform (简化版)...")
    print("API地址: http://localhost:8004")
    print("API文档: http://localhost:8004/docs")
    print("LangChain: 模拟模式 (无依赖)")
    print("预加载Agent: 3个")
    
    uvicorn.run(
        "start_simple:app",
        host="0.0.0.0",
        port=8004,
        reload=True
    )