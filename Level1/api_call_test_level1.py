import requests

# API endpoint
API_URL = "https://huggingface.co/spaces/dveersingh/movie_character"

# Function to send a message to the chatbot
def chat_with_character(character: str, user_message: str):
    payload = {
        "character": character,
        "user_message": user_message
    }
    
    # Send POST request to the API
    response = requests.post(API_URL, json=payload)
    print(response.json())
    """
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Request failed with status code {response.status_code}"}"""

# Example usage
if __name__ == "__main__":
    # Test with Tony Stark
    character = "Tony Stark"
    user_message = "What's your secret to building such advanced tech?"
    
    result = chat_with_character(character, user_message)
    #print(f"{character}: {result['response']}")