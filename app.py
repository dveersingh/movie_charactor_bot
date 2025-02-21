from fastapi import FastAPI, WebSocket, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
import asyncio
from datetime import datetime

# Local imports
from database import get_db, ChatHistory, Dialogue
from cache import cache_response, get_cached_response
from rate_limit import limiter
from chroma_setup import collection, embedder #model
from gemini_utils import generate_character_response
#from config import DB_CONFIG
from sqlalchemy import select
import logging,os

# Configure gRPC logging BEFORE initializing anything else
os.environ["GRPC_VERBOSITY"] = "ERROR"  # Override .env if needed
logging.getLogger("grpc").setLevel(logging.ERROR)
logging.getLogger("grpc.channelz").setLevel(logging.ERROR)
logging.getLogger("grpc.aio").setLevel(logging.ERROR)

app = FastAPI()
app.state.limiter = limiter

# Add Prometheus metrics
Instrumentator().instrument(app).expose(app)

class ChatRequest(BaseModel):
    character: str
    user_message: str

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

    #query_embedding = model.encode(user_message).tolist()
    query_embedding = embedder(user_message)
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

