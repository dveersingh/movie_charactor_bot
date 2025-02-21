from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
import ssl
import os
from config import DB_URL

CA_CERT_PATH = "./ca.pem"  

Base = declarative_base()


DATABASE_URL = (DB_URL)

# SSL context configuration
ssl_context = ssl.create_default_context(cafile=CA_CERT_PATH)
ssl_context.verify_mode = ssl.CERT_REQUIRED

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    connect_args={
        "ssl": ssl_context,
        "server_settings": {
            "application_name": "MovieBotApp"
        }
    }
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

# To test the connection and table creation
async def main():
    try:
        await create_tables()
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await engine.dispose()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())