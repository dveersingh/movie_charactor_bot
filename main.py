from fastapi import FastAPI
from chroma_setup import model, chroma_client
from database import Session, Dialogue
from gemini_utils import get_character_response
from pydantic import BaseModel
app = FastAPI()

class ChatRequest(BaseModel):
    character: str
    user_message: str

collection = chroma_client.get_collection("dialogues")

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    # 1. Semantic search with RAG
    query_embedding = model.encode([request.user_message])[0].tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    
    if results['distances'][0][0] < 0.3:  # Similarity threshold
        return {"response": results['documents'][0][0]}
    
    # 2. Fallback to AI with context
    context = "\n".join(results['documents'][0])
    ai_response = get_character_response(
        character=request.character,
        message=f"Context:\n{context}\n\nUser: {request.user_message}"
    )
    
    return {"response": ai_response}