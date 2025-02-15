import google.generativeai as genai
from config import GEMINI_KEY

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

def get_character_response(character, message):
    prompt = f"Respond as {character} would: {message}"
    response = model.generate_content(prompt)
    return response.text