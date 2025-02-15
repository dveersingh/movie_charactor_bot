from fastapi import FastAPI
from pydantic import BaseModel
from database import Session, Dialogue
from gemini_utils import get_character_response

app = FastAPI()

class ChatRequest(BaseModel):
    character: str
    user_message: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    # Check database first
    with Session() as session:
        result = session.query(Dialogue).filter(
            Dialogue.character_name.ilike(request.character),
            Dialogue.dialogue.ilike(f"%{request.user_message}%")
        ).first()
        
        if result:
            return {"response": result.dialogue}
    
    # Fallback to AI
    ai_response = get_character_response(request.character, request.user_message)
    return {"response": ai_response}