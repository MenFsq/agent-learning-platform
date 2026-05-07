"""
记忆服务
实现triple-memory技能的核心功能
"""

import json
import uuid
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

from ..models.memory import MemoryItem, MemorySession


class MemoryService:
    """记忆服务类"""
    
    def __init__(self):
        """初始化记忆服务"""
        self.categories = {
            "technical": "技术知识",
            "project": "项目信息", 
            "preference": "用户偏好",
            "decision": "决策记录",
            "learning": "学习内容",
            "conversation": "对话历史",
            "task": "任务信息",
            "general": "通用信息"
        }
    
    def check_health(self) -> Dict[str, Any]:
        """检查记忆系统健康状态"""
        return {
            "status": "operational",
            "categories": len(self.categories),
            "timestamp": datetime.now().isoformat(),
            "features": [
                "memory_storage",
                "semantic_search", 
                "session_context",
                "learning_extraction",
                "export_capabilities"
            ]
        }
    
    def create_memory_item(
        self,
        content: str,
        category: str = "general",
        tags: List[str] = None,
        importance: int = 1,
        metadata: Dict[str, Any] = None,
        db: Session = None
    ) -> MemoryItem:
        """创建新的记忆项"""
        if tags is None:
            tags = []
        if metadata is None:
            metadata = {}
        
        # 计算内容哈希作为ID
        content_hash = hashlib.md5(content.encode()).hexdigest()
        memory_id = f"memory_{content_hash[:16]}"
        
        # 计算相关性分数（简单实现）
        relevance_score = min(importance / 10.0 + len(content) / 10000.0, 1.0)
        
        memory_item = MemoryItem(
            id=memory_id,
            content=content,
            category=category,
            tags=json.dumps(tags, ensure_ascii=False),
            importance=importance,
            relevance_score=relevance_score,
            metadata=json.dumps(metadata, ensure_ascii=False),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        if db:
            db.add(memory_item)
            db.commit()
            db.refresh(memory_item)
        
        return memory_item
    
    def query_memories(
        self,
        query_text: str,
        limit: int = 10,
        min_relevance: float = 0.3,
        categories: List[str] = None,
        db: Session = None
    ) -> List[MemoryItem]:
        """查询相关记忆（简单语义搜索）"""
        if not db:
            return []
        
        query = db.query(MemoryItem).filter(
            MemoryItem.relevance_score >= min_relevance
        )
        
        # 简单的关键词匹配
        if query_text:
            query = query.filter(
                MemoryItem.content.contains(query_text) |
                MemoryItem.tags.contains(query_text)
            )
        
        # 分类过滤
        if categories:
            query = query.filter(MemoryItem.category.in_(categories))
        
        # 按相关性和重要性排序
        memories = query.order_by(
            desc(MemoryItem.relevance_score),
            desc(MemoryItem.importance),
            desc(MemoryItem.updated_at)
        ).limit(limit).all()
        
        return memories
    
    def get_memory_item(self, item_id: str, db: Session) -> Optional[MemoryItem]:
        """获取特定记忆项"""
        return db.query(MemoryItem).filter(MemoryItem.id == item_id).first()
    
    def delete_memory_item(self, item_id: str, db: Session) -> bool:
        """删除记忆项"""
        memory = db.query(MemoryItem).filter(MemoryItem.id == item_id).first()
        if not memory:
            return False
        
        db.delete(memory)
        db.commit()
        return True
    
    def create_memory_session(
        self,
        session_id: str,
        context: Dict[str, Any] = None,
        agent_id: str = None,
        db: Session = None
    ) -> MemorySession:
        """创建记忆会话"""
        if context is None:
            context = {}
        
        memory_session = MemorySession(
            session_id=session_id,
            agent_id=agent_id,
            context=json.dumps(context, ensure_ascii=False),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        if db:
            db.add(memory_session)
            db.commit()
            db.refresh(memory_session)
        
        return memory_session
    
    def get_session_context(self, session_id: str, db: Session) -> Optional[Dict[str, Any]]:
        """获取会话上下文"""
        session = db.query(MemorySession).filter(
            MemorySession.session_id == session_id
        ).first()
        
        if not session or not session.context:
            return None
        
        return json.loads(session.context)
    
    def update_session_context(
        self,
        session_id: str,
        context_updates: Dict[str, Any],
        db: Session
    ) -> bool:
        """更新会话上下文"""
        session = db.query(MemorySession).filter(
            MemorySession.session_id == session_id
        ).first()
        
        if not session:
            return False
        
        # 合并上下文
        current_context = json.loads(session.context) if session.context else {}
        current_context.update(context_updates)
        
        session.context = json.dumps(current_context, ensure_ascii=False)
        session.updated_at = datetime.now()
        
        db.commit()
        return True
    
    def analyze_memories(self, db: Session) -> Dict[str, Any]:
        """分析记忆系统状态"""
        # 统计总数
        total_items = db.query(func.count(MemoryItem.id)).scalar() or 0
        
        # 分类统计
        category_stats = db.query(
            MemoryItem.category,
            func.count(MemoryItem.id).label('count')
        ).group_by(MemoryItem.category).all()
        
        categories = {cat: cnt for cat, cnt in category_stats}
        
        # 热门标签
        tag_items = db.query(MemoryItem.tags).filter(
            MemoryItem.tags.isnot(None)
        ).all()
        
        tag_counts = {}
        for item in tag_items:
            if item.tags:
                try:
                    tags = json.loads(item.tags)
                    for tag in tags:
                        tag_counts[tag] = tag_counts.get(tag, 0) + 1
                except:
                    continue
        
        top_tags = [
            {"tag": tag, "count": count}
            for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        ]
        
        # 最近活动
        recent_items = db.query(MemoryItem).order_by(
            desc(MemoryItem.updated_at)
        ).limit(5).all()
        
        recent_activity = [
            {
                "id": item.id,
                "content_preview": item.content[:50] + "..." if len(item.content) > 50 else item.content,
                "category": item.category,
                "updated_at": item.updated_at.isoformat()
            }
            for item in recent_items
        ]
        
        # 记忆健康度
        memory_health = {
            "total_items": total_items,
            "avg_importance": db.query(func.avg(MemoryItem.importance)).scalar() or 0,
            "recent_activity_count": db.query(func.count(MemoryItem.id)).filter(
                MemoryItem.updated_at >= datetime.now() - timedelta(days=7)
            ).scalar() or 0,
            "category_diversity": len(categories),
            "tag_coverage": len(tag_counts)
        }
        
        return {
            "total_items": total_items,
            "categories": categories,
            "top_tags": top_tags,
            "recent_activity": recent_activity,
            "memory_health": memory_health
        }
    
    def learn_from_conversation(
        self,
        conversation: Dict[str, Any],
        db: Session
    ) -> List[MemoryItem]:
        """从对话中学习并提取记忆"""
        learned_items = []
        
        # 提取对话中的关键信息
        messages = conversation.get("messages", [])
        participants = conversation.get("participants", [])
        topic = conversation.get("topic", "general")
        
        # 从消息中提取学习点
        for i, message in enumerate(messages):
            if i % 3 == 0:  # 每3条消息提取一个学习点
                content = message.get("content", "")
                if len(content) > 20:  # 只处理有实质内容的消息
                    # 简单的内容分析
                    if any(keyword in content.lower() for keyword in ["learn", "understand", "know", "remember"]):
                        category = "learning"
                    elif any(keyword in content.lower() for keyword in ["like", "prefer", "want", "need"]):
                        category = "preference"
                    elif any(keyword in content.lower() for keyword in ["decide", "choose", "select", "option"]):
                        category = "decision"
                    else:
                        category = "conversation"
                    
                    # 创建记忆项
                    memory_item = self.create_memory_item(
                        content=f"From conversation about '{topic}': {content[:200]}...",
                        category=category,
                        tags=[topic] + participants,
                        importance=2,  # 对话记忆的重要性中等
                        metadata={
                            "conversation_index": i,
                            "participants": participants,
                            "topic": topic,
                            "extracted_at": datetime.now().isoformat()
                        },
                        db=db
                    )
                    
                    learned_items.append(memory_item)
        
        return learned_items
    
    def export_memories_json(self, db: Session) -> Dict[str, Any]:
        """以JSON格式导出记忆数据"""
        memories = db.query(MemoryItem).all()
        sessions = db.query(MemorySession).all()
        
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "total_memories": len(memories),
            "total_sessions": len(sessions),
            "memories": [],
            "sessions": []
        }
        
        # 导出记忆项
        for memory in memories:
            export_data["memories"].append({
                "id": memory.id,
                "content": memory.content,
                "category": memory.category,
                "tags": json.loads(memory.tags) if memory.tags else [],
                "importance": memory.importance,
                "relevance_score": memory.relevance_score,
                "metadata": json.loads(memory.metadata) if memory.metadata else {},
                "created_at": memory.created_at.isoformat() if memory.created_at else None,
                "updated_at": memory.updated_at.isoformat() if memory.updated_at else None
            })
        
        # 导出会话
        for session in sessions:
            export_data["sessions"].append({
                "session_id": session.session_id,
                "agent_id": session.agent_id,
                "context": json.loads(session.context) if session.context else {},
                "created_at": session.created_at.isoformat() if session.created_at else None,
                "updated_at": session.updated_at.isoformat() if session.updated_at else None
            })
        
        return export_data
    
    def export_memories_markdown(self, db: Session) -> str:
        """以Markdown格式导出记忆数据"""
        memories = db.query(MemoryItem).order_by(
            desc(MemoryItem.importance),
            desc(MemoryItem.updated_at)
        ).all()
        
        markdown = f"""# 记忆系统导出报告

**导出时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**记忆总数**: {len(memories)}

## 记忆项列表

"""
        
        for memory in memories:
            tags = json.loads(memory.tags) if memory.tags else []
            tags_str = ", ".join([f"`{tag}`" for tag in tags]) if tags else "无标签"
            
            markdown += f"""### {memory.category.title()} - {memory.id}

**重要性**: {"⭐" * memory.importance}
**相关性分数**: {memory.relevance_score:.2f}
**标签**: {tags_str}
**创建时间**: {memory.created_at.strftime('%Y-%m-%d %H:%M')}
**更新时间**: {memory.updated_at.strftime('%Y-%m-%d %H:%M')}

{memory.content}

---
"""
        
        return markdown
    
    def get_context_for_agent(
        self,
        agent_id: str,
        query: str = None,
        db: Session = None
    ) -> Dict[str, Any]:
        """为特定Agent获取相关上下文"""
        if not db:
            return {}
        
        # 获取Agent相关的会话
        sessions = db.query(MemorySession).filter(
            MemorySession.agent_id == agent_id
        ).order_by(desc(MemorySession.updated_at)).limit(3).all()
        
        # 获取相关记忆
        related_memories = []
        if query:
            related_memories = self.query_memories(query, limit=5, db=db)
        
        # 构建上下文
        context = {
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "recent_sessions": [],
            "related_memories": []
        }
        
        # 添加会话信息
        for session in sessions:
            context["recent_sessions"].append({
                "session_id": session.session_id,
                "context_preview": json.loads(session.context)[:100] + "..." if session.context else "无上下文",
                "updated_at": session.updated_at.isoformat() if session.updated_at else None
            })
        
        # 添加相关记忆
        for memory in related_memories:
            context["related_memories"].append({
                "id": memory.id,
                "content_preview": memory.content[:100] + "..." if len(memory.content) > 100 else memory.content,
                "category": memory.category,
                "relevance_score": memory.relevance_score
            })
        
        return context