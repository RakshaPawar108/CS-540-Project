# pubmed_fetcher.py
import requests
import time
from Bio import Entrez
from dotenv import load_dotenv
import os

load_dotenv()
Entrez.email = os.environ["NCBI_EMAIL"]

def search_pubmed(query: str, max_results: int = 500) -> list[str]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

def fetch_full_text(pmid: str) -> dict | None:
    """
    Fetches full text via BioC API. Only works for Open Access papers.
    Falls back to abstract if full text unavailable.
    """
    url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmid}/unicode"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return None  # Not open access, will fall back to abstract
        
        data = response.json()
        
        # BioC format stores text in "passages" — each passage is a section
        # (Abstract, Introduction, Methods, Results, Discussion, etc.)
        sections = {}
        full_text_parts = []
        
        for document in data.get("documents", []):
            for passage in document.get("passages", []):
                section_type = passage.get("infons", {}).get("section_type", "unknown")
                text = passage.get("text", "").strip()
                
                if text:
                    full_text_parts.append(f"[{section_type}] {text}")
                    sections[section_type] = sections.get(section_type, "") + " " + text
        
        return {
            "pmid": pmid,
            "full_text": "\n\n".join(full_text_parts),
            "sections": sections,  # Useful for section-aware chunking later
            "source": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "is_full_text": True
        }
    
    except Exception:
        return None

def fetch_abstract_fallback(pmid: str) -> dict | None:
    """Fallback for papers not in PMC Open Access."""
    try:
        handle = Entrez.efetch(db="pubmed", id=pmid, rettype="abstract", retmode="xml")
        records = Entrez.read(handle)
        handle.close()
        
        article = records["PubmedArticle"][0]
        medline = article["MedlineCitation"]
        title = str(medline["Article"]["ArticleTitle"])
        abstract_texts = medline["Article"].get("Abstract", {}).get("AbstractText", [])
        abstract = " ".join([str(a) for a in abstract_texts])
        
        if not abstract:
            return None
        
        return {
            "pmid": pmid,
            "full_text": f"[TITLE] {title}\n\n[ABSTRACT] {abstract}",
            "sections": {"ABSTRACT": abstract},
            "source": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "is_full_text": False
        }
    except Exception:
        return None

def fetch_documents(pmids: list[str]) -> list[dict]:
    """Tries full text first, falls back to abstract."""
    documents = []
    full_text_count = 0
    
    for i, pmid in enumerate(pmids):
        doc = fetch_full_text(pmid)
        
        if doc:
            full_text_count += 1
        else:
            doc = fetch_abstract_fallback(pmid)
        
        if doc:
            documents.append(doc)
        
        time.sleep(0.4)  # Respect rate limits
        
        if (i + 1) % 50 == 0:
            print(f"Processed {i+1}/{len(pmids)} | Full text: {full_text_count}")
    
    print(f"\nDone. Full text: {full_text_count}/{len(documents)} papers")
    return documents

if __name__ == "__main__":
    pmids = search_pubmed("diabetes treatment", max_results=5)
    print("Found PMIDs:", pmids)
    docs = fetch_documents(pmids)
    for d in docs:
        print(d["pmid"], "| Full text:", d["is_full_text"])
        print(d["full_text"][:300])
        print("---")