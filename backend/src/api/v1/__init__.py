"""
API v1 路由模块
"""
from fastapi import APIRouter

from . import auth, projects, learning, system

# 创建主路由器
router = APIRouter()

# 包含子路由
router.include_router(auth.router)
router.include_router(projects.router)
router.include_router(learning.router)
router.include_router(system.router)

# 这里可以添加其他API模块
# from . import ai, community, etc.
# router.include_router(ai.router)
# router.include_router(community.router)