"""
Agent 持久化存储模块
使用 JSON 文件持久化 Agent 配置和对话历史
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger

# 数据目录
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
AGENTS_FILE = DATA_DIR / "agents.json"
CONVERSATIONS_FILE = DATA_DIR / "conversations.json"


def _ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_agents() -> Dict[str, Dict[str, Any]]:
    """加载 Agent 配置"""
    _ensure_data_dir()
    if not AGENTS_FILE.exists():
        return {}
    try:
        with open(AGENTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load agents: {e}")
        return {}


def save_agents(agents: Dict[str, Dict[str, Any]]):
    """保存 Agent 配置"""
    _ensure_data_dir()
    try:
        with open(AGENTS_FILE, "w", encoding="utf-8") as f:
            json.dump(agents, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to save agents: {e}")


def load_conversations() -> Dict[str, List[Dict[str, Any]]]:
    """加载对话历史"""
    _ensure_data_dir()
    if not CONVERSATIONS_FILE.exists():
        return {}
    try:
        with open(CONVERSATIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load conversations: {e}")
        return {}


def save_conversations(conversations: Dict[str, List[Dict[str, Any]]]):
    """保存对话历史"""
    _ensure_data_dir()
    try:
        # 每个 Agent 只保留最近 200 条消息
        trimmed = {}
        for agent_id, msgs in conversations.items():
            trimmed[agent_id] = msgs[-200:]
        with open(CONVERSATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(trimmed, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to save conversations: {e}")
