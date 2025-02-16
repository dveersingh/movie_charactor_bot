from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from config import DB_CONFIG

Base = declarative_base()

engine = create_async_engine(
    f"postgresql+asyncpg://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}",
    pool_size=20
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

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
    character = Column(String(100))
    message = Column(Text)
    response = Column(Text)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)