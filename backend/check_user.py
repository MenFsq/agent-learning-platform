import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from passlib.context import CryptContext

DATABASE_URL = 'sqlite+aiosqlite:///./agent_learning_platform.db'
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

pwd_context = CryptContext(schemes=['pbkdf2_sha256', 'bcrypt'], deprecated='auto')

async def check_user():
    async with async_session() as session:
        result = await session.execute(text("SELECT * FROM users WHERE username = 'testuser'"))
        user = result.fetchone()
        if user:
            print(f'User found: ID={user[0]}, Username={user[2]}')
            print(f'Password hash: {user[3]}')
            # 测试密码
            test_password = 'testpass'
            is_valid = pwd_context.verify(test_password, user[3])
            print(f'Password "testpass" is valid: {is_valid}')
            
            # 也测试其他可能的密码
            for pwd in ['password', 'admin', '123456', 'test']:
                is_valid = pwd_context.verify(pwd, user[3])
                print(f'Password "{pwd}" is valid: {is_valid}')
        else:
            print('User not found')

asyncio.run(check_user())