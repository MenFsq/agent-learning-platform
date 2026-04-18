import os
import sys

# 设置环境变量
os.environ['DATABASE_URL'] = 'sqlite+aiosqlite:///./agent_learning_platform.db'
os.environ['SECRET_KEY'] = 'dev-secret-key-change-in-production-1234567890'
os.environ['DEBUG'] = 'True'
os.environ['ENVIRONMENT'] = 'development'

# 导入并执行主应用
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 直接导入并运行
from src.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)