from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

print(os.getenv("DATABASE_URL"))

engine = create_async_engine(os.getenv("DATABASE_URL"))


async_session_factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
