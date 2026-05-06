"""
Agent 对话聊天 API 模块
提供 AI Agent 的创建、管理、以及 DeepSeek 驱动的对话问答能力
支持文件持久化记忆系统
"""
import os
import json
import time
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field

# ----- 外部 AI SDK -----
OPENAI_AVAILABLE = False
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    pass

# ----- 持久化存储 -----
from ...storage.persistence import (
    load_agents,
    save_agents,
    load_conversations,
    save_conversations,
)

router = APIRouter(prefix="/agents", tags=["agents"])

# ----- DeepSeek 配置 -----
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", os.getenv("OPENAI_API_KEY", ""))
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
DEFAULT_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")


# ============================================================
# 数据模型
# ============================================================

class AgentConfig(BaseModel):
    """Agent 配置"""
    model: str = DEFAULT_MODEL
    temperature: float = 0.7
    max_tokens: int = 4096
    system_prompt: str = "You are a helpful AI assistant. Answer questions accurately and concisely."
    tools: List[str] = Field(default_factory=list)


class AgentCreate(BaseModel):
    """创建 Agent 请求"""
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field("", max_length=500)
    type: str = Field("chat", description="Agent 类型: chat, code-review, research")
    config: AgentConfig = Field(default_factory=AgentConfig)
    project_id: Optional[str] = None


class ChatMessage(BaseModel):
    """对话消息"""
    role: str  # user | assistant | system
    content: str
    timestamp: float = Field(default_factory=time.time)


class ChatRequest(BaseModel):
    """发送消息请求"""
    message: str = Field(..., min_length=1, max_length=10000)
    context: Optional[Dict[str, Any]] = None


class ChatResponse(BaseModel):
    """对话响应"""
    agent_id: str
    agent_name: str
    user_message: str
    response: str
    model: str
    conversation_id: str
    timestamp: str
    tokens_used: Optional[int] = None


class AgentResponse(BaseModel):
    """Agent 信息响应"""
    id: str
    name: str
    description: str
    type: str
    config: Dict[str, Any]
    status: str
    created_at: str
    conversation_count: int


# ============================================================
# 持久化存储（从磁盘加载，自动保存）
# ============================================================

agents_store: Dict[str, Dict[str, Any]] = {}
conversations_store: Dict[str, List[Dict[str, Any]]] = {}

_loaded = False


def _ensure_loaded():
    """确保从磁盘加载数据"""
    global _loaded, agents_store, conversations_store
    if _loaded:
        return
    agents_store = load_agents()
    conversations_store = load_conversations()
    _loaded = True


def _persist():
    """保存到磁盘"""
    save_agents(agents_store)
    save_conversations(conversations_store)


def _utcnow_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ============================================================
# DeepSeek 对话引擎
# ============================================================

def _chat_with_deepseek(
    messages: List[Dict[str, str]],
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 4096,
) -> str:
    """直接调用 DeepSeek API 进行对话"""
    if not OPENAI_AVAILABLE or not DEEPSEEK_API_KEY:
        return _fallback_response(messages)

    try:
        client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url=DEEPSEEK_BASE_URL,
        )
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        print(f"DeepSeek API error: {e}")
        return f"[DeepSeek API 暂时不可用] {_fallback_response(messages)}"


def _fallback_response(messages: List[Dict[str, str]]) -> str:
    """API 不可用时的回退响应"""
    last_msg = messages[-1]["content"] if messages else "Hello"
    return (
        f"I received your message: 「{last_msg[:200]}」\n\n"
        f"Currently running in offline mode. DeepSeek API connection will be "
        f"restored shortly. Your conversation history is being saved locally.\n\n"
        f"💡 Tip: Set the DEEPSEEK_API_KEY environment variable to enable AI responses."
    )


# ============================================================
# API 端点
# ============================================================

@router.get("", response_model=List[AgentResponse])
async def list_agents():
    """获取所有 Agent"""
    _ensure_loaded()
    return [
        AgentResponse(
            id=agent["id"],
            name=agent["name"],
            description=agent.get("description", ""),
            type=agent.get("type", "chat"),
            config=agent.get("config", {}),
            status=agent.get("status", "stopped"),
            created_at=agent.get("created_at", _utcnow_iso()),
            conversation_count=len(conversations_store.get(agent["id"], [])),
        )
        for agent in agents_store.values()
    ]


@router.post("", response_model=AgentResponse)
async def create_agent(req: AgentCreate):
    """创建新 Agent"""
    _ensure_loaded()
    agent_id = f"agent_{uuid4().hex[:12]}"
    now = _utcnow_iso()

    agent = {
        "id": agent_id,
        "name": req.name,
        "description": req.description,
        "type": req.type,
        "config": req.config.model_dump(),
        "status": "running",
        "project_id": req.project_id,
        "created_at": now,
        "updated_at": now,
    }
    agents_store[agent_id] = agent
    conversations_store[agent_id] = []
    _persist()

    return AgentResponse(
        id=agent_id,
        name=req.name,
        description=req.description,
        type=req.type,
        config=req.config.model_dump(),
        status="running",
        created_at=now,
        conversation_count=0,
    )


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """获取单个 Agent"""
    _ensure_loaded()
    agent = agents_store.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return AgentResponse(
        id=agent["id"],
        name=agent["name"],
        description=agent.get("description", ""),
        type=agent.get("type", "chat"),
        config=agent.get("config", {}),
        status=agent.get("status", "running"),
        created_at=agent.get("created_at", ""),
        conversation_count=len(conversations_store.get(agent_id, [])),
    )


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    """删除 Agent"""
    _ensure_loaded()
    if agent_id not in agents_store:
        raise HTTPException(status_code=404, detail="Agent not found")
    del agents_store[agent_id]
    conversations_store.pop(agent_id, None)
    _persist()
    return {"success": True, "message": "Agent deleted"}


@router.post("/{agent_id}/chat", response_model=ChatResponse)
async def chat_with_agent(agent_id: str, req: ChatRequest):
    """与 Agent 对话（自动持久化记忆）"""
    _ensure_loaded()
    agent = agents_store.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    config = agent.get("config", {})
    system_prompt = config.get("system_prompt", "You are a helpful AI assistant.")
    model = config.get("model", DEFAULT_MODEL)
    temperature = config.get("temperature", 0.7)
    max_tokens = config.get("max_tokens", 4096)

    # 构建消息历史
    history = conversations_store.get(agent_id, [])
    messages: List[Dict[str, str]] = [{"role": "system", "content": system_prompt}]

    # 取最近 20 条作为上下文
    for msg in history[-20:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": req.message})

    # 调用 DeepSeek
    response_text = _chat_with_deepseek(messages, model, temperature, max_tokens)

    # 保存消息
    conversation_id = str(uuid4())
    history.append({
        "id": conversation_id,
        "role": "user",
        "content": req.message,
        "timestamp": time.time(),
    })
    history.append({
        "id": str(uuid4()),
        "role": "assistant",
        "content": response_text,
        "timestamp": time.time(),
    })
    conversations_store[agent_id] = history
    _persist()  # 每次对话后自动保存

    return ChatResponse(
        agent_id=agent_id,
        agent_name=agent["name"],
        user_message=req.message,
        response=response_text,
        model=model,
        conversation_id=conversation_id,
        timestamp=_utcnow_iso(),
    )


@router.get("/{agent_id}/conversations")
async def get_conversations(agent_id: str, limit: int = 50):
    """获取对话历史"""
    _ensure_loaded()
    if agent_id not in agents_store:
        raise HTTPException(status_code=404, detail="Agent not found")
    history = conversations_store.get(agent_id, [])
    return history[-limit:]


@router.delete("/{agent_id}/conversations")
async def clear_conversations(agent_id: str):
    """清空对话历史"""
    _ensure_loaded()
    if agent_id not in agents_store:
        raise HTTPException(status_code=404, detail="Agent not found")
    conversations_store[agent_id] = []
    _persist()
    return {"success": True, "message": "Conversations cleared"}


# ============================================================
# 初始化默认 Agent
# ============================================================

def _init_default_agents():
    """创建默认 Agent（仅在首次运行时）"""
    _ensure_loaded()
    if agents_store:
        return  # 已有数据，不覆盖

    defaults = [
        {
            "name": "通用助手",
            "description": "全能 AI 助手，可以回答任何技术问题",
            "type": "chat",
            "config": {
                "model": DEFAULT_MODEL,
                "temperature": 0.7,
                "max_tokens": 4096,
                "system_prompt": (
                    "你是小老虎 AI 助手，一个专业的技术伙伴。"
                    "你擅长 Vue 3、TypeScript、OpenClaw 技能开发、代码审查和前端工程化。"
                    "用简洁、专业、偶尔带点幽默的方式回答问题。"
                    "如果用户问技术问题，给出代码示例和最佳实践。"
                ),
            },
        },
        {
            "name": "代码审查专家",
            "description": "专注于 Vue 3 代码质量审查",
            "type": "code-review",
            "config": {
                "model": DEFAULT_MODEL,
                "temperature": 0.3,
                "max_tokens": 4096,
                "system_prompt": (
                    "你是一个 Vue 3 代码审查专家。分析代码时关注：\n"
                    "1. Composition API 正确使用\n"
                    "2. TypeScript 类型安全\n"
                    "3. 响应式系统最佳实践\n"
                    "4. 组件设计模式\n"
                    "5. 性能优化机会\n"
                    "6. 安全性问题\n"
                    "给出具体行号和修改建议。"
                ),
            },
        },
    ]

    for d in defaults:
        agent_id = f"agent_{uuid4().hex[:12]}"
        now = _utcnow_iso()
        agents_store[agent_id] = {**d, "id": agent_id, "status": "running",
                                   "created_at": now, "updated_at": now}
        conversations_store[agent_id] = []

    _persist()
    print(f"[Agent] 初始化 {len(defaults)} 个默认 Agent 并持久化到磁盘")


_init_default_agents()
