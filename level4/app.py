from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from typing import AsyncGenerator
from pydantic import BaseModel
import absl.logging
import logging
from database import engine, AsyncSessionLocal, Dialogue
from cache import cache_response, get_cached_response, redis_client
from rate_limit import limiter
from chroma_setup import model
from gemini_utils import generate_character_response
from sqlalchemy import select
import asyncio
from sqlalchemy import text
import chromadb

class ChatRequest(BaseModel):
    character: str
    user_message: str

app = FastAPI()
app.state.limiter = limiter

@app.on_event("startup")
async def startup():
    # Initialize logging first
    #absl.logging.get_absl_handler().setFormatter(logging.Formatter('%(levelname)s:%(message)s'))
    #absl.logging.set_verbosity(absl.logging.INFO)
    
    # Verify database connection using text()
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))  # Fixed line
        await conn.close()
@app.on_event("shutdown")
async def shutdown():
    # Cleanup resources properly
    await engine.dispose()
    redis_client.close()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

@app.post("/chat")
@limiter.limit("5/second")
async def chat_endpoint(
    request: Request,
    chat_data: ChatRequest,
    db: AsyncSession = Depends(get_db)
):
    character = chat_data.character
    user_message = chat_data.user_message

    if cached := get_cached_response(user_message):
        return {"response": cached}

    query_embedding = model.encode(user_message).tolist()
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    try:
        collection = chroma_client.get_collection("dialogues")
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3
        )
        
        if results['distances'][0][0] < 0.3:
            response = results['documents'][0][0]
            cache_response(user_message, response)
            return {"response": response}

        result = await db.execute(
            select(Dialogue).filter(
                Dialogue.character_name.ilike(f"%{character}%"),
                Dialogue.dialogue.ilike(f"%{user_message}%")
            ).limit(1)
        )
        if dialogue := result.scalar():
            return {"response": dialogue.dialogue}

        context = "\n".join(results['documents'][0])
        response = generate_character_response(character, user_message, context)
        cache_response(user_message, response)
        return {"response": response}
    finally:
        if hasattr(chroma_client, 'close'):
            chroma_client.close()

if __name__ == "__main__":
    import uvicorn
    #absl.logging.use_absl_handler()
    uvicorn.run(app, host="0.0.0.0", port=8000)