"""
项目服务层
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_, func, case
from sqlalchemy.orm import selectinload
from loguru import logger

from ..models.project import Project, ProjectMember, ProjectTask, ProjectStatus, ProjectType
from ..models.user import User
from ..schemas.project import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectMemberCreate,
    ProjectTaskCreate,
    ProjectTaskUpdate
)


class ProjectService:
    """项目服务类"""
    
    @staticmethod
    async def create_project(
        db: AsyncSession,
        project_data: ProjectCreate,
        owner_id: int
    ) -> Project:
        """
        创建新项目
        """
        try:
            # 检查项目slug是否已存在
            existing_project = await db.execute(
                select(Project).where(Project.slug == project_data.slug)
            )
            if existing_project.scalar_one_or_none():
                raise ValueError("Project slug already exists")
            
            # 创建项目
            project = Project(
                name=project_data.name,
                slug=project_data.slug,
                description=project_data.description,
                short_description=project_data.short_description,
                status=ProjectStatus.DRAFT,
                type=project_data.type or ProjectType.LEARNING,
                tags=project_data.tags or [],
                technologies=project_data.technologies or [],
                config=project_data.config or {},
                settings=project_data.settings or {},
                owner_id=owner_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_public=project_data.is_public or False,
                is_featured=False,
                total_tasks=0,
                completed_tasks=0,
                total_members=1,
                total_contributions=0
            )
            
            db.add(project)
            await db.commit()
            await db.refresh(project)
            
            # 创建项目所有者成员记录
            owner_member = ProjectMember(
                project_id=project.id,
                user_id=owner_id,
                role="owner",
                permissions=["*"],  # 所有权限
                joined_at=datetime.utcnow(),
                is_active=True,
                is_accepted=True
            )
            
            db.add(owner_member)
            await db.commit()
            
            logger.info(f"Project created: {project.name} (ID: {project.id})")
            return project
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create project: {e}")
            raise
    
    @staticmethod
    async def get_project_by_id(
        db: AsyncSession,
        project_id: int
    ) -> Optional[Project]:
        """
        通过ID获取项目
        """
        try:
            result = await db.execute(
                select(Project)
                .options(selectinload(Project.owner))
                .where(Project.id == project_id)
            )
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"Failed to get project by ID: {e}")
            raise
    
    @staticmethod
    async def get_project_by_slug(
        db: AsyncSession,
        slug: str
    ) -> Optional[Project]:
        """
        通过slug获取项目
        """
        try:
            result = await db.execute(
                select(Project)
                .options(selectinload(Project.owner))
                .where(Project.slug == slug)
            )
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"Failed to get project by slug: {e}")
            raise
    
    @staticmethod
    async def update_project(
        db: AsyncSession,
        project_id: int,
        update_data: ProjectUpdate
    ) -> Optional[Project]:
        """
        更新项目信息
        """
        try:
            # 获取项目
            project = await ProjectService.get_project_by_id(db, project_id)
            if not project:
                return None
            
            # 更新字段
            update_dict = update_data.dict(exclude_unset=True)
            
            # 如果更新slug，需要检查是否已存在
            if "slug" in update_dict and update_dict["slug"] != project.slug:
                existing_project = await db.execute(
                    select(Project).where(Project.slug == update_dict["slug"])
                )
                if existing_project.scalar_one_or_none():
                    raise ValueError("Project slug already exists")
            
            # 移除不允许直接更新的字段
            for field in ["id", "created_at", "owner_id"]:
                update_dict.pop(field, None)
            
            # 更新项目
            await db.execute(
                update(Project)
                .where(Project.id == project_id)
                .values(**update_dict, updated_at=datetime.utcnow())
            )
            await db.commit()
            
            # 重新获取项目
            project = await ProjectService.get_project_by_id(db, project_id)
            logger.info(f"Project updated: {project.name} (ID: {project.id})")
            
            return project
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to update project: {e}")
            raise
    
    @staticmethod
    async def delete_project(
        db: AsyncSession,
        project_id: int
    ) -> bool:
        """
        删除项目
        """
        try:
            # 获取项目
            project = await ProjectService.get_project_by_id(db, project_id)
            if not project:
                return False
            
            # 删除项目
            await db.execute(
                delete(Project).where(Project.id == project_id)
            )
            await db.commit()
            
            logger.info(f"Project deleted: {project.name} (ID: {project.id})")
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to delete project: {e}")
            raise
    
    @staticmethod
    async def list_projects(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        status: Optional[ProjectStatus] = None,
        type: Optional[ProjectType] = None,
        is_public: Optional[bool] = None,
        owner_id: Optional[int] = None
    ) -> List[Project]:
        """
        列出项目
        """
        try:
            query = select(Project).options(selectinload(Project.owner))
            
            # 添加过滤条件
            if status is not None:
                query = query.where(Project.status == status)
            
            if type is not None:
                query = query.where(Project.type == type)
            
            if is_public is not None:
                query = query.where(Project.is_public == is_public)
            
            if owner_id is not None:
                query = query.where(Project.owner_id == owner_id)
            
            # 添加分页
            query = query.offset(skip).limit(limit).order_by(Project.created_at.desc())
            
            result = await db.execute(query)
            projects = result.scalars().all()
            
            return projects
            
        except Exception as e:
            logger.error(f"Failed to list projects: {e}")
            raise
    
    @staticmethod
    async def search_projects(
        db: AsyncSession,
        query: str,
        skip: int = 0,
        limit: int = 50
    ) -> List[Project]:
        """
        搜索项目
        """
        try:
            search_query = select(Project).options(selectinload(Project.owner)).where(
                or_(
                    Project.name.ilike(f"%{query}%"),
                    Project.description.ilike(f"%{query}%"),
                    Project.short_description.ilike(f"%{query}%")
                )
            )
            
            search_query = search_query.offset(skip).limit(limit).order_by(Project.created_at.desc())
            
            result = await db.execute(search_query)
            projects = result.scalars().all()
            
            return projects
            
        except Exception as e:
            logger.error(f"Failed to search projects: {e}")
            raise
    
    @staticmethod
    async def get_user_projects(
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Project]:
        """
        获取用户参与的项目
        """
        try:
            # 获取用户作为成员的项目
            query = select(Project).join(ProjectMember).where(
                and_(
                    ProjectMember.user_id == user_id,
                    ProjectMember.is_active == True,
                    ProjectMember.is_accepted == True
                )
            ).options(selectinload(Project.owner))
            
            query = query.offset(skip).limit(limit).order_by(Project.created_at.desc())
            
            result = await db.execute(query)
            projects = result.scalars().all()
            
            return projects
            
        except Exception as e:
            logger.error(f"Failed to get user projects: {e}")
            raise
    
    @staticmethod
    async def add_project_member(
        db: AsyncSession,
        project_id: int,
        member_data: ProjectMemberCreate,
        invited_by: int
    ) -> ProjectMember:
        """
        添加项目成员
        """
        try:
            # 检查项目是否存在
            project = await ProjectService.get_project_by_id(db, project_id)
            if not project:
                raise ValueError("Project not found")
            
            # 检查用户是否存在
            user = await db.execute(
                select(User).where(User.id == member_data.user_id)
            )
            user = user.scalar_one_or_none()
            
            if not user:
                raise ValueError("User not found")
            
            # 检查用户是否已经是项目成员
            existing_member = await db.execute(
                select(ProjectMember).where(
                    and_(
                        ProjectMember.project_id == project_id,
                        ProjectMember.user_id == member_data.user_id
                    )
                )
            )
            existing_member = existing_member.scalar_one_or_none()
            
            if existing_member:
                # 如果成员已存在但被禁用，重新激活
                if not existing_member.is_active:
                    existing_member.is_active = True
                    existing_member.is_accepted = False  # 需要重新接受邀请
                    existing_member.invited_by = invited_by
                    await db.commit()
                    await db.refresh(existing_member)
                    return existing_member
                else:
                    raise ValueError("User is already a project member")
            
            # 创建成员记录
            member = ProjectMember(
                project_id=project_id,
                user_id=member_data.user_id,
                role=member_data.role or "member",
                permissions=member_data.permissions or [],
                joined_at=datetime.utcnow(),
                invited_by=invited_by,
                invitation_token=member_data.invitation_token,
                is_active=True,
                is_accepted=member_data.is_accepted or False
            )
            
            db.add(member)
            
            # 更新项目成员计数
            project.total_members += 1
            await db.commit()
            await db.refresh(member)
            
            logger.info(f"Project member added: user_id={member_data.user_id}, project_id={project_id}")
            return member
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to add project member: {e}")
            raise
    
    @staticmethod
    async def remove_project_member(
        db: AsyncSession,
        project_id: int,
        user_id: int
    ) -> bool:
        """
        移除项目成员
        """
        try:
            # 检查成员是否存在
            member = await db.execute(
                select(ProjectMember).where(
                    and_(
                        ProjectMember.project_id == project_id,
                        ProjectMember.user_id == user_id
                    )
                )
            )
            member = member.scalar_one_or_none()
            
            if not member:
                return False
            
            # 如果是项目所有者，不能移除
            if member.role == "owner":
                raise ValueError("Cannot remove project owner")
            
            # 移除成员
            await db.execute(
                delete(ProjectMember).where(
                    and_(
                        ProjectMember.project_id == project_id,
                        ProjectMember.user_id == user_id
                    )
                )
            )
            
            # 更新项目成员计数
            project = await ProjectService.get_project_by_id(db, project_id)
            if project:
                project.total_members = max(0, project.total_members - 1)
            
            await db.commit()
            
            logger.info(f"Project member removed: user_id={user_id}, project_id={project_id}")
            return True
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to remove project member: {e}")
            raise
    
    @staticmethod
    async def create_project_task(
        db: AsyncSession,
        project_id: int,
        task_data: ProjectTaskCreate,
        created_by: int
    ) -> ProjectTask:
        """
        创建项目任务
        """
        try:
            # 检查项目是否存在
            project = await ProjectService.get_project_by_id(db, project_id)
            if not project:
                raise ValueError("Project not found")
            
            # 创建任务
            task = ProjectTask(
                project_id=project_id,
                title=task_data.title,
                description=task_data.description,
                status=task_data.status or "todo",
                priority=task_data.priority or "medium",
                assigned_to=task_data.assigned_to,
                created_by=created_by,
                due_date=task_data.due_date,
                estimated_hours=task_data.estimated_hours,
                actual_hours=0,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                tags=task_data.tags or [],
                category=task_data.category
            )
            
            db.add(task)
            
            # 更新项目任务计数
            project.total_tasks += 1
            await db.commit()
            await db.refresh(task)
            
            logger.info(f"Project task created: {task.title} (ID: {task.id})")
            return task
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to create project task: {e}")
            raise
    
    @staticmethod
    async def update_project_task(
        db: AsyncSession,
        task_id: int,
        update_data: ProjectTaskUpdate
    ) -> Optional[ProjectTask]:
        """
        更新项目任务
        """
        try:
            # 获取任务
            task = await db.execute(
                select(ProjectTask).where(ProjectTask.id == task_id)
            )
            task = task.scalar_one_or_none()
            
            if not task:
                return None
            
            # 更新字段
            update_dict = update_data.dict(exclude_unset=True)
            
            # 检查状态变化
            old_status = task.status
            new_status = update_dict.get("status", old_status)
            
            # 移除不允许直接更新的字段
            for field in ["id", "created_at", "project_id", "created_by"]:
                update_dict.pop(field, None)
            
            # 更新任务
            await db.execute(
                update(ProjectTask)
                .where(ProjectTask.id == task_id)
                .values(**update_dict, updated_at=datetime.utcnow())
            )
            
            # 如果状态从非完成变为完成，更新项目完成计数
            if old_status != "done" and new_status == "done":
                project = await ProjectService.get_project_by_id(db, task.project_id)
                if project:
                    project.completed_tasks += 1
                    project.total_contributions += 1
            
            # 如果状态从完成变为非完成，更新项目完成计数
            elif old_status == "done" and new_status != "done":
                project = await ProjectService.get_project_by_id(db, task.project_id)
                if project:
                    project.completed_tasks = max(0, project.completed_tasks - 1)
                    project.total_contributions = max(0, project.total_contributions - 1)
            
            await db.commit()
            
            # 重新获取任务
            task = await db.execute(
                select(ProjectTask).where(ProjectTask.id == task_id)
            )
            task = task.scalar_one_or_none()
            
            logger.info(f"Project task updated: {task.title} (ID: {task.id})")
            return task
            
        except Exception as e:
            await db.rollback()
            logger.error(f"Failed to update project task: {e}")
            raise
    
    @staticmethod
    async def get_project_stats(
        db: AsyncSession,
        project_id: int
    ) -> Dict[str, Any]:
        """
        获取项目统计信息
        """
        try:
            # 获取项目
            project = await ProjectService.get_project_by_id(db, project_id)
            if not project:
                raise ValueError("Project not found")
            
            # 获取任务统计
            task_stats = await db.execute(
                select(
                    func.count(ProjectTask.id).label("total"),
                    func.sum(case((ProjectTask.status == "done", 1), else_=0)).label("completed"),
                    func.avg(ProjectTask.estimated_hours).label("avg_estimated_hours"),
                    func.sum(ProjectTask.actual_hours).label("total_actual_hours")
                ).where(ProjectTask.project_id == project_id)
            )
            task_stats = task_stats.first()
            
            # 获取成员统计
            member_stats = await db.execute(
                select(
                    func.count(ProjectMember.id).label("total"),
                    func.sum(case((ProjectMember.role == "owner", 1), else_=0)).label("owners"),
                    func.sum(case((ProjectMember.role == "admin", 1), else_=0)).label("admins")
                ).where(
                    and_(
                        ProjectMember.project_id == project_id,
                        ProjectMember.is_active == True,
                        ProjectMember.is_accepted == True
                    )
                )
            )
            member_stats = member_stats.first()
            
            return {
                "project": {
                    "id": project.id,
                    "name": project.name,
                    "status": project.status,
                    "type": project.type
                },
                "tasks": {
                    "total": task_stats.total or 0,
                    "completed": task_stats.completed or 0,
                    "completion_rate": (task_stats.completed or 0) / max(task_stats.total or 1, 1) * 100,
                    "avg_estimated_hours": float(task_stats.avg_estimated_hours or 0),
                    "total_actual_hours": task_stats.total_actual_hours or 0
                },
                "members": {
                    "total": member_stats.total or 0,
                    "owners": member_stats.owners or 0,
                    "admins": member_stats.admins or 0,
                    "regular_members": (member_stats.total or 0) - (member_stats.owners or 0) - (member_stats.admins or 0)
                },
                "overall": {
                    "total_contributions": project.total_contributions,
                    "created_at": project.created_at.isoformat() if project.created_at else None,
                    "updated_at": project.updated_at.isoformat() if project.updated_at else None
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get project stats: {e}")
            raise