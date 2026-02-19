# ingest.py — run this once to build the database
from dotenv import load_dotenv
from pubmed_fetcher import search_pubmed, fetch_documents
from chunker import chunk_documents
from vector_store import build_vector_store

load_dotenv()

MEDICAL_QUERIES = [
    "diabetes treatment clinical trial",
    "hypertension medication",
    "COVID-19 treatment outcomes",
    "cancer immunotherapy",
    "antibiotic resistance",
]

if __name__ == "__main__":
    all_documents = []
    
    for query in MEDICAL_QUERIES:
        print(f"\nSearching PubMed for: {query}")
        pmids = search_pubmed(query, max_results=200)
        docs = fetch_documents(pmids)
        all_documents.extend(docs)
        print(f"  Got {len(docs)} abstracts")
    
    # Deduplicate by PMID
    seen = set()
    unique_docs = []
    for doc in all_documents:
        if doc["pmid"] not in seen:
            seen.add(doc["pmid"])
            unique_docs.append(doc)
    
    print(f"\nTotal unique documents: {len(unique_docs)}")
    
    chunks = chunk_documents(unique_docs)
    print(f"Total chunks: {len(chunks)}")
    
    build_vector_store(chunks)