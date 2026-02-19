# retriever.py
def retrieve(query: str, collection, n_results: int = 5) -> list[dict]:
    """
    Given a medical question, returns the top N most relevant chunks.
    This is what your teammates will import and use.
    """
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    # Format into clean, usable output
    retrieved = []
    for i in range(len(results["documents"][0])):
        retrieved.append({
            "text": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "similarity_score": 1 - results["distances"][0][i]  # convert distance → similarity
        })
    
    return retrieved

if __name__ == "__main__":
    from vector_store import load_vector_store
    
    collection = load_vector_store()
    results = retrieve("What are treatments for type 2 diabetes?", collection)
    
    for r in results:
        print(f"Score: {r['similarity_score']:.3f}")
        print(f"Source: {r['metadata']['source']}")
        print(f"Text: {r['text'][:200]}")
        print("---")