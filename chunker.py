from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(documents: list[dict]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "]
    )
    
    chunks = []
    for doc in documents:
        split_texts = splitter.split_text(doc["full_text"])
        
        for i, chunk_text in enumerate(split_texts):
            chunks.append({
                "text": chunk_text,
                "metadata": {
                    "pmid": doc["pmid"],
                    "source": doc["source"],
                    "is_full_text": doc["is_full_text"],
                    "chunk_index": i
                }
            })
    
    return chunks