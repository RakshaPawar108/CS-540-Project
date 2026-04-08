"""
Ingestion Pipeline — Person 1
Routes: /api/v1/ingestion/...
"""
from fastapi import APIRouter, Depends, HTTPException
from langchain_chroma import Chroma

from app.models.schemas import IngestionRequest, IngestionResponse, IngestionStatusResponse
from app.services import ingestion_service
from app.core.vector_store import get_vector_store
from app.config import get_settings, Settings

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])


@router.post("/ingest", response_model=IngestionResponse)
def ingest_pubmed(
    body: IngestionRequest,
    vector_store: Chroma = Depends(get_vector_store),
    settings: Settings = Depends(get_settings),
):
    """Fetch PubMed abstracts matching the query and store them in ChromaDB."""
    try:
        count = ingestion_service.ingest(
            query=body.query,
            max_results=body.max_results,
            vector_store=vector_store,
            email=settings.pubmed_email,
        )
        return IngestionResponse(status="completed", documents_ingested=count, message="Ingestion complete.")
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Ingestion not yet implemented.")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/status", response_model=IngestionStatusResponse)
def ingestion_status(
    vector_store: Chroma = Depends(get_vector_store),
    settings: Settings = Depends(get_settings),
):
    """Return current ChromaDB collection size and embedding model info."""
    count = ingestion_service.get_collection_count(vector_store)
    return IngestionStatusResponse(
        collection=settings.chroma_collection,
        document_count=count,
        embedding_model=settings.embedding_model,
    )
