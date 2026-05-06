"""
生产环境启动脚本
从环境变量读取配置，不使用硬编码的开发值
"""
import os
import sys

# 确保 src 路径可导入
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app
import uvicorn

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8005"))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print(f"[Runner] Starting on {host}:{port} (debug={debug})")
    uvicorn.run(app, host=host, port=port)
