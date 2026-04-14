"""
项目管理API模块
提供项目相关的CRUD操作和项目管理功能
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Depends, Query

router = APIRouter(prefix="/projects", tags=["projects"])


# 数据模型
class ProjectBase(BaseModel):
    """项目基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="项目名称")
    description: Optional[str] = Field(None, max_length=500, description="项目描述")
    status: str = Field("planning", description="项目状态: planning, active, completed, archived")
    tags: List[str] = Field(default_factory=list, description="项目标签")
    priority: int = Field(1, ge=1, le=5, description="优先级 (1-5)")
    estimated_hours: Optional[int] = Field(None, ge=0, description="预估工时")
    start_date: Optional[datetime] = Field(None, description="开始日期")
    due_date: Optional[datetime] = Field(None, description="截止日期")


class ProjectCreate(ProjectBase):
    """创建项目模型"""
    pass


class ProjectUpdate(BaseModel):
    """更新项目模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="项目名称")
    description: Optional[str] = Field(None, max_length=500, description="项目描述")
    status: Optional[str] = Field(None, description="项目状态")
    tags: Optional[List[str]] = Field(None, description="项目标签")
    priority: Optional[int] = Field(None, ge=1, le=5, description="优先级")
    estimated_hours: Optional[int] = Field(None, ge=0, description="预估工时")
    due_date: Optional[datetime] = Field(None, description="截止日期")


class Project(ProjectBase):
    """项目完整模型"""
    id: str = Field(..., description="项目ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    owner_id: str = Field(..., description="创建者ID")
    progress: float = Field(0.0, ge=0.0, le=100.0, description="进度百分比")
    member_count: int = Field(0, ge=0, description="成员数量")
    task_count: int = Field(0, ge=0, description="任务数量")
    completed_task_count: int = Field(0, ge=0, description="已完成任务数量")


class ProjectListResponse(BaseModel):
    """项目列表响应"""
    projects: List[Project]
    total: int
    page: int
    page_size: int
    total_pages: int


class ProjectStats(BaseModel):
    """项目统计信息"""
    total_projects: int
    active_projects: int
    completed_projects: int
    total_tasks: int
    completed_tasks: int
    total_members: int
    average_progress: float


# 模拟数据库
projects_db = {
    "1": Project(
        id="1",
        name="Agent Learning Platform",
        description="一站式AI Agent学习、开发和部署平台",
        status="active",
        tags=["ai", "learning", "platform", "vue", "fastapi"],
        priority=1,
        estimated_hours=120,
        start_date=datetime(2026, 4, 1),
        due_date=datetime(2026, 6, 30),
        created_at=datetime(2026, 4, 1),
        updated_at=datetime(2026, 4, 14),
        owner_id="user_001",
        progress=65.5,
        member_count=3,
        task_count=24,
        completed_task_count=16
    ),
    "2": Project(
        id="2",
        name="代码审查 Agent",
        description="自动化代码审查和质量分析工具",
        status="active",
        tags=["code-review", "automation", "quality"],
        priority=2,
        estimated_hours=80,
        start_date=datetime(2026, 3, 15),
        due_date=datetime(2026, 5, 31),
        created_at=datetime(2026, 3, 15),
        updated_at=datetime(2026, 4, 13),
        owner_id="user_001",
        progress=61.0,
        member_count=2,
        task_count=18,
        completed_task_count=11
    ),
    "3": Project(
        id="3",
        name="PromptOps 控制台",
        description="提示词版本管理和实验平台",
        status="completed",
        tags=["prompt-engineering", "experimentation", "dashboard"],
        priority=3,
        estimated_hours=60,
        start_date=datetime(2026, 2, 1),
        due_date=datetime(2026, 3, 31),
        created_at=datetime(2026, 2, 1),
        updated_at=datetime(2026, 3, 31),
        owner_id="user_002",
        progress=100.0,
        member_count=3,
        task_count=15,
        completed_task_count=15
    ),
    "4": Project(
        id="4",
        name="多 Agent 协作实验",
        description="验证多角色Agent协作效率提升模型",
        status="planning",
        tags=["multi-agent", "collaboration", "research"],
        priority=4,
        estimated_hours=100,
        start_date=None,
        due_date=datetime(2026, 8, 31),
        created_at=datetime(2026, 4, 10),
        updated_at=datetime(2026, 4, 10),
        owner_id="user_003",
        progress=47.0,
        member_count=1,
        task_count=8,
        completed_task_count=4
    )
}


@router.get("/", response_model=ProjectListResponse)
async def get_projects(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="按状态筛选"),
    tag: Optional[str] = Query(None, description="按标签筛选"),
    search: Optional[str] = Query(None, description="搜索项目名称或描述")
):
    """
    获取项目列表
    
    支持分页、筛选和搜索功能
    """
    # 筛选项目
    filtered_projects = list(projects_db.values())
    
    if status:
        filtered_projects = [p for p in filtered_projects if p.status == status]
    
    if tag:
        filtered_projects = [p for p in filtered_projects if tag in p.tags]
    
    if search:
        search_lower = search.lower()
        filtered_projects = [
            p for p in filtered_projects
            if search_lower in p.name.lower() or 
               (p.description and search_lower in p.description.lower())
        ]
    
    # 分页
    total = len(filtered_projects)
    total_pages = (total + page_size - 1) // page_size
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    paginated_projects = filtered_projects[start_idx:end_idx]
    
    return ProjectListResponse(
        projects=paginated_projects,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str):
    """
    获取单个项目详情
    """
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    return projects_db[project_id]


@router.post("/", response_model=Project)
async def create_project(project: ProjectCreate):
    """
    创建新项目
    """
    # 生成项目ID
    new_id = str(len(projects_db) + 1)
    
    # 创建项目对象
    new_project = Project(
        id=new_id,
        **project.dict(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        owner_id="current_user",  # 实际应用中从认证信息获取
        progress=0.0,
        member_count=1,
        task_count=0,
        completed_task_count=0
    )
    
    # 保存到数据库
    projects_db[new_id] = new_project
    
    return new_project


@router.put("/{project_id}", response_model=Project)
async def update_project(project_id: str, project_update: ProjectUpdate):
    """
    更新项目信息
    """
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    # 获取现有项目
    existing_project = projects_db[project_id]
    
    # 更新字段
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(existing_project, field, value)
    
    # 更新更新时间
    existing_project.updated_at = datetime.now()
    
    # 重新计算进度（如果有任务数量变化）
    if existing_project.task_count > 0:
        existing_project.progress = (
            existing_project.completed_task_count / existing_project.task_count * 100
        )
    
    return existing_project


@router.delete("/{project_id}")
async def delete_project(project_id: str):
    """
    删除项目
    """
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    del projects_db[project_id]
    
    return {"message": "项目删除成功", "project_id": project_id}


@router.get("/{project_id}/stats")
async def get_project_stats(project_id: str):
    """
    获取项目统计信息
    """
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    project = projects_db[project_id]
    
    return {
        "project_id": project_id,
        "name": project.name,
        "progress": project.progress,
        "task_stats": {
            "total": project.task_count,
            "completed": project.completed_task_count,
            "pending": project.task_count - project.completed_task_count,
            "completion_rate": (
                project.completed_task_count / project.task_count * 100
                if project.task_count > 0 else 0
            )
        },
        "member_count": project.member_count,
        "days_remaining": (
            (project.due_date - datetime.now()).days
            if project.due_date else None
        ),
        "status": project.status,
        "priority": project.priority
    }


@router.get("/stats/overview", response_model=ProjectStats)
async def get_overview_stats():
    """
    获取所有项目概览统计
    """
    projects = list(projects_db.values())
    
    total_projects = len(projects)
    active_projects = len([p for p in projects if p.status == "active"])
    completed_projects = len([p for p in projects if p.status == "completed"])
    
    total_tasks = sum(p.task_count for p in projects)
    completed_tasks = sum(p.completed_task_count for p in projects)
    total_members = sum(p.member_count for p in projects)
    
    average_progress = (
        sum(p.progress for p in projects) / total_projects
        if total_projects > 0 else 0
    )
    
    return ProjectStats(
        total_projects=total_projects,
        active_projects=active_projects,
        completed_projects=completed_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        total_members=total_members,
        average_progress=average_progress
    )


@router.post("/{project_id}/tasks")
async def create_project_task(
    project_id: str,
    title: str,
    description: Optional[str] = None,
    assignee_id: Optional[str] = None,
    estimated_hours: Optional[int] = None,
    priority: int = 3
):
    """
    为项目创建任务
    """
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    project = projects_db[project_id]
    
    # 更新项目任务统计
    project.task_count += 1
    project.updated_at = datetime.now()
    
    # 重新计算进度
    if project.task_count > 0:
        project.progress = (
            project.completed_task_count / project.task_count * 100
        )
    
    return {
        "message": "任务创建成功",
        "project_id": project_id,
        "task": {
            "title": title,
            "description": description,
            "assignee_id": assignee_id,
            "estimated_hours": estimated_hours,
            "priority": priority,
            "status": "todo",
            "created_at": datetime.now().isoformat()
        }
    }


@router.put("/{project_id}/tasks/{task_id}/complete")
async def complete_project_task(project_id: str, task_id: str):
    """
    标记项目任务为完成
    """
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="项目不存在")
    
    project = projects_db[project_id]
    
    # 更新项目任务统计
    project.completed_task_count += 1
    project.updated_at = datetime.now()
    
    # 重新计算进度
    if project.task_count > 0:
        project.progress = (
            project.completed_task_count / project.task_count * 100
        )
    
    return {
        "message": "任务标记为完成",
        "project_id": project_id,
        "task_id": task_id,
        "completed_at": datetime.now().isoformat()
    }