from sentence_transformers import SentenceTransformer
import chromadb
from database import AsyncSessionLocal, Dialogue
from sqlalchemy import select
import asyncio

# Initialize model and client at top level
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="dialogues")

async def create_vector_db():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Dialogue))
        dialogues = result.scalars().all()
        
        batch_size = 500
        for i in range(0, len(dialogues), batch_size):
            batch = dialogues[i:i+batch_size]
            
            ids = [str(d.id) for d in batch]
            texts = [d.dialogue for d in batch]
            embeddings = model.encode(texts)
            
            collection.add(
                ids=ids,
                embeddings=embeddings.tolist(),
                documents=texts
            )

if __name__ == "__main__":
    asyncio.run(create_vector_db())