"""
CLI script to seed ChromaDB with PubMed abstracts.
Run from backend/ with the venv active:

    python seed_db.py

Requires PUBMED_EMAIL in .env. Set NCBI_API_KEY to cut runtime from ~60 min to ~13 min.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
load_dotenv()

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.services.seeding import run_seed, DOMAIN_QUERIES, MAX_RESULTS_PER_QUERY

CHROMA_DIR  = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION  = os.getenv("CHROMA_COLLECTION", "pubmed_abstracts")
EMAIL       = os.getenv("PUBMED_EMAIL", "")
NCBI_KEY    = os.getenv("NCBI_API_KEY", "")

if __name__ == "__main__":
    if not EMAIL:
        raise SystemExit("Set PUBMED_EMAIL in .env before running.")

    sleep_s = 0.1 if NCBI_KEY else 0.4
    est_min = int(len(DOMAIN_QUERIES) * MAX_RESULTS_PER_QUERY * sleep_s / 60)
    print(f"Queries : {len(DOMAIN_QUERIES)} across 20 PubMedQA domains")
    print(f"Max results per query : {MAX_RESULTS_PER_QUERY}")
    print(f"NCBI API key : {'yes — 10 req/s' if NCBI_KEY else 'no — 3 req/s (add NCBI_API_KEY to go faster)'}")
    print(f"Estimated time : ~{est_min} min\n")

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    vector_store = Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )

    total = run_seed(vector_store=vector_store, email=EMAIL, ncbi_api_key=NCBI_KEY)
    print(f"\nDone — {total} chunks in '{COLLECTION}' at '{CHROMA_DIR}'")
