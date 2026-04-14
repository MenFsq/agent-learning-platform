"""
系统管理API模块
提供系统状态、配置、监控等功能
"""

import os
import platform
import psutil
from datetime import datetime
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/system", tags=["system"])


# 数据模型
class SystemInfo(BaseModel):
    """系统信息模型"""
    platform: str = Field(..., description="操作系统平台")
    platform_version: str = Field(..., description="平台版本")
    architecture: str = Field(..., description="系统架构")
    hostname: str = Field(..., description="主机名")
    python_version: str = Field(..., description="Python版本")
    cpu_count: int = Field(..., description="CPU核心数")
    total_memory: int = Field(..., description="总内存(字节)")
    available_memory: int = Field(..., description="可用内存(字节)")
    disk_usage: Dict[str, Any] = Field(..., description="磁盘使用情况")
    boot_time: datetime = Field(..., description="系统启动时间")
    uptime: str = Field(..., description="运行时间")


class ServiceStatus(BaseModel):
    """服务状态模型"""
    service: str = Field(..., description="服务名称")
    status: str = Field(..., description="状态: running, stopped, error")
    version: str = Field(..., description="服务版本")
    last_check: datetime = Field(..., description="最后检查时间")
    response_time: float = Field(..., description="响应时间(毫秒)")
    details: Dict[str, Any] = Field(default_factory=dict, description="详细信息")


class HealthCheck(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="状态: healthy, degraded, unhealthy")
    service: str = Field(..., description="服务名称")
    version: str = Field(..., description="服务版本")
    timestamp: datetime = Field(..., description="检查时间")
    checks: List[ServiceStatus] = Field(default_factory=list, description="各组件检查结果")
    uptime: str = Field(..., description="服务运行时间")


class Metrics(BaseModel):
    """系统指标模型"""
    timestamp: datetime = Field(..., description="指标时间")
    cpu_percent: float = Field(..., description="CPU使用率")
    memory_percent: float = Field(..., description="内存使用率")
    disk_percent: float = Field(..., description="磁盘使用率")
    active_connections: int = Field(..., description="活跃连接数")
    request_count: int = Field(..., description="请求计数")
    error_count: int = Field(..., description="错误计数")
    response_time_avg: float = Field(..., description="平均响应时间")


class ConfigItem(BaseModel):
    """配置项模型"""
    key: str = Field(..., description="配置键")
    value: Any = Field(..., description="配置值")
    type: str = Field(..., description="值类型")
    description: str = Field(..., description="配置描述")
    is_editable: bool = Field(False, description="是否可编辑")
    updated_at: datetime = Field(..., description="最后更新时间")


# 模拟数据
service_start_time = datetime.now()
request_counter = 0
error_counter = 0


@router.get("/info", response_model=SystemInfo)
async def get_system_info():
    """
    获取系统信息
    
    返回操作系统、硬件、运行环境等详细信息
    """
    try:
        # 获取系统信息
        sys_platform = platform.system()
        platform_version = platform.version()
        architecture = platform.machine()
        hostname = platform.node()
        python_version = platform.python_version()
        
        # 获取CPU信息
        cpu_count = psutil.cpu_count()
        
        # 获取内存信息
        memory = psutil.virtual_memory()
        total_memory = memory.total
        available_memory = memory.available
        
        # 获取磁盘信息
        disk_usage = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_usage[partition.mountpoint] = {
                    "total": usage.total,
                    "used": usage.used,
                    "free": usage.free,
                    "percent": usage.percent
                }
            except:
                continue
        
        # 获取启动时间
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime_seconds = (datetime.now() - boot_time).total_seconds()
        
        # 格式化运行时间
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        uptime = f"{days}d {hours}h {minutes}m {seconds}s"
        
        return SystemInfo(
            platform=sys_platform,
            platform_version=platform_version,
            architecture=architecture,
            hostname=hostname,
            python_version=python_version,
            cpu_count=cpu_count,
            total_memory=total_memory,
            available_memory=available_memory,
            disk_usage=disk_usage,
            boot_time=boot_time,
            uptime=uptime
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取系统信息失败: {str(e)}"
        )


@router.get("/health", response_model=HealthCheck)
async def health_check():
    """
    系统健康检查
    
    检查所有关键组件的运行状态
    """
    global service_start_time
    
    checks = []
    
    # 检查API服务
    try:
        api_status = ServiceStatus(
            service="api-server",
            status="running",
            version="1.0.0",
            last_check=datetime.now(),
            response_time=0.5,
            details={
                "endpoints": 15,
                "active_workers": 4,
                "memory_usage": "45MB"
            }
        )
        checks.append(api_status)
    except Exception as e:
        api_status = ServiceStatus(
            service="api-server",
            status="error",
            version="1.0.0",
            last_check=datetime.now(),
            response_time=0,
            details={"error": str(e)}
        )
        checks.append(api_status)
    
    # 检查数据库连接（模拟）
    try:
        db_status = ServiceStatus(
            service="database",
            status="running",
            version="sqlite-3.45.0",
            last_check=datetime.now(),
            response_time=2.1,
            details={
                "type": "sqlite",
                "connections": 3,
                "last_backup": "2026-04-14 23:00:00"
            }
        )
        checks.append(db_status)
    except Exception as e:
        db_status = ServiceStatus(
            service="database",
            status="error",
            version="unknown",
            last_check=datetime.now(),
            response_time=0,
            details={"error": str(e)}
        )
        checks.append(db_status)
    
    # 检查外部API（模拟）
    try:
        external_api_status = ServiceStatus(
            service="external-apis",
            status="running",
            version="1.0.0",
            last_check=datetime.now(),
            response_time=150.3,
            details={
                "ai_services": "available",
                "storage_services": "available",
                "monitoring": "enabled"
            }
        )
        checks.append(external_api_status)
    except Exception as e:
        external_api_status = ServiceStatus(
            service="external-apis",
            status="degraded",
            version="1.0.0",
            last_check=datetime.now(),
            response_time=0,
            details={"error": str(e)}
        )
        checks.append(external_api_status)
    
    # 确定整体状态
    statuses = [check.status for check in checks]
    if "error" in statuses:
        overall_status = "unhealthy"
    elif "degraded" in statuses:
        overall_status = "degraded"
    else:
        overall_status = "healthy"
    
    # 计算运行时间
    uptime_seconds = (datetime.now() - service_start_time).total_seconds()
    days = int(uptime_seconds // 86400)
    hours = int((uptime_seconds % 86400) // 3600)
    minutes = int((uptime_seconds % 3600) // 60)
    seconds = int(uptime_seconds % 60)
    uptime_str = f"{days}d {hours}h {minutes}m {seconds}s"
    
    return HealthCheck(
        status=overall_status,
        service="agent-learning-platform",
        version="1.0.0",
        timestamp=datetime.now(),
        checks=checks,
        uptime=uptime_str
    )


@router.get("/metrics", response_model=Metrics)
async def get_system_metrics():
    """
    获取系统性能指标
    
    返回CPU、内存、磁盘、网络等实时指标
    """
    global request_counter, error_counter
    
    try:
        # 获取CPU使用率
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # 获取内存使用率
        memory_percent = psutil.virtual_memory().percent
        
        # 获取磁盘使用率（使用根目录）
        disk_percent = psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:\\').percent
        
        # 模拟连接数和请求计数
        active_connections = 12  # 模拟值
        
        # 更新请求计数
        request_counter += 1
        
        return Metrics(
            timestamp=datetime.now(),
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            disk_percent=disk_percent,
            active_connections=active_connections,
            request_count=request_counter,
            error_count=error_counter,
            response_time_avg=45.2  # 模拟值
        )
        
    except Exception as e:
        error_counter += 1
        raise HTTPException(
            status_code=500,
            detail=f"获取系统指标失败: {str(e)}"
        )


@router.get("/metrics/history")
async def get_metrics_history(
    hours: int = 24,
    interval_minutes: int = 5
):
    """
    获取历史指标数据
    
    返回指定时间范围内的指标历史记录
    """
    if hours > 168:  # 限制最多7天
        hours = 168
    
    if interval_minutes < 1:
        interval_minutes = 1
    elif interval_minutes > 60:
        interval_minutes = 60
    
    # 模拟历史数据
    history = []
    now = datetime.now()
    
    for i in range(hours * 60 // interval_minutes):
        timestamp = now - timedelta(minutes=i * interval_minutes)
        
        # 模拟波动数据
        base_cpu = 20.0
        cpu_variation = 10.0 * (i % 12) / 12
        cpu_percent = base_cpu + cpu_variation
        
        base_memory = 45.0
        memory_variation = 5.0 * (i % 8) / 8
        memory_percent = base_memory + memory_variation
        
        base_disk = 65.0
        disk_increment = 0.01 * i
        disk_percent = min(base_disk + disk_increment, 85.0)
        
        # 模拟请求模式（白天活跃，夜晚低峰）
        hour_of_day = timestamp.hour
        if 9 <= hour_of_day <= 17:  # 工作时间
            request_rate = 100 + 50 * (hour_of_day - 9) / 8
        else:
            request_rate = 20 + 30 * abs(hour_of_day - 1) / 12
        
        history.append({
            "timestamp": timestamp.isoformat(),
            "cpu_percent": round(cpu_percent, 1),
            "memory_percent": round(memory_percent, 1),
            "disk_percent": round(disk_percent, 1),
            "active_connections": int(10 + 5 * (i % 6) / 6),
            "request_count": int(request_counter * (i / (hours * 60 // interval_minutes))),
            "error_count": int(error_counter * (i / (hours * 60 // interval_minutes))),
            "response_time_avg": 30.0 + 20.0 * (i % 10) / 10
        })
    
    return {
        "time_range_hours": hours,
        "interval_minutes": interval_minutes,
        "data_points": len(history),
        "history": list(reversed(history))  # 时间顺序：从旧到新
    }


@router.get("/config", response_model=List[ConfigItem])
async def get_system_config():
    """
    获取系统配置
    
    返回所有可配置的系统参数
    """
    config_items = [
        ConfigItem(
            key="api.rate_limit.enabled",
            value=True,
            type="boolean",
            description="是否启用API速率限制",
            is_editable=True,
            updated_at=datetime(2026, 4, 1)
        ),
        ConfigItem(
            key="api.rate_limit.requests_per_minute",
            value=60,
            type="integer",
            description="每分钟请求限制",
            is_editable=True,
            updated_at=datetime(2026, 4, 1)
        ),
        ConfigItem(
            key="api.cors.enabled",
            value=True,
            type="boolean",
            description="是否启用CORS跨域支持",
            is_editable=True,
            updated_at=datetime(2026, 4, 1)
        ),
        ConfigItem(
            key="api.cors.allowed_origins",
            value=["http://localhost:5178", "http://localhost:8001"],
            type="list",
            description="允许的跨域来源",
            is_editable=True,
            updated_at=datetime(2026, 4, 14)
        ),
        ConfigItem(
            key="database.type",
            value="sqlite",
            type="string",
            description="数据库类型",
            is_editable=False,
            updated_at=datetime(2026, 4, 1)
        ),
        ConfigItem(
            key="database.path",
            value="./data/agent_platform.db",
            type="string",
            description="数据库文件路径",
            is_editable=True,
            updated_at=datetime(2026, 4, 1)
        ),
        ConfigItem(
            key="logging.level",
            value="INFO",
            type="string",
            description="日志级别",
            is_editable=True,
            updated_at=datetime(2026, 4, 1)
        ),
        ConfigItem(
            key="logging.max_size_mb",
            value=100,
            type="integer",
            description="日志文件最大大小(MB)",
            is_editable=True,
            updated_at=datetime(2026, 4, 1)
        ),
        ConfigItem(
            key="security.jwt.secret",
            value="********",
            type="string",
            description="JWT密钥（已隐藏）",
            is_editable=True,
            updated_at=datetime(2026, 4, 1)
        ),
        ConfigItem(
            key="security.jwt.expire_minutes",
            value=1440,
            type="integer",
            description="JWT过期时间(分钟)",
            is_editable=True,
            updated_at=datetime(2026, 4, 1)
        ),
        ConfigItem(
            key="cache.enabled",
            value=True,
            type="boolean",
            description="是否启用缓存",
            is_editable=True,
            updated_at=datetime(2026, 4, 1)
        ),
        ConfigItem(
            key="cache.ttl_seconds",
            value=300,
            type="integer",
            description="缓存存活时间(秒)",
            is_editable=True,
            updated_at=datetime(2026, 4, 1)
        ),
        ConfigItem(
            key="monitoring.enabled",
            value=True,
            type="boolean",
            description="是否启用监控",
            is_editable=True,
            updated_at=datetime(2026, 4, 1)
        ),
        ConfigItem(
            key="monitoring.alert_email",
            value="admin@agent-learning.com",
            type="string",
            description="监控告警邮箱",
            is_editable=True,
            updated_at=datetime(2026, 4, 1)
        )
    ]
    
    return config_items


@router.put("/config/{config_key}")
async def update_config(config_key: str, value: Any):
    """
    更新系统配置
    
    更新指定配置项的值
    """
    # 模拟配置更新
    # 实际应用中应该验证配置项和值类型，并持久化存储
    
    valid_configs = {
        "api.rate_limit.enabled": bool,
        "api.rate_limit.requests_per_minute": int,
        "api.cors.enabled": bool,
        "api.cors.allowed_origins": list,
        "database.path": str,
        "logging.level": str,
        "logging.max_size_mb": int,
        "security.jwt.secret": str,
        "security.jwt.expire_minutes": int,
        "cache.enabled": bool,
        "cache.ttl_seconds": int,
        "monitoring.enabled": bool,
        "monitoring.alert_email": str
    }
    
    if config_key not in valid_configs:
        raise HTTPException(
            status_code=404,
            detail=f"配置项不存在: {config_key}"
        )
    
    # 验证值类型
    expected_type = valid_configs[config_key]
    if not isinstance(value, expected_type):
        raise HTTPException(
            status_code=400,
            detail=f"配置值类型错误，期望 {expected_type.__name__}，实际 {type(value).__name__}"
        )
    
    # 验证特定约束
    if config_key == "api.rate_limit.requests_per_minute" and value <= 0:
        raise HTTPException(
            status_code=400,
            detail="请求限制必须大于0"
        )
    
    if config_key == "security.jwt.expire_minutes" and value < 1:
        raise HTTPException(
            status_code=400,
            detail="JWT过期时间必须大于0分钟"
        )
    
    if config_key == "logging.max_size_mb" and value < 1:
        raise HTTPException(
            status_code=400,
            detail="日志文件大小必须大于0MB"
        )
    
    if config_key == "cache.ttl_seconds" and value < 1:
        raise HTTPException(
            status_code=400,
            detail="缓存存活时间必须大于0秒"
        )
    
    return {
        "message": "配置更新成功",
        "config_key": config_key,
        "value": value,
        "updated_at": datetime.now().isoformat()
    }


@router.get("/logs")
async def get_system_logs(
    level: str = "INFO",
    limit: int = 100,
    search: str = None
):
    """
    获取系统日志
    
    返回系统运行日志，支持按级别和关键词筛选
    """
    # 模拟日志数据
    log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    
    if level.upper() not in log_levels:
        raise HTTPException(
            status_code=400,
            detail=f"无效的日志级别，可选值: {', '.join(log_levels)}"
        )
    
    # 模拟日志条目
    logs = []
    for i in range(limit):
        log_time = datetime.now() - timedelta(minutes=i * 5)
        
        # 模拟不同的日志级别
        if i % 20 == 0:
            log_level = "ERROR"
            message = f"数据库连接超时，重试中... (attempt {i//20 + 1})"
        elif i % 10 == 0:
            log_level = "WARNING"
            message = f"API请求响应时间超过阈值: {150 + i%50}ms"
        elif i % 5 == 0:
            log_level = "INFO"
            message = f"用户登录成功: user_{i%100}"
        else:
            log_level = "DEBUG"
            message = f"处理请求: GET /api/v1/{['projects', 'learning', 'system'][i%3]}"
        
        # 添加一些特定的日志用于搜索测试
        if i == 15:
            message = "系统启动完成，所有服务正常运行"
            log_level = "INFO"
        elif i == 30:
            message = "数据库备份完成，大小: 45.2MB"
            log_level = "INFO"
        elif i == 45:
            message = "监控告警: CPU使用率超过80%"
            log_level = "WARNING"
        
        logs.append({
            "timestamp": log_time.isoformat(),
            "level": log_level,
            "message": message,
            "source": f"app.server.{i%3}",
            "request_id": f"req_{i:08x}"
        })
    
    # 按级别筛选
    level_index = log_levels.index(level.upper())
    filtered_logs = [
        log for log in logs
        if log_levels.index(log["level"]) >= level_index
    ]
    
    # 关键词搜索
    if search:
        search_lower = search.lower()
        filtered_logs = [
            log for log in filtered_logs
            if search_lower in log["message"].lower() or
               search_lower in log["source"].lower()
        ]
    
    return {
        "total_logs": len(filtered_logs),
        "filtered_level": level,
        "search_query": search,
        "logs": filtered_logs[:limit]
    }


@router.post("/maintenance/backup")
async def create_backup():
    """
    创建系统备份
    
    触发系统数据备份操作
    """
    backup_time = datetime.now()
    backup_id = f"backup_{backup_time.strftime('%Y%m%d_%H%M%S')}"
    
    # 模拟备份过程
    backup_size = 152.7  # MB
    backup_files = [
        "database.sqlite",
        "config.json",
        "logs/app.log",
        "uploads/",
        "templates/"
    ]
    
    return {
        "message": "备份创建成功",
        "backup_id": backup_id,
        "timestamp": backup_time.isoformat(),
        "size_mb": backup_size,
        "files": backup_files,
        "status": "completed",
        "duration_seconds": 45.3
    }


@router.get("/maintenance/backups")
async def list_backups():
    """
    列出所有备份
    
    返回系统备份列表
    """
    backups = []
    
    for i in range(5):
        backup_time = datetime.now() - timedelta(days=i*2)
        backup_id = f"backup_{backup_time.strftime('%Y%m%d_%H%M%S')}"
        
        backups.append({
            "id": backup_id,
            "timestamp": backup_time.isoformat(),
            "size_mb": 150.0 + i*5.2,
            "status": "completed",
            "files_count": 5 + i,
            "retention_days": 30 - i*2
        })
    
    return {
        "total_backups": len(backups),
        "total_size_mb": sum(b["size_mb"] for b in backups),
        "backups": backups
    }


@router.post("/restart")
async def restart_service():
    """
    重启服务
    
    触发服务重启（需要管理员权限）
    """
    # 实际应用中应该实现安全的服务重启逻辑
    # 这里只是模拟
    
    return {
        "message": "服务重启已触发",
        "timestamp": datetime.now().isoformat(),
        "estimated_downtime": "10-30 seconds",
        "status": "restarting"
    }


@router.get("/version")
async def get_version_info():
    """
    获取版本信息
    
    返回系统组件版本信息
    """
    return {
        "service": "agent-learning-platform",
        "version": "1.0.0",
        "build_date": "2026-04-14",
        "git_commit": "a1b2c3d4e5f67890",
        "components": {
            "api_server": "1.0.0",
            "database": "sqlite-3.45.0",
            "authentication": "jwt-1.0.0",
            "cache": "redis-1.0.0",
            "monitoring": "prometheus-1.0.0"
        },
        "dependencies": {
            "fastapi": "0.104.1",
            "uvicorn": "0.24.0",
            "pydantic": "2.5.0",
            "sqlalchemy": "2.0.23",
            "psutil": "5.9.6"
        }
    }


# 导入timedelta
from datetime import timedelta