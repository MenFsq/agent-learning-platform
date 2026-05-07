"""
记忆管理API模块
集成triple-memory技能，提供智能记忆管理功能
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...models.memory import MemoryItem, MemorySession
from ...services.memory_service import MemoryService

router = APIRouter(prefix="/memory", tags=["memory"])


# 数据模型
class MemoryItemCreate(BaseModel):
    """创建记忆项模型"""
    content: str = Field(..., description="记忆内容")
    category: str = Field("general", description="记忆分类")
    tags: List[str] = Field(default_factory=list, description="标签")
    importance: int = Field(1, ge=1, le=10, description="重要性等级(1-10)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="元数据")


class MemoryItemResponse(BaseModel):
    """记忆项响应模型"""
    id: str
    content: str
    category: str
    tags: List[str]
    importance: int
    relevance_score: float
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]


class MemoryQuery(BaseModel):
    """记忆查询模型"""
    query: str = Field(..., description="查询内容")
    limit: int = Field(10, ge=1, le=100, description="返回数量限制")
    min_relevance: float = Field(0.3, ge=0.0, le=1.0, description="最小相关性分数")
    categories: Optional[List[str]] = Field(None, description="过滤分类")


class MemorySessionCreate(BaseModel):
    """创建记忆会话模型"""
    session_id: str = Field(..., description="会话ID")
    context: Dict[str, Any] = Field(default_factory=dict, description="会话上下文")
    agent_id: Optional[str] = Field(None, description="关联的Agent ID")


class MemoryAnalysis(BaseModel):
    """记忆分析结果"""
    total_items: int
    categories: Dict[str, int]
    top_tags: List[Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]
    memory_health: Dict[str, Any]


# 依赖项
def get_memory_service():
    """获取记忆服务实例"""
    return MemoryService()


@router.get("/health", response_model=Dict[str, Any])
async def memory_health_check(
    service: MemoryService = Depends(get_memory_service)
):
    """记忆系统健康检查"""
    try:
        health = service.check_health()
        return {
            "status": "healthy",
            "service": "memory-system",
            "timestamp": datetime.now(),
            "details": health
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"记忆系统检查失败: {str(e)}")


@router.post("/items", response_model=MemoryItemResponse)
async def create_memory_item(
    item: MemoryItemCreate,
    service: MemoryService = Depends(get_memory_service),
    db: Session = Depends(get_db)
):
    """创建新的记忆项"""
    try:
        memory_item = service.create_memory_item(
            content=item.content,
            category=item.category,
            tags=item.tags,
            importance=item.importance,
            metadata=item.metadata,
            db=db
        )
        
        return MemoryItemResponse(
            id=memory_item.id,
            content=memory_item.content,
            category=memory_item.category,
            tags=json.loads(memory_item.tags) if memory_item.tags else [],
            importance=memory_item.importance,
            relevance_score=memory_item.relevance_score or 0.0,
            created_at=memory_item.created_at,
            updated_at=memory_item.updated_at,
            metadata=json.loads(memory_item.metadata) if memory_item.metadata else {}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建记忆项失败: {str(e)}")


@router.post("/query", response_model=List[MemoryItemResponse])
async def query_memories(
    query: MemoryQuery,
    service: MemoryService = Depends(get_memory_service),
    db: Session = Depends(get_db)
):
    """查询相关记忆"""
    try:
        memories = service.query_memories(
            query_text=query.query,
            limit=query.limit,
            min_relevance=query.min_relevance,
            categories=query.categories,
            db=db
        )
        
        response = []
        for memory in memories:
            response.append(MemoryItemResponse(
                id=memory.id,
                content=memory.content,
                category=memory.category,
                tags=json.loads(memory.tags) if memory.tags else [],
                importance=memory.importance,
                relevance_score=memory.relevance_score or 0.0,
                created_at=memory.created_at,
                updated_at=memory.updated_at,
                metadata=json.loads(memory.metadata) if memory.metadata else {}
            ))
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询记忆失败: {str(e)}")


@router.get("/items/{item_id}", response_model=MemoryItemResponse)
async def get_memory_item(
    item_id: str,
    service: MemoryService = Depends(get_memory_service),
    db: Session = Depends(get_db)
):
    """获取特定记忆项"""
    try:
        memory = service.get_memory_item(item_id, db)
        if not memory:
            raise HTTPException(status_code=404, detail="记忆项未找到")
        
        return MemoryItemResponse(
            id=memory.id,
            content=memory.content,
            category=memory.category,
            tags=json.loads(memory.tags) if memory.tags else [],
            importance=memory.importance,
            relevance_score=memory.relevance_score or 0.0,
            created_at=memory.created_at,
            updated_at=memory.updated_at,
            metadata=json.loads(memory.metadata) if memory.metadata else {}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取记忆项失败: {str(e)}")


@router.delete("/items/{item_id}")
async def delete_memory_item(
    item_id: str,
    service: MemoryService = Depends(get_memory_service),
    db: Session = Depends(get_db)
):
    """删除记忆项"""
    try:
        success = service.delete_memory_item(item_id, db)
        if not success:
            raise HTTPException(status_code=404, detail="记忆项未找到")
        
        return {"message": "记忆项已删除", "item_id": item_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除记忆项失败: {str(e)}")


@router.post("/sessions", response_model=Dict[str, Any])
async def create_memory_session(
    session: MemorySessionCreate,
    service: MemoryService = Depends(get_memory_service),
    db: Session = Depends(get_db)
):
    """创建记忆会话"""
    try:
        memory_session = service.create_memory_session(
            session_id=session.session_id,
            context=session.context,
            agent_id=session.agent_id,
            db=db
        )
        
        return {
            "session_id": memory_session.session_id,
            "agent_id": memory_session.agent_id,
            "context": json.loads(memory_session.context) if memory_session.context else {},
            "created_at": memory_session.created_at,
            "updated_at": memory_session.updated_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建记忆会话失败: {str(e)}")


@router.get("/sessions/{session_id}/context")
async def get_session_context(
    session_id: str,
    service: MemoryService = Depends(get_memory_service),
    db: Session = Depends(get_db)
):
    """获取会话上下文"""
    try:
        context = service.get_session_context(session_id, db)
        if not context:
            raise HTTPException(status_code=404, detail="会话未找到")
        
        return {
            "session_id": session_id,
            "context": context,
            "timestamp": datetime.now()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取会话上下文失败: {str(e)}")


@router.get("/analysis", response_model=MemoryAnalysis)
async def analyze_memories(
    service: MemoryService = Depends(get_memory_service),
    db: Session = Depends(get_db)
):
    """分析记忆系统状态"""
    try:
        analysis = service.analyze_memories(db)
        
        return MemoryAnalysis(
            total_items=analysis["total_items"],
            categories=analysis["categories"],
            top_tags=analysis["top_tags"],
            recent_activity=analysis["recent_activity"],
            memory_health=analysis["memory_health"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"记忆分析失败: {str(e)}")


@router.post("/learn")
async def learn_from_conversation(
    conversation: Dict[str, Any],
    service: MemoryService = Depends(get_memory_service),
    db: Session = Depends(get_db)
):
    """从对话中学习并提取记忆"""
    try:
        learned_items = service.learn_from_conversation(conversation, db)
        
        return {
            "message": "对话学习完成",
            "learned_items": len(learned_items),
            "items": [
                {
                    "id": item.id,
                    "content": item.content[:100] + "..." if len(item.content) > 100 else item.content,
                    "category": item.category
                }
                for item in learned_items
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话学习失败: {str(e)}")


@router.get("/export")
async def export_memories(
    format: str = "json",
    service: MemoryService = Depends(get_memory_service),
    db: Session = Depends(get_db)
):
    """导出记忆数据"""
    try:
        if format == "json":
            data = service.export_memories_json(db)
            return data
        elif format == "markdown":
            data = service.export_memories_markdown(db)
            return {"content": data, "format": "markdown"}
        else:
            raise HTTPException(status_code=400, detail="不支持的导出格式")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导出记忆失败: {str(e)}")