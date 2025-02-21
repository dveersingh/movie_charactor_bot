import google.generativeai as genai
from config import GEMINI_KEY

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

def generate_character_response(character: str, user_message: str, context: str = ""):
    prompt = f"""You are {character} from a movie. Respond to the user in 2-3 sentences using their personality and style.
    
    Context from previous dialogues:
    {context}
    
    User message: {user_message}
    
    Respond exactly as {character} would:"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"{character}: ❌ System error - Could not generate response. (AI Service Down)"