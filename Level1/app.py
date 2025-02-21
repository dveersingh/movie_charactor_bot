from fastapi import FastAPI
from pydantic import BaseModel

#this function from gemini_utils to request gemini
from gemini_utils import generate_character_response
import uvicorn

app = FastAPI()

class ChatRequest(BaseModel):
    character: str
    user_message: str

class ChatResponse(BaseModel):
    character: str
    response: str

#this is the chat endpoint where the request will be send
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    ai_response = generate_character_response(request.character, request.user_message)
    return {
        "character": request.character,
        "response": ai_response
    }

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)