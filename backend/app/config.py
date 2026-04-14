from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # LLM
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.0

    # Embeddings — sentence-transformers/all-MiniLM-L6-v2 (runs locally, no API key)
    embedding_model: str = "all-MiniLM-L6-v2"
    embedding_dim: int = 384

    # ChromaDB
    chroma_persist_dir: str = "./chroma_db"
    chroma_collection: str = "pubmed_abstracts"

    # PubMed ingestion
    pubmed_email: str = ""          # required by NCBI Entrez
    pubmed_max_results: int = 500

    # Multi-turn conversation
    max_history_turns: int = 10     # pairs of (user, assistant) to keep

    # LangSmith tracing
    langsmith_api_key: str = ""
    langchain_tracing_v2: str = "false"
    langchain_project: str = "cs540-medical-chatbot"
    langchain_endpoint: str = "https://api.smith.langchain.com"


@lru_cache
def get_settings() -> Settings:
    return Settings()
