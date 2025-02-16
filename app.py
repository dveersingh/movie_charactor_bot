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
from chroma_setup import collection, model
from gemini_utils import generate_character_response
from config import DB_CONFIG
from sqlalchemy import select

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
    # Existing Level 4 logic
    character = chat_data.character
    user_message = chat_data.user_message

    if cached := get_cached_response(user_message):
        return {"response": cached}

    query_embedding = model.encode(user_message).tolist()
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

@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            
            # Process message using existing logic
            response = await process_message(data)
            
            # Store history
            async with get_db() as db:
                db.add(ChatHistory(
                    user_id="anonymous",
                    character=data['character'],
                    message=data['user_message'],
                    response=response,
                    timestamp=datetime.utcnow()
                ))
                await db.commit()
            
            await websocket.send_json({"response": response})
    except WebSocketDisconnect:
        await websocket.close()

async def process_message(data: dict):
    # Reuse existing chat logic
    character = data['character']
    user_message = data['user_message']
    
    if cached := get_cached_response(user_message):
        return cached
    
    # Rest of the chat logic from POST endpoint
    # ... (copy the core logic from POST /chat here)
    
    
    
    query_embedding = model.encode(user_message).tolist()
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
    
    
    return response