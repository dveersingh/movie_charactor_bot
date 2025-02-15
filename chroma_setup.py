from sentence_transformers import SentenceTransformer
import chromadb
from database import AsyncSessionLocal, Dialogue
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

async def create_vector_db():
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    try:
        collection = chroma_client.get_or_create_collection(name="dialogues")
        
        async with AsyncSessionLocal() as session:
            result = await session.execute(select(Dialogue))
            dialogues = result.scalars().all()
            
            batch_size = 500
            for i in range(0, len(dialogues), batch_size):
                batch = dialogues[i:i+batch_size]
                
                ids = [str(d.id) for d in batch]
                texts = [d.dialogue for d in batch]
                embeddings = model.encode(texts, show_progress_bar=True)
                
                collection.add(
                    ids=ids,
                    embeddings=embeddings.tolist(),
                    documents=texts
                )
    finally:
        if hasattr(chroma_client, 'close'):
            chroma_client.close()

if __name__ == "__main__":
    import absl.logging
    absl.logging.use_absl_handler()
    asyncio.run(create_vector_db())