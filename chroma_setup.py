import chromadb
from database import AsyncSessionLocal, Dialogue
from sqlalchemy import select
import requests
from tenacity import retry, wait_exponential, stop_after_attempt
from config import HF_API_TOKEN, HF_URL

class HuggingFaceEmbedder:
    def __init__(self):
    
        self.api_token = HF_API_TOKEN
        self.api_url = HF_URL
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    @retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
    def __call__(self, input: list[str]) -> list[list[float]]:
        if isinstance(input, str):  # Ensure input is a list
            input = [input]

        response = requests.post(
            self.api_url,
            headers=self.headers,
            json={"inputs": input, "options": {"wait_for_model": True}},
            timeout=10
        )
        response.raise_for_status()
        return response.json()[0]  # Return list of embeddings directly

# Initialize ChromaDB with Hugging Face embeddings
embedder = HuggingFaceEmbedder()
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(
    name="dialogues",
    embedding_function=embedder  
)