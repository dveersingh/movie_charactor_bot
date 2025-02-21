from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text
from config import DB_CONFIG

Base = declarative_base()

# Async engine with connection pool
engine = create_async_engine(
    f"postgresql+asyncpg://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}",
    pool_size=20,
    max_overflow=10
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class Dialogue(Base):
    __tablename__ = "dialogues"
    id = Column(Integer, primary_key=True)
    character_name = Column(String(100))
    dialogue = Column(Text)