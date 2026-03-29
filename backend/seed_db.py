"""
One-off script to seed ChromaDB with PubMed abstracts.
Run from backend/ with the venv active:
    python seed_db.py

Uses the same Chroma collection/path as the FastAPI backend so the
multi-turn RAG endpoint can query it immediately after.
"""
import os
import time
import requests
from dotenv import load_dotenv
from Bio import Entrez
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()

# --- Config (must match .env / config.py defaults) ---
CHROMA_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION  = os.getenv("CHROMA_COLLECTION", "pubmed_abstracts")
EMAIL       = os.getenv("PUBMED_EMAIL", "")

Entrez.email = EMAIL

QUERIES = [
    "diabetes treatment clinical trial",
    "hypertension medication",
    "COVID-19 treatment outcomes",
    "cancer immunotherapy",
    "antibiotic resistance",
]
MAX_RESULTS_PER_QUERY = 50   # keep small for a quick test run


# --- PubMed fetch (from friend's pubmed_fetcher.py) ---

def search_pubmed(query: str, max_results: int) -> list[str]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]


def fetch_full_text(pmid: str) -> dict | None:
    url = (
        f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/"
        f"pmcoa.cgi/BioC_json/{pmid}/unicode"
    )
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
        data = response.json()
        parts = []
        for document in data.get("documents", []):
            for passage in document.get("passages", []):
                section = passage.get("infons", {}).get("section_type", "unknown")
                text = passage.get("text", "").strip()
                if text:
                    parts.append(f"[{section}] {text}")
        if not parts:
            return None
        return {
            "pmid": pmid,
            "full_text": "\n\n".join(parts),
            "source": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "is_full_text": True,
        }
    except Exception:
        return None


def fetch_abstract_fallback(pmid: str) -> dict | None:
    try:
        handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="xml")
        records = Entrez.read(handle)
        handle.close()
        article  = records["PubmedArticle"][0]
        medline  = article["MedlineCitation"]
        title    = str(medline["Article"]["ArticleTitle"])
        abstract_texts = medline["Article"].get("Abstract", {}).get("AbstractText", [])
        abstract = " ".join(str(a) for a in abstract_texts)
        if not abstract:
            return None
        return {
            "pmid": pmid,
            "full_text": f"[TITLE] {title}\n\n[ABSTRACT] {abstract}",
            "source": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "is_full_text": False,
        }
    except Exception:
        return None


def fetch_documents(pmids: list[str]) -> list[dict]:
    docs = []
    for i, pmid in enumerate(pmids):
        doc = fetch_full_text(pmid) or fetch_abstract_fallback(pmid)
        if doc:
            docs.append(doc)
        time.sleep(0.4)
        if (i + 1) % 20 == 0:
            print(f"  fetched {i+1}/{len(pmids)}")
    return docs


# --- Chunking (from friend's chunker.py) ---

def chunk_documents(documents: list[dict]) -> list[dict]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " "],
    )
    chunks = []
    for doc in documents:
        for i, text in enumerate(splitter.split_text(doc["full_text"])):
            chunks.append({
                "text": text,
                "metadata": {
                    "pmid": doc["pmid"],
                    "source": doc["source"],
                    "is_full_text": doc["is_full_text"],
                    "chunk_index": i,
                },
            })
    return chunks


# --- Store into Chroma (langchain_chroma, matches backend) ---

def store_chunks(chunks: list[dict]) -> int:
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
    texts     = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids       = [f"{c['metadata']['pmid']}_chunk_{c['metadata']['chunk_index']}" for c in chunks]

    batch_size = 100
    for i in range(0, len(texts), batch_size):
        vector_store.add_texts(
            texts=texts[i:i+batch_size],
            metadatas=metadatas[i:i+batch_size],
            ids=ids[i:i+batch_size],
        )
        print(f"  stored batch {i//batch_size + 1}/{-(-len(texts)//batch_size)}")

    return vector_store._collection.count()


# --- Main ---

if __name__ == "__main__":
    if not EMAIL:
        raise SystemExit("Set PUBMED_EMAIL in .env before running.")

    all_docs: list[dict] = []
    for query in QUERIES:
        print(f"\nSearching: {query}")
        pmids = search_pubmed(query, MAX_RESULTS_PER_QUERY)
        print(f"  found {len(pmids)} PMIDs — fetching...")
        all_docs.extend(fetch_documents(pmids))

    # deduplicate
    seen: set[str] = set()
    unique_docs = [d for d in all_docs if not (d["pmid"] in seen or seen.add(d["pmid"]))]
    print(f"\nUnique documents: {len(unique_docs)}")

    chunks = chunk_documents(unique_docs)
    print(f"Total chunks: {len(chunks)}")

    print("\nStoring in ChromaDB...")
    total = store_chunks(chunks)
    print(f"\nDone — {total} chunks in collection '{COLLECTION}' at '{CHROMA_DIR}'")
