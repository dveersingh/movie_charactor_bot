import google.generativeai as genai
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)


#Load the model
model = genai.GenerativeModel('gemini-pro')

def generate_character_response(character: str, user_message: str) -> str:
    prompt = f"""
    You are {character} from the movie. Respond to the user's message exactly as {character} would.
    Stay completely in character and use the character's typical speech patterns and personality.
    
    User Message: {user_message}
    {character}'s Response: 
    """
    #send the requests and get the response
    response = model.generate_content(prompt)
    return response.text