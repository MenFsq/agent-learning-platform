"""
统一后的后端启动脚本。

将认证、项目管理和 Agent 管理正式接入数据库。
"""

from __future__ import annotations

import os
import random
import re
import time
import enum
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import uuid4

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import JSON, Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

from src.core.config import settings
from src.core.database import AsyncSessionLocal, engine, get_db
from src.core.security import create_access_token, create_refresh_token, decode_token, get_password_hash, verify_password

load_dotenv()

DEFAULT_CHAT_MODEL = os.getenv("DEFAULT_CHAT_MODEL", "deepseek-chat")
DEFAULT_REASONER_MODEL = os.getenv("DEFAULT_REASONER_MODEL", "deepseek-reasoner")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
APP_BASE = declarative_base()


def utcnow() -> datetime:
    return datetime.utcnow()


def iso_now() -> str:
    return utcnow().isoformat()


def model_dump_compat(model: BaseModel) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or f"project-{int(time.time())}"


def ensure_unique_slug(base_slug: str, existing_slugs: set[str]) -> str:
    if base_slug not in existing_slugs:
        return base_slug

    index = 2
    while f"{base_slug}-{index}" in existing_slugs:
        index += 1
    return f"{base_slug}-{index}"


def project_status_value(value: Optional[str]) -> ProjectStatus:
    if not value:
        return ProjectStatus.ACTIVE
    try:
        return ProjectStatus(value)
    except ValueError:
        return ProjectStatus.ACTIVE


def project_type_value(value: Optional[str]) -> ProjectType:
    if not value:
        return ProjectType.LEARNING
    try:
        return ProjectType(value)
    except ValueError:
        return ProjectType.LEARNING


def user_to_response(user: User) -> Dict[str, Any]:
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "created_at": user.created_at,
    }


def project_to_response(project: Project) -> Dict[str, Any]:
    total_tasks = project.total_tasks or 0
    completed_tasks = project.completed_tasks or 0
    progress = round((completed_tasks / total_tasks) * 100, 2) if total_tasks else 0
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "owner_id": project.owner_id,
        "is_public": project.is_public,
        "status": project.status.value if hasattr(project.status, "value") else project.status,
        "created_at": project.created_at,
        "updated_at": project.updated_at,
        "type": project.type.value if hasattr(project.type, "value") else project.type,
        "due_date": project.completed_at.isoformat() if project.completed_at else None,
        "progress": progress,
        "collaborator_count": project.total_members or 1,
        "task_total": total_tasks,
        "task_completed": completed_tasks,
    }


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    DEVELOPER = "developer"
    MANAGER = "manager"


class User(APP_BASE):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)


class UserSession(APP_BASE):
    __tablename__ = "user_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    session_token: Mapped[str] = mapped_column(String(500), unique=True, index=True, nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(500), unique=True, index=True, nullable=False)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    last_used_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class ProjectStatus(str, enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class ProjectType(str, enum.Enum):
    LEARNING = "learning"
    DEVELOPMENT = "development"
    RESEARCH = "research"
    PRODUCTION = "production"


class Project(APP_BASE):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    short_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), default=ProjectStatus.DRAFT, nullable=False)
    type: Mapped[ProjectType] = mapped_column(Enum(ProjectType), default=ProjectType.LEARNING, nullable=False)
    tags: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    technologies: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    config: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    settings: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    total_tasks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_tasks: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    total_members: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    total_contributions: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)


class UnifiedAgentRecord(APP_BASE):
    __tablename__ = "unified_agents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="conversational")
    config: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="stopped")
    run_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    uptime: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    memory_usage: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    owner_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    project_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    conversations: Mapped[List[Dict[str, Any]]] = mapped_column(JSON, nullable=False, default=list)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=utcnow)


def resolve_llm_provider_settings(requested_model: Optional[str] = None) -> Dict[str, Optional[str]]:
    deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if deepseek_api_key:
        model = requested_model or DEFAULT_CHAT_MODEL
        if model.startswith("gpt-") or model.startswith("claude-"):
            model = DEFAULT_CHAT_MODEL
        return {
            "provider": "deepseek",
            "api_key": deepseek_api_key,
            "base_url": DEEPSEEK_BASE_URL,
            "model": model,
        }

    return {
        "provider": "openai",
        "api_key": openai_api_key,
        "base_url": os.getenv("OPENAI_BASE_URL"),
        "model": requested_model or DEFAULT_CHAT_MODEL,
    }


LANGCHAIN_AVAILABLE = False
LANGCHAIN_VERSION = "none"
ChatOpenAI = None
AgentExecutor = None
create_openai_tools_agent = None
ChatPromptTemplate = None
MessagesPlaceholder = None
ConversationBufferMemory = None
Tool = None
initialize_agent = None
AgentType = None

try:
    from langchain_openai import ChatOpenAI
    from langchain.agents import AgentExecutor, Tool, create_openai_tools_agent
    from langchain.memory import ConversationBufferMemory
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

    LANGCHAIN_AVAILABLE = True
    LANGCHAIN_VERSION = "new"
except ImportError:
    try:
        from langchain.agents import AgentType, Tool, initialize_agent
        from langchain.chat_models import ChatOpenAI
        from langchain.memory import ConversationBufferMemory

        LANGCHAIN_AVAILABLE = True
        LANGCHAIN_VERSION = "old"
    except ImportError:
        LANGCHAIN_AVAILABLE = False
        LANGCHAIN_VERSION = "none"


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: Optional[str] = None
    created_at: datetime


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False
    status: str = "active"


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    status: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    owner_id: int
    is_public: bool
    status: str = "active"
    created_at: datetime
    updated_at: datetime
    type: Optional[str] = None
    due_date: Optional[str] = None
    progress: int = 0
    collaborator_count: int = 1
    task_total: int = 0
    task_completed: int = 0


class AgentCreate(BaseModel):
    name: str
    description: str
    type: str = "conversational"
    model: str = DEFAULT_CHAT_MODEL
    temperature: float = 0.7
    max_tokens: int = 2000
    memory: bool = False
    tools: List[str] = Field(default_factory=list)
    system_prompt: Optional[str] = None
    project_id: Optional[int] = None


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
    project_id: Optional[int] = None


class AgentResponse(BaseModel):
    id: str
    name: str
    description: str
    type: str
    config: Dict[str, Any]
    created_at: str
    status: str
    run_count: int
    uptime: Optional[str] = None
    memory_usage: Optional[str] = None
    owner_id: Optional[int] = None
    project_id: Optional[int] = None
    updated_at: Optional[str] = None


class AgentInteraction(BaseModel):
    message: str


class AgentInteractionResponse(BaseModel):
    success: bool
    response: str
    conversation_id: Optional[int] = None
    error: Optional[str] = None


class UnifiedAgentManager:
    def __init__(self) -> None:
        self.executors: Dict[str, Any] = {}
        self.agent_start_times: Dict[str, float] = {}

    def _build_tools(self, tool_names: List[str]) -> List[Any]:
        if not LANGCHAIN_AVAILABLE or Tool is None:
            return []

        tool_map = {
            "web-search": ("web_search", self._web_search, "搜索网页获取最新信息"),
            "calculator": ("calculator", self._calculator, "执行数学计算"),
            "code-executor": ("code_executor", self._code_executor, "执行 Python 代码"),
            "file-reader": ("file_reader", self._file_reader, "读取文件内容"),
            "database-query": ("database_query", self._database_query, "查询数据库"),
            "document-analyzer": ("document_analyzer", self._document_analyzer, "分析文档内容"),
            "learning-tracker": ("learning_tracker", self._learning_tracker, "跟踪学习进度"),
        }
        tools: List[Any] = []
        for tool_name in tool_names:
            definition = tool_map.get(tool_name)
            if definition:
                name, func, description = definition
                tools.append(Tool(name=name, func=func, description=description))
        return tools

    def _build_executor(self, config: Dict[str, Any]) -> Optional[Any]:
        if not LANGCHAIN_AVAILABLE:
            return None

        try:
            llm_settings = resolve_llm_provider_settings(config.get("model"))
            api_key = llm_settings["api_key"]
            model_name = llm_settings["model"] or DEFAULT_CHAT_MODEL
            base_url = llm_settings["base_url"]
            temperature = config.get("temperature", 0.7)
            max_tokens = config.get("max_tokens", 2000)
            tools = self._build_tools(config.get("tools", []))
            system_prompt = config.get("system_prompt") or "你是一个有帮助的AI助手。"

            if not api_key:
                return None

            if LANGCHAIN_VERSION == "new":
                llm_kwargs = {
                    "model": model_name,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "api_key": api_key,
                }
                if base_url:
                    llm_kwargs["base_url"] = base_url
                llm = ChatOpenAI(**llm_kwargs)
                prompt = ChatPromptTemplate.from_messages(
                    [
                        ("system", system_prompt),
                        MessagesPlaceholder(variable_name="chat_history"),
                        ("human", "{input}"),
                        MessagesPlaceholder(variable_name="agent_scratchpad"),
                    ]
                )
                memory = (
                    ConversationBufferMemory(memory_key="chat_history", return_messages=True)
                    if config.get("memory")
                    else None
                )
                agent = create_openai_tools_agent(llm, tools, prompt)
                return AgentExecutor(
                    agent=agent,
                    tools=tools,
                    memory=memory,
                    verbose=True,
                    handle_parsing_errors=True,
                )

            llm_kwargs = {
                "temperature": temperature,
                "model_name": model_name,
                "openai_api_key": api_key,
            }
            if base_url:
                llm_kwargs["openai_api_base"] = base_url
            llm = ChatOpenAI(**llm_kwargs)
            memory = (
                ConversationBufferMemory(memory_key="chat_history", return_messages=True)
                if config.get("memory")
                else None
            )
            return initialize_agent(
                tools=tools,
                llm=llm,
                agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                memory=memory,
                verbose=True,
                handle_parsing_errors=True,
            )
        except Exception:
            return None

    def hydrate_executor(self, agent_id: str, config: Dict[str, Any]) -> None:
        self.executors[agent_id] = self._build_executor(config)

    def remove_executor(self, agent_id: str) -> None:
        self.executors.pop(agent_id, None)
        self.agent_start_times.pop(agent_id, None)

    def _fallback_response(self, agent: UnifiedAgentRecord, message: str) -> str:
        tool_hint = "、".join((agent.config or {}).get("tools", [])) or "无工具"
        templates = [
            f"{agent.name} 已收到请求：{message}",
            f"关于“{message}”，{agent.name} 的建议是先结合工具 {tool_hint} 做进一步分析。",
            f"{agent.name} 正在处理：{message}。当前为{'LangChain' if self.executors.get(agent.id) else '模拟'}模式响应。",
            f"处理完成：这是 {agent.name} 针对“{message}”的统一脚本回复。",
        ]
        return random.choice(templates)

    def _web_search(self, query: str) -> str:
        return f"搜索 '{query}' 的结果：\n1. 相关结果1\n2. 相关结果2\n3. 相关结果3"

    def _calculator(self, expression: str) -> str:
        try:
            allowed_chars = "0123456789+-*/(). "
            if not all(char in allowed_chars for char in expression):
                return "错误：表达式包含不安全字符"
            return f"{expression} = {eval(expression)}"
        except Exception as exc:
            return f"计算错误：{exc}"

    def _code_executor(self, code: str) -> str:
        return f"执行代码：\n{code}\n\n输出：代码执行成功（模拟）"

    def _file_reader(self, file_path: str) -> str:
        if not os.path.exists(file_path):
            return f"文件 '{file_path}' 不存在。"
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return f"文件 '{file_path}' 的内容预览：\n{file.read(1000)}"
        except Exception as exc:
            return f"读取文件失败：{exc}"

    def _database_query(self, query: str) -> str:
        return f"数据库查询：{query}\n\n结果：模拟查询结果"

    def _document_analyzer(self, query: str) -> str:
        return f"已分析文档内容：{query}\n结论：结构清晰，建议继续提取摘要和关键词。"

    def _learning_tracker(self, progress: str) -> str:
        return f"学习进度分析：{progress}\n建议：保持节奏，优先复习高频薄弱点。"

    def to_response(self, agent: UnifiedAgentRecord) -> Dict[str, Any]:
        return {
            "id": agent.id,
            "name": agent.name,
            "description": agent.description,
            "type": agent.type,
            "config": agent.config or {},
            "created_at": agent.created_at.isoformat(),
            "updated_at": agent.updated_at.isoformat() if agent.updated_at else None,
            "status": agent.status,
            "run_count": agent.run_count,
            "uptime": agent.uptime,
            "memory_usage": agent.memory_usage,
            "owner_id": agent.owner_id,
            "project_id": agent.project_id,
        }


agent_manager = UnifiedAgentManager()
DB_BOOTSTRAP_OK = False
DB_BOOTSTRAP_ERROR: Optional[str] = None


def ensure_database_ready() -> None:
    if DB_BOOTSTRAP_OK:
        return
    detail = DB_BOOTSTRAP_ERROR or "Database is not available"
    raise HTTPException(status_code=503, detail=f"Database unavailable: {detail}")


async def get_current_user_record(
    authorization: Optional[str],
    db: AsyncSession,
) -> User:
    ensure_database_ready()
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    token = authorization.replace("Bearer ", "").strip()
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    session_result = await db.execute(
        select(UserSession).where(
            UserSession.session_token == token,
            UserSession.is_active.is_(True),
            UserSession.expires_at > utcnow(),
        )
    )
    session = session_result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=401, detail="Session expired or revoked")

    user_result = await db.execute(select(User).where(User.id == int(user_id), User.is_active.is_(True)))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.last_used_at = utcnow()
    await db.flush()
    return user


async def bootstrap_unified_data() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(APP_BASE.metadata.create_all)

    async with AsyncSessionLocal() as db:
        user_result = await db.execute(select(User).where(User.username == "testuser"))
        user = user_result.scalar_one_or_none()
        if not user:
            user = User(
                username="testuser",
                email="test@example.com",
                hashed_password=get_password_hash("testpass"),
                full_name="测试用户",
                role=UserRole.USER,
                is_active=True,
                is_verified=False,
                created_at=utcnow(),
                updated_at=utcnow(),
            )
            db.add(user)
            await db.flush()

        project_result = await db.execute(select(Project).where(Project.owner_id == user.id))
        owned_projects = project_result.scalars().all()
        existing_names = {project.name for project in owned_projects}

        sample_projects = [
            ("示例项目", "这是一个示例项目", True, ProjectStatus.ACTIVE),
            ("AI Agent集成", "整合 LangChain 与统一后端逻辑", False, ProjectStatus.ACTIVE),
        ]
        existing_slugs = {
            row[0]
            for row in (
                await db.execute(select(Project.slug))
            ).all()
        }
        for name, description, is_public, status in sample_projects:
            if name in existing_names:
                continue
            slug = ensure_unique_slug(slugify(name), existing_slugs)
            existing_slugs.add(slug)
            db.add(
                Project(
                    name=name,
                    slug=slug,
                    description=description,
                    short_description=description[:120],
                    status=status,
                    type=ProjectType.LEARNING,
                    tags=[],
                    technologies=[],
                    config={},
                    settings={},
                    owner_id=user.id,
                    created_at=utcnow(),
                    updated_at=utcnow(),
                    is_public=is_public,
                    is_featured=False,
                    total_tasks=0,
                    completed_tasks=0,
                    total_members=1,
                    total_contributions=0,
                )
            )

        agent_result = await db.execute(select(UnifiedAgentRecord.id).where(UnifiedAgentRecord.is_deleted.is_(False)))
        existing_agent_ids = {row[0] for row in agent_result.all()}
        sample_agents = [
            {
                "id": "agent_1",
                "name": "文档分析助手",
                "description": "使用 LangChain 分析文档内容，提取关键信息",
                "type": "tool-calling",
                "status": "running",
                "run_count": 156,
                "uptime": "3天2小时",
                "memory_usage": "1.2GB",
                "config": {
                    "model": DEFAULT_CHAT_MODEL,
                    "temperature": 0.7,
                    "max_tokens": 2000,
                    "memory": True,
                    "tools": ["file-reader", "web-search", "document-analyzer"],
                    "system_prompt": "你是一个专业的文档分析助手。请帮助用户分析文档并提取关键信息。",
                },
            },
            {
                "id": "agent_2",
                "name": "代码审查助手",
                "description": "自动审查代码质量，提供改进建议",
                "type": "conversational",
                "status": "stopped",
                "run_count": 89,
                "uptime": "1天5小时",
                "memory_usage": "2.4GB",
                "config": {
                    "model": DEFAULT_CHAT_MODEL,
                    "temperature": 0.3,
                    "max_tokens": 4000,
                    "memory": True,
                    "tools": ["code-executor"],
                    "system_prompt": "你是一个专业的代码审查助手。请指出问题并给出改进建议。",
                },
            },
            {
                "id": "agent_3",
                "name": "数据分析助手",
                "description": "处理和分析结构化数据，生成可视化报告",
                "type": "planning",
                "status": "running",
                "run_count": 42,
                "uptime": "12小时",
                "memory_usage": "3.1GB",
                "config": {
                    "model": DEFAULT_REASONER_MODEL,
                    "temperature": 0.5,
                    "max_tokens": 4000,
                    "memory": True,
                    "tools": ["database-query", "calculator", "learning-tracker"],
                    "system_prompt": "你是一个专业的数据分析助手。请帮助用户分析数据并提供洞察。",
                },
            },
        ]
        for payload in sample_agents:
            if payload["id"] in existing_agent_ids:
                continue
            db.add(
                UnifiedAgentRecord(
                    id=payload["id"],
                    name=payload["name"],
                    description=payload["description"],
                    type=payload["type"],
                    config=payload["config"],
                    status=payload["status"],
                    run_count=payload["run_count"],
                    uptime=payload["uptime"],
                    memory_usage=payload["memory_usage"],
                    owner_id=user.id,
                    project_id=None,
                    conversations=[],
                    created_at=utcnow(),
                    updated_at=utcnow(),
                )
            )

        await db.commit()

        hydrated_agents = await db.execute(
            select(UnifiedAgentRecord).where(UnifiedAgentRecord.is_deleted.is_(False))
        )
        for agent in hydrated_agents.scalars().all():
            agent_manager.hydrate_executor(agent.id, agent.config or {})
            if agent.status == "running":
                agent_manager.agent_start_times[agent.id] = time.time()


app = FastAPI(
    title="Agent Learning Platform (统一版)",
    version="1.0.0",
    description="统一版后端 API，整合认证、项目管理与 LangChain Agent 功能。",
)

cors_origins = [str(origin).rstrip("/") for origin in settings.CORS_ORIGINS] if settings.CORS_ORIGINS else [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "http://localhost:5176",
    "http://localhost:5177",
    "http://localhost:5178",
    "http://localhost:5179",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    global DB_BOOTSTRAP_OK, DB_BOOTSTRAP_ERROR
    try:
        await bootstrap_unified_data()
        DB_BOOTSTRAP_OK = True
        DB_BOOTSTRAP_ERROR = None
    except Exception as exc:
        DB_BOOTSTRAP_OK = False
        DB_BOOTSTRAP_ERROR = str(exc) or f"{type(exc).__name__}"
        print(f"[startup] database bootstrap skipped: {exc}")


@app.get("/")
async def root() -> Dict[str, Any]:
    return {
        "message": "Agent Learning Platform 统一后端 API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "port": 8005,
        "langchain": {"available": LANGCHAIN_AVAILABLE, "version": LANGCHAIN_VERSION},
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    agents_count = 0
    if DB_BOOTSTRAP_OK:
        async with AsyncSessionLocal() as db:
            agents_count = (
                await db.execute(
                    select(func.count())
                    .select_from(UnifiedAgentRecord)
                    .where(UnifiedAgentRecord.is_deleted.is_(False))
                )
            ).scalar_one()

    return {
        "status": "healthy" if DB_BOOTSTRAP_OK else "degraded",
        "service": "agent-platform-backend-unified",
        "version": "1.0.0",
        "database": "connected" if DB_BOOTSTRAP_OK else "unavailable",
        "database_error": DB_BOOTSTRAP_ERROR,
        "langchain": "integrated" if LANGCHAIN_AVAILABLE else "mock-fallback",
        "agents_count": agents_count,
        "timestamp": iso_now(),
    }


@app.get("/api/health")
async def api_health_check() -> Dict[str, Any]:
    return await health_check()


@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    ensure_database_ready()
    existing = await db.execute(
        select(User).where(or_(User.username == user.username, User.email == user.email))
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
        role=UserRole.USER,
        is_active=True,
        is_verified=False,
        created_at=utcnow(),
        updated_at=utcnow(),
    )
    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)
    return user_to_response(new_user)


@app.post("/api/v1/auth/login")
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    ensure_database_ready()
    result = await db.execute(
        select(User).where(
            or_(User.username == credentials.username, User.email == credentials.username),
            User.is_active.is_(True),
        )
    )
    user = result.scalar_one_or_none()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(user.id), "username": user.username})
    refresh_token = create_refresh_token({"sub": str(user.id), "username": user.username})

    session = UserSession(
        user_id=user.id,
        session_token=access_token,
        refresh_token=refresh_token,
        user_agent="start_unified",
        ip_address="local",
        expires_at=utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        created_at=utcnow(),
        last_used_at=utcnow(),
        is_active=True,
    )
    db.add(session)
    user.last_login = utcnow()
    user.updated_at = utcnow()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
        },
    }


@app.post("/api/v1/auth/refresh")
async def refresh_token(
    payload: Optional[RefreshTokenRequest] = None,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    ensure_database_ready()
    refresh_token_value = payload.refresh_token if payload and payload.refresh_token else None

    if not refresh_token_value and authorization:
        access_token = authorization.replace("Bearer ", "").strip()
        session_result = await db.execute(
            select(UserSession).where(UserSession.session_token == access_token, UserSession.is_active.is_(True))
        )
        session = session_result.scalar_one_or_none()
        refresh_token_value = session.refresh_token if session else None

    if not refresh_token_value:
        raise HTTPException(status_code=401, detail="Refresh token required")

    payload_data = decode_token(refresh_token_value)
    if payload_data.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    session_result = await db.execute(
        select(UserSession).where(
            UserSession.refresh_token == refresh_token_value,
            UserSession.is_active.is_(True),
            UserSession.expires_at > utcnow(),
        )
    )
    session = session_result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=401, detail="Refresh session not found")

    user_result = await db.execute(select(User).where(User.id == session.user_id, User.is_active.is_(True)))
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token({"sub": str(user.id), "username": user.username})
    new_refresh_token = create_refresh_token({"sub": str(user.id), "username": user.username})
    session.session_token = new_access_token
    session.refresh_token = new_refresh_token
    session.last_used_at = utcnow()
    session.expires_at = utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }


@app.get("/api/v1/auth/me", response_model=UserResponse)
async def get_current_user(
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    user = await get_current_user_record(authorization, db)
    return user_to_response(user)


@app.get("/api/v1/projects", response_model=List[ProjectResponse])
async def get_projects(
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> List[Dict[str, Any]]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(
        select(Project).where(Project.owner_id == current_user.id).order_by(Project.created_at.desc())
    )
    return [project_to_response(project) for project in result.scalars().all()]


@app.get("/api/v1/projects/my", response_model=List[ProjectResponse])
async def get_my_projects(
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> List[Dict[str, Any]]:
    ensure_database_ready()
    return await get_projects(authorization, db)


@app.get("/api/v1/projects/public", response_model=List[ProjectResponse])
async def get_public_projects(db: AsyncSession = Depends(get_db)) -> List[Dict[str, Any]]:
    ensure_database_ready()
    result = await db.execute(
        select(Project).where(Project.is_public.is_(True)).order_by(Project.created_at.desc())
    )
    return [project_to_response(project) for project in result.scalars().all()]


@app.get("/api/v1/projects/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    if not project or (project.owner_id != current_user.id and not project.is_public):
        raise HTTPException(status_code=404, detail="Project not found")
    return project_to_response(project)


@app.post("/api/v1/projects", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    existing_slugs = {
        row[0]
        for row in (
            await db.execute(select(Project.slug))
        ).all()
    }
    slug = ensure_unique_slug(slugify(project.name), existing_slugs)
    new_project = Project(
        name=project.name,
        slug=slug,
        description=project.description,
        short_description=(project.description or "")[:120] or None,
        status=project_status_value(project.status),
        type=ProjectType.LEARNING,
        tags=[],
        technologies=[],
        config={},
        settings={},
        owner_id=current_user.id,
        created_at=utcnow(),
        updated_at=utcnow(),
        is_public=project.is_public,
        is_featured=False,
        total_tasks=0,
        completed_tasks=0,
        total_members=1,
        total_contributions=0,
    )
    db.add(new_project)
    await db.flush()
    await db.refresh(new_project)
    return project_to_response(new_project)


@app.put("/api/v1/projects/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    updates: ProjectUpdate,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = model_dump_compat(updates)
    if update_data.get("name") is not None:
        project.name = update_data["name"]
        existing_slugs = {
            row[0]
            for row in (
                await db.execute(select(Project.slug).where(Project.id != project.id))
            ).all()
        }
        project.slug = ensure_unique_slug(slugify(project.name), existing_slugs)
    if update_data.get("description") is not None:
        project.description = update_data["description"]
        project.short_description = (update_data["description"] or "")[:120] or None
    if update_data.get("is_public") is not None:
        project.is_public = update_data["is_public"]
    if update_data.get("status") is not None:
        project.status = project_status_value(update_data["status"])
    project.updated_at = utcnow()
    await db.flush()
    await db.refresh(project)
    return project_to_response(project)


@app.delete("/api/v1/projects/{project_id}")
async def delete_project(
    project_id: int,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(select(Project).where(Project.id == project_id, Project.owner_id == current_user.id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    await db.delete(project)
    return {"success": True, "message": "Project deleted"}


@app.get("/api/v1/system/info")
async def system_info(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    if not DB_BOOTSTRAP_OK:
        return {
            "users_count": 0,
            "projects_count": 0,
            "public_projects_count": 0,
            "agents_count": 0,
            "langchain_available": LANGCHAIN_AVAILABLE,
            "database": "unavailable",
            "database_error": DB_BOOTSTRAP_ERROR,
            "active_since": iso_now(),
        }
    users_count = (await db.execute(select(func.count()).select_from(User).where(User.is_active.is_(True)))).scalar_one()
    projects_count = (await db.execute(select(func.count()).select_from(Project))).scalar_one()
    public_projects_count = (
        await db.execute(select(func.count()).select_from(Project).where(Project.is_public.is_(True)))
    ).scalar_one()
    agents_count = (
        await db.execute(select(func.count()).select_from(UnifiedAgentRecord).where(UnifiedAgentRecord.is_deleted.is_(False)))
    ).scalar_one()
    return {
        "users_count": users_count,
        "projects_count": projects_count,
        "public_projects_count": public_projects_count,
        "agents_count": agents_count,
        "langchain_available": LANGCHAIN_AVAILABLE,
        "active_since": iso_now(),
    }


@app.get("/api/v1/system/status")
async def system_status(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    if not DB_BOOTSTRAP_OK:
        return {
            "status": "degraded",
            "timestamp": iso_now(),
            "agents": {"total": 0, "running": 0, "stopped": 0},
            "services": {
                "api": "running",
                "database": "unavailable",
                "database_error": DB_BOOTSTRAP_ERROR,
                "langchain": "integrated" if LANGCHAIN_AVAILABLE else "mock-fallback",
            },
        }
    result = await db.execute(
        select(UnifiedAgentRecord).where(UnifiedAgentRecord.is_deleted.is_(False))
    )
    agents = result.scalars().all()
    running_agents = [agent for agent in agents if agent.status == "running"]
    return {
        "status": "healthy",
        "timestamp": iso_now(),
        "agents": {
            "total": len(agents),
            "running": len(running_agents),
            "stopped": len([agent for agent in agents if agent.status == "stopped"]),
        },
        "services": {
            "api": "running",
            "database": "connected",
            "langchain": "integrated" if LANGCHAIN_AVAILABLE else "mock-fallback",
        },
    }


@app.get("/api/v1/agents", response_model=List[AgentResponse])
async def get_agents(
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> List[Dict[str, Any]]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(
        select(UnifiedAgentRecord)
        .where(
            UnifiedAgentRecord.is_deleted.is_(False),
            or_(UnifiedAgentRecord.owner_id == current_user.id, UnifiedAgentRecord.owner_id.is_(None)),
        )
        .order_by(UnifiedAgentRecord.created_at.desc())
    )
    return [agent_manager.to_response(agent) for agent in result.scalars().all()]


@app.get("/api/v1/agents/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: str,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(
        select(UnifiedAgentRecord).where(
            UnifiedAgentRecord.id == agent_id,
            UnifiedAgentRecord.is_deleted.is_(False),
        )
    )
    agent = result.scalar_one_or_none()
    if not agent or (agent.owner_id not in (None, current_user.id)):
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent_manager.to_response(agent)


@app.post("/api/v1/agents", response_model=AgentResponse)
async def create_agent(
    agent: AgentCreate,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    agent_id = f"agent_{uuid4().hex[:12]}"
    config = {
        "model": agent.model,
        "temperature": agent.temperature,
        "max_tokens": agent.max_tokens,
        "memory": agent.memory,
        "tools": agent.tools,
        "system_prompt": agent.system_prompt or "你是一个有帮助的AI助手。",
    }
    record = UnifiedAgentRecord(
        id=agent_id,
        name=agent.name,
        description=agent.description,
        type=agent.type,
        config=config,
        status="stopped",
        run_count=0,
        uptime=None,
        memory_usage=None,
        owner_id=current_user.id,
        project_id=agent.project_id,
        conversations=[],
        created_at=utcnow(),
        updated_at=utcnow(),
    )
    db.add(record)
    await db.flush()
    agent_manager.hydrate_executor(record.id, record.config)
    return agent_manager.to_response(record)


@app.put("/api/v1/agents/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: str,
    updates: AgentUpdate,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(
        select(UnifiedAgentRecord).where(
            UnifiedAgentRecord.id == agent_id,
            UnifiedAgentRecord.is_deleted.is_(False),
            UnifiedAgentRecord.owner_id == current_user.id,
        )
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    update_data = {key: value for key, value in model_dump_compat(updates).items() if value is not None}
    for field in ["name", "description", "type", "project_id"]:
        if field in update_data:
            setattr(agent, field, update_data[field])

    config_updates = {
        key: update_data[key]
        for key in ["model", "temperature", "max_tokens", "memory", "tools", "system_prompt"]
        if key in update_data
    }
    if config_updates:
        current_config = dict(agent.config or {})
        current_config.update(config_updates)
        agent.config = current_config
        agent_manager.hydrate_executor(agent.id, agent.config)

    agent.updated_at = utcnow()
    await db.flush()
    return agent_manager.to_response(agent)


@app.delete("/api/v1/agents/{agent_id}")
async def delete_agent(
    agent_id: str,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(
        select(UnifiedAgentRecord).where(
            UnifiedAgentRecord.id == agent_id,
            UnifiedAgentRecord.is_deleted.is_(False),
            UnifiedAgentRecord.owner_id == current_user.id,
        )
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    agent.is_deleted = True
    agent.updated_at = utcnow()
    agent_manager.remove_executor(agent.id)
    return {"success": True, "message": "Agent deleted"}


@app.post("/api/v1/agents/{agent_id}/start")
async def start_agent(
    agent_id: str,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(
        select(UnifiedAgentRecord).where(
            UnifiedAgentRecord.id == agent_id,
            UnifiedAgentRecord.is_deleted.is_(False),
            UnifiedAgentRecord.owner_id == current_user.id,
        )
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    was_running = agent.status == "running"
    agent.status = "running"
    if not was_running:
        agent.run_count += 1
        agent.uptime = f"{random.randint(1, 72)}小时"
        agent.memory_usage = f"{random.randint(128, 4096)}MB"
        agent_manager.agent_start_times[agent.id] = time.time()
    agent.updated_at = utcnow()
    return {
        "success": True,
        "message": "Agent already running" if was_running else "Agent started",
        "agent_id": agent_id,
    }


@app.post("/api/v1/agents/{agent_id}/stop")
async def stop_agent(
    agent_id: str,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(
        select(UnifiedAgentRecord).where(
            UnifiedAgentRecord.id == agent_id,
            UnifiedAgentRecord.is_deleted.is_(False),
            UnifiedAgentRecord.owner_id == current_user.id,
        )
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    was_stopped = agent.status == "stopped"
    agent.status = "stopped"
    agent.updated_at = utcnow()
    agent_manager.agent_start_times.pop(agent.id, None)
    return {
        "success": True,
        "message": "Agent already stopped" if was_stopped else "Agent stopped",
        "agent_id": agent_id,
    }


@app.post("/api/v1/agents/{agent_id}/interact", response_model=AgentInteractionResponse)
async def interact_with_agent(
    agent_id: str,
    interaction: AgentInteraction,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> AgentInteractionResponse:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(
        select(UnifiedAgentRecord).where(
            UnifiedAgentRecord.id == agent_id,
            UnifiedAgentRecord.is_deleted.is_(False),
            UnifiedAgentRecord.owner_id == current_user.id,
        )
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    if agent.status != "running":
        agent.status = "running"
        agent.run_count += 1
        agent.updated_at = utcnow()
        agent.uptime = f"{random.randint(1, 72)}小时"
        agent.memory_usage = f"{random.randint(128, 4096)}MB"

    try:
        executor = agent_manager.executors.get(agent.id)
        if executor is not None and LANGCHAIN_AVAILABLE:
            if LANGCHAIN_VERSION == "new":
                invoke_result = executor.invoke({"input": interaction.message})
                response_text = invoke_result.get("output", "没有响应")
            else:
                response_text = executor.run(input=interaction.message)
        else:
            response_text = agent_manager._fallback_response(agent, interaction.message)
    except Exception:
        response_text = (
            f"{agent_manager._fallback_response(agent, interaction.message)}\n\n"
            "附加说明：真实模型调用失败，已自动降级为模拟模式。"
        )

    history = list(agent.conversations or [])
    history.append(
        {
            "timestamp": iso_now(),
            "user": interaction.message,
            "agent": response_text,
            "intermediate_steps": [],
        }
    )
    agent.conversations = history
    agent.updated_at = utcnow()

    return AgentInteractionResponse(
        success=True,
        response=response_text,
        conversation_id=len(history) - 1,
    )


@app.get("/api/v1/agents/{agent_id}/conversations")
async def get_agent_conversations(
    agent_id: str,
    limit: int = 10,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> List[Dict[str, Any]]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(
        select(UnifiedAgentRecord).where(
            UnifiedAgentRecord.id == agent_id,
            UnifiedAgentRecord.is_deleted.is_(False),
            UnifiedAgentRecord.owner_id == current_user.id,
        )
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return list(agent.conversations or [])[-limit:]


@app.delete("/api/v1/agents/{agent_id}/conversations")
async def clear_agent_conversations(
    agent_id: str,
    authorization: Optional[str] = Header(default=None),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    ensure_database_ready()
    current_user = await get_current_user_record(authorization, db)
    result = await db.execute(
        select(UnifiedAgentRecord).where(
            UnifiedAgentRecord.id == agent_id,
            UnifiedAgentRecord.is_deleted.is_(False),
            UnifiedAgentRecord.owner_id == current_user.id,
        )
    )
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    agent.conversations = []
    agent.updated_at = utcnow()
    return {"success": True, "message": "Conversation history cleared"}


if __name__ == "__main__":
    print("启动统一版后端服务器...")
    print("API地址: http://localhost:8005")
    print("API文档: http://localhost:8005/docs")
    print("健康检查: http://localhost:8005/health")
    print("测试用户: testuser / testpass")
    print(f"LangChain模式: {'可用' if LANGCHAIN_AVAILABLE else '模拟降级'} ({LANGCHAIN_VERSION})")
    uvicorn.run("start_unified:app", host="0.0.0.0", port=8005, reload=True)
