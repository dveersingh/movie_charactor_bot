from sentence_transformers import SentenceTransformer
import chromadb
from database import Session, Dialogue
import config

model = SentenceTransformer(config.EMBEDDING_MODEL)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def create_vector_db():
    collection = chroma_client.create_collection(name="dialogues")
    
    with Session() as session:
        dialogues = session.query(Dialogue).all()
        
        # Batch processing for 20k+ rows
        batch_size = 500
        for i in range(0, len(dialogues), batch_size):
            batch = dialogues[i:i+batch_size]
            
            ids = [str(d.id) for d in batch]
            texts = [d.dialogue for d in batch]
            embeddings = model.encode(texts, show_progress_bar=True)
            
            collection.add(
                embeddings=embeddings.tolist(),
                documents=texts,
                ids=ids
            )