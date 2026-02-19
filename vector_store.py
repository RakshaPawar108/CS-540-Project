# vector_store.py
import chromadb
from chromadb.utils import embedding_functions
import os

def build_vector_store(chunks: list[dict], collection_name: str = "pubmed_medical"):
    """Embeds chunks and stores them in ChromaDB."""
    
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Free local embeddings — no API key, no cost
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"}
    )
    
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        
        collection.add(
            documents=[c["text"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
            ids=[f"{c['metadata']['pmid']}_chunk_{c['metadata']['chunk_index']}" for c in batch]
        )
        print(f"Stored batch {i//batch_size + 1}/{len(chunks)//batch_size + 1}")
    
    print(f"✅ Stored {len(chunks)} chunks in ChromaDB")
    return collection

def load_vector_store(collection_name: str = "pubmed_medical"):
    """Loads an existing ChromaDB collection (no re-embedding needed)."""
    client = chromadb.PersistentClient(path="./chroma_db")
    
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    return client.get_collection(name=collection_name, embedding_function=ef)