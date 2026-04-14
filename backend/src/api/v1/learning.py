"""
学习管理API模块
提供学习路径、课程、进度跟踪等功能
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/learning", tags=["learning"])


# 数据模型
class CourseBase(BaseModel):
    """课程基础模型"""
    title: str = Field(..., min_length=1, max_length=200, description="课程标题")
    description: Optional[str] = Field(None, max_length=1000, description="课程描述")
    category: str = Field(..., description="课程分类")
    difficulty: str = Field("beginner", description="难度级别: beginner, intermediate, advanced")
    estimated_hours: int = Field(1, ge=1, description="预估学习时长(小时)")
    tags: List[str] = Field(default_factory=list, description="课程标签")
    prerequisites: List[str] = Field(default_factory=list, description="先修课程ID列表")


class CourseCreate(CourseBase):
    """创建课程模型"""
    pass


class Course(CourseBase):
    """课程完整模型"""
    id: str = Field(..., description="课程ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    instructor_id: str = Field(..., description="讲师ID")
    lesson_count: int = Field(0, ge=0, description="课时数量")
    student_count: int = Field(0, ge=0, description="学生数量")
    average_rating: float = Field(0.0, ge=0.0, le=5.0, description="平均评分")
    is_published: bool = Field(False, description="是否已发布")


class LearningPathBase(BaseModel):
    """学习路径基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="学习路径名称")
    description: Optional[str] = Field(None, max_length=500, description="学习路径描述")
    goal: str = Field(..., description="学习目标")
    target_audience: str = Field("all", description="目标受众: beginner, intermediate, advanced, all")
    estimated_completion_time: int = Field(1, ge=1, description="预估完成时间(周)")


class LearningPathCreate(LearningPathBase):
    """创建学习路径模型"""
    course_ids: List[str] = Field(default_factory=list, description="课程ID列表")


class LearningPath(LearningPathBase):
    """学习路径完整模型"""
    id: str = Field(..., description="学习路径ID")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")
    creator_id: str = Field(..., description="创建者ID")
    course_count: int = Field(0, ge=0, description="课程数量")
    enrolled_count: int = Field(0, ge=0, description="报名人数")
    completion_rate: float = Field(0.0, ge=0.0, le=100.0, description="完成率")
    courses: List[Course] = Field(default_factory=list, description="课程列表")


class UserProgress(BaseModel):
    """用户学习进度模型"""
    user_id: str = Field(..., description="用户ID")
    course_id: str = Field(..., description="课程ID")
    progress: float = Field(0.0, ge=0.0, le=100.0, description="进度百分比")
    completed_lessons: List[str] = Field(default_factory=list, description="已完成的课时ID列表")
    started_at: datetime = Field(..., description="开始学习时间")
    last_activity_at: datetime = Field(..., description="最后活动时间")
    is_completed: bool = Field(False, description="是否已完成")
    completed_at: Optional[datetime] = Field(None, description="完成时间")
    notes: Optional[str] = Field(None, description="学习笔记")


class LearningStats(BaseModel):
    """学习统计信息"""
    total_courses: int
    total_learning_paths: int
    total_enrollments: int
    active_learners: int
    average_completion_rate: float
    popular_categories: List[str]


# 模拟数据库
courses_db = {
    "1": Course(
        id="1",
        title="LangChain Agentic Patterns",
        description="深入学习LangChain中的Agent设计模式和最佳实践",
        category="Reasoning",
        difficulty="intermediate",
        estimated_hours=12,
        tags=["langchain", "agents", "patterns", "best-practices"],
        prerequisites=[],
        created_at=datetime(2026, 3, 1),
        updated_at=datetime(2026, 4, 10),
        instructor_id="instructor_001",
        lesson_count=8,
        student_count=156,
        average_rating=4.7,
        is_published=True
    ),
    "2": Course(
        id="2",
        title="RAG Pipeline In Practice",
        description="实战构建高效的检索增强生成(RAG)管道",
        category="Retrieval",
        difficulty="intermediate",
        estimated_hours=10,
        tags=["rag", "retrieval", "embeddings", "vector-db"],
        prerequisites=["1"],
        created_at=datetime(2026, 3, 15),
        updated_at=datetime(2026, 4, 12),
        instructor_id="instructor_002",
        lesson_count=6,
        student_count=89,
        average_rating=4.5,
        is_published=True
    ),
    "3": Course(
        id="3",
        title="PromptOps Deployment Basics",
        description="提示词工程部署和运维基础",
        category="Delivery",
        difficulty="beginner",
        estimated_hours=8,
        tags=["prompt-engineering", "deployment", "monitoring"],
        prerequisites=[],
        created_at=datetime(2026, 2, 20),
        updated_at=datetime(2026, 4, 5),
        instructor_id="instructor_003",
        lesson_count=5,
        student_count=203,
        average_rating=4.3,
        is_published=True
    ),
    "4": Course(
        id="4",
        title="Evaluation And Guardrails",
        description="AI系统评估和安全护栏设计",
        category="Quality",
        difficulty="advanced",
        estimated_hours=15,
        tags=["evaluation", "safety", "guardrails", "testing"],
        prerequisites=["1", "2"],
        created_at=datetime(2026, 4, 1),
        updated_at=datetime(2026, 4, 14),
        instructor_id="instructor_001",
        lesson_count=10,
        student_count=42,
        average_rating=4.8,
        is_published=True
    )
}

learning_paths_db = {
    "1": LearningPath(
        id="1",
        name="AI Agent开发全栈路径",
        description="从基础到高级的完整AI Agent开发学习路径",
        goal="掌握AI Agent开发的全栈技能，能够独立设计和部署生产级Agent系统",
        target_audience="intermediate",
        estimated_completion_time=12,
        created_at=datetime(2026, 3, 1),
        updated_at=datetime(2026, 4, 10),
        creator_id="creator_001",
        course_count=4,
        enrolled_count=124,
        completion_rate=65.5,
        courses=[courses_db["1"], courses_db["2"], courses_db["3"], courses_db["4"]]
    ),
    "2": LearningPath(
        id="2",
        name="提示词工程专家路径",
        description="专注于提示词工程和优化的学习路径",
        goal="成为提示词工程专家，能够设计和优化高效的提示词系统",
        target_audience="beginner",
        estimated_completion_time=8,
        created_at=datetime(2026, 3, 15),
        updated_at=datetime(2026, 4, 8),
        creator_id="creator_002",
        course_count=2,
        enrolled_count=87,
        completion_rate=78.2,
        courses=[courses_db["3"], courses_db["4"]]
    )
}

user_progress_db = {}


@router.get("/courses", response_model=List[Course])
async def get_courses(
    category: Optional[str] = Query(None, description="按分类筛选"),
    difficulty: Optional[str] = Query(None, description="按难度筛选"),
    tag: Optional[str] = Query(None, description="按标签筛选"),
    search: Optional[str] = Query(None, description="搜索课程标题或描述"),
    published_only: bool = Query(True, description="是否只返回已发布的课程")
):
    """
    获取课程列表
    
    支持筛选和搜索功能
    """
    filtered_courses = list(courses_db.values())
    
    if published_only:
        filtered_courses = [c for c in filtered_courses if c.is_published]
    
    if category:
        filtered_courses = [c for c in filtered_courses if c.category == category]
    
    if difficulty:
        filtered_courses = [c for c in filtered_courses if c.difficulty == difficulty]
    
    if tag:
        filtered_courses = [c for c in filtered_courses if tag in c.tags]
    
    if search:
        search_lower = search.lower()
        filtered_courses = [
            c for c in filtered_courses
            if search_lower in c.title.lower() or 
               (c.description and search_lower in c.description.lower())
        ]
    
    # 按学生数量排序（热门课程在前）
    filtered_courses.sort(key=lambda c: c.student_count, reverse=True)
    
    return filtered_courses


@router.get("/courses/{course_id}", response_model=Course)
async def get_course(course_id: str):
    """
    获取单个课程详情
    """
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    return courses_db[course_id]


@router.get("/courses/{course_id}/prerequisites")
async def get_course_prerequisites(course_id: str):
    """
    获取课程先修要求
    """
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    course = courses_db[course_id]
    prerequisites = []
    
    for prereq_id in course.prerequisites:
        if prereq_id in courses_db:
            prereq_course = courses_db[prereq_id]
            prerequisites.append({
                "id": prereq_course.id,
                "title": prereq_course.title,
                "description": prereq_course.description,
                "difficulty": prereq_course.difficulty,
                "estimated_hours": prereq_course.estimated_hours
            })
    
    return {
        "course_id": course_id,
        "course_title": course.title,
        "prerequisites": prerequisites,
        "prerequisite_count": len(prerequisites)
    }


@router.get("/paths", response_model=List[LearningPath])
async def get_learning_paths(
    target_audience: Optional[str] = Query(None, description="按目标受众筛选"),
    search: Optional[str] = Query(None, description="搜索学习路径名称或描述")
):
    """
    获取学习路径列表
    """
    filtered_paths = list(learning_paths_db.values())
    
    if target_audience:
        filtered_paths = [p for p in filtered_paths if p.target_audience == target_audience]
    
    if search:
        search_lower = search.lower()
        filtered_paths = [
            p for p in filtered_paths
            if search_lower in p.name.lower() or 
               (p.description and search_lower in p.description.lower())
        ]
    
    # 按报名人数排序（热门路径在前）
    filtered_paths.sort(key=lambda p: p.enrolled_count, reverse=True)
    
    return filtered_paths


@router.get("/paths/{path_id}", response_model=LearningPath)
async def get_learning_path(path_id: str):
    """
    获取单个学习路径详情
    """
    if path_id not in learning_paths_db:
        raise HTTPException(status_code=404, detail="学习路径不存在")
    
    return learning_paths_db[path_id]


@router.post("/paths/{path_id}/enroll")
async def enroll_learning_path(path_id: str, user_id: str = "current_user"):
    """
    报名学习路径
    """
    if path_id not in learning_paths_db:
        raise HTTPException(status_code=404, detail="学习路径不存在")
    
    path = learning_paths_db[path_id]
    
    # 更新报名人数
    path.enrolled_count += 1
    path.updated_at = datetime.now()
    
    # 为用户创建所有课程的进度记录
    for course in path.courses:
        progress_key = f"{user_id}:{course.id}"
        user_progress_db[progress_key] = UserProgress(
            user_id=user_id,
            course_id=course.id,
            progress=0.0,
            completed_lessons=[],
            started_at=datetime.now(),
            last_activity_at=datetime.now(),
            is_completed=False
        )
    
    return {
        "message": "报名成功",
        "path_id": path_id,
        "path_name": path.name,
        "user_id": user_id,
        "enrolled_at": datetime.now().isoformat(),
        "course_count": path.course_count
    }


@router.get("/users/{user_id}/progress")
async def get_user_progress(user_id: str):
    """
    获取用户学习进度
    """
    user_progress = []
    total_courses = 0
    completed_courses = 0
    total_progress = 0.0
    
    for key, progress in user_progress_db.items():
        if progress.user_id == user_id:
            user_progress.append(progress)
            total_courses += 1
            total_progress += progress.progress
            
            if progress.is_completed:
                completed_courses += 1
    
    average_progress = total_progress / total_courses if total_courses > 0 else 0
    
    return {
        "user_id": user_id,
        "total_courses": total_courses,
        "completed_courses": completed_courses,
        "in_progress_courses": total_courses - completed_courses,
        "average_progress": average_progress,
        "progress_details": user_progress
    }


@router.put("/users/{user_id}/courses/{course_id}/progress")
async def update_course_progress(
    user_id: str,
    course_id: str,
    progress: float = Field(..., ge=0.0, le=100.0, description="进度百分比"),
    completed_lesson_id: Optional[str] = None,
    notes: Optional[str] = None
):
    """
    更新课程学习进度
    """
    progress_key = f"{user_id}:{course_id}"
    
    if progress_key not in user_progress_db:
        # 创建新的进度记录
        user_progress_db[progress_key] = UserProgress(
            user_id=user_id,
            course_id=course_id,
            progress=progress,
            completed_lessons=[],
            started_at=datetime.now(),
            last_activity_at=datetime.now(),
            is_completed=False,
            notes=notes
        )
    else:
        # 更新现有进度记录
        user_progress = user_progress_db[progress_key]
        user_progress.progress = progress
        user_progress.last_activity_at = datetime.now()
        
        if notes:
            user_progress.notes = notes
        
        if completed_lesson_id and completed_lesson_id not in user_progress.completed_lessons:
            user_progress.completed_lessons.append(completed_lesson_id)
        
        # 检查是否完成课程
        if progress >= 100.0 and not user_progress.is_completed:
            user_progress.is_completed = True
            user_progress.completed_at = datetime.now()
    
    return {
        "message": "进度更新成功",
        "user_id": user_id,
        "course_id": course_id,
        "progress": progress,
        "is_completed": user_progress_db[progress_key].is_completed,
        "updated_at": datetime.now().isoformat()
    }


@router.get("/stats/overview", response_model=LearningStats)
async def get_learning_stats():
    """
    获取学习统计概览
    """
    courses = list(courses_db.values())
    paths = list(learning_paths_db.values())
    
    total_courses = len([c for c in courses if c.is_published])
    total_learning_paths = len(paths)
    total_enrollments = sum(p.enrolled_count for p in paths)
    
    # 计算活跃学习者（最近30天有活动的用户）
    active_learners = len(set(
        progress.user_id for progress in user_progress_db.values()
        if (datetime.now() - progress.last_activity_at).days <= 30
    ))
    
    # 计算平均完成率
    completion_rates = [p.completion_rate for p in paths]
    average_completion_rate = (
        sum(completion_rates) / len(completion_rates)
        if completion_rates else 0
    )
    
    # 计算热门分类
    category_counts = {}
    for course in courses:
        if course.is_published:
            category_counts[course.category] = category_counts.get(course.category, 0) + 1
    
    popular_categories = sorted(
        category_counts.items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    popular_categories = [cat for cat, _ in popular_categories]
    
    return LearningStats(
        total_courses=total_courses,
        total_learning_paths=total_learning_paths,
        total_enrollments=total_enrollments,
        active_learners=active_learners,
        average_completion_rate=average_completion_rate,
        popular_categories=popular_categories
    )


@router.get("/recommendations")
async def get_recommendations(
    user_id: str = "current_user",
    limit: int = Query(5, ge=1, le=20, description="推荐数量")
):
    """
    获取个性化学习推荐
    
    基于用户的学习历史和兴趣推荐相关课程
    """
    # 获取用户已学习的课程
    user_courses = []
    for key, progress in user_progress_db.items():
        if progress.user_id == user_id:
            user_courses.append(progress.course_id)
    
    # 如果没有学习历史，推荐热门课程
    if not user_courses:
        popular_courses = sorted(
            courses_db.values(),
            key=lambda c: c.student_count,
            reverse=True
        )[:limit]
        
        return {
            "user_id": user_id,
            "recommendation_type": "popular",
            "reason": "基于热门程度推荐",
            "courses": [
                {
                    "id": course.id,
                    "title": course.title,
                    "description": course.description,
                    "category": course.category,
                    "difficulty": course.difficulty,
                    "student_count": course.student_count,
                    "average_rating": course.average_rating
                }
                for course in popular_courses
            ]
        }
    
    # 基于已学课程推荐相关课程
    recommended_courses = []
    
    for course_id in user_courses:
        if course_id in courses_db:
            course = courses_db[course_id]
            
            # 推荐相同分类的课程
            same_category = [
                c for c in courses_db.values()
                if c.category == course.category and 
                   c.id != course_id and
                   c.id not in user_courses and
                   c.is_published
            ]
            
            # 推荐先修课程的后继课程
            for other_course in courses_db.values():
                if course_id in other_course.prerequisites and other_course.id not in user_courses:
                    if other_course.is_published:
                        recommended_courses.append(other_course)
            
            recommended_courses.extend(same_category)
    
    # 去重并按学生数量排序
    unique_courses = {}
    for course in recommended_courses:
        if course.id not in unique_courses:
            unique_courses[course.id] = course
    
    sorted_courses = sorted(
        unique_courses.values(),
        key=lambda c: c.student_count,
        reverse=True
    )[:limit]
    
    return {
        "user_id": user_id,
        "recommendation_type": "personalized",
        "reason": "基于你的学习历史推荐",
        "courses": [
            {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "category": course.category,
                "difficulty": course.difficulty,
                "student_count": course.student_count,
                "average_rating": course.average_rating,
                "relation": "similar_category" if course.category in [
                    c.category for c in user_courses if c in courses_db.values()
                ] else "prerequisite_chain"
            }
            for course in sorted_courses
        ]
    }


@router.post("/courses/{course_id}/rate")
async def rate_course(
    course_id: str,
    user_id: str = "current_user",
    rating: float = Field(..., ge=0.0, le=5.0, description="评分 (0-5)"),
    review: Optional[str] = Field(None, max_length=1000, description="评价内容")
):
    """
    为课程评分
    """
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="课程不存在")
    
    course = courses_db[course_id]
    
    # 模拟更新平均评分
    # 实际应用中应该存储所有评分并重新计算
    current_rating = course.average_rating
    current_students = course.student_count
    
    # 简单加权平均
    new_rating = (current_rating * current_students + rating) / (current_students + 1)
    course.average_rating = round(new_rating, 1)
    
    return {
        "message": "评分成功",
        "course_id": course_id,
        "course_title": course.title,
        "user_id": user_id,
        "rating": rating,
        "new_average_rating": course.average_rating,
        "review": review
    }