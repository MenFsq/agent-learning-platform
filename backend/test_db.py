import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from dotenv import load_dotenv

# 加载环境变量（自动读取当前目录的 .env）
load_dotenv()

async def test_db():
    # 从 .env 读取数据库连接
    db_url = os.getenv("DATABASE_URL")
    print("📌 读取到的数据库URL：", db_url)

    # 创建数据库连接
    engine = create_async_engine(db_url)

    try:
        async with engine.connect() as conn:
            print("✅ 数据库连接成功！")

            # 正确写法：必须用 text()
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print("📦 PostgreSQL 版本：", version)

    except Exception as e:
        print("❌ 连接失败：", str(e))
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_db())