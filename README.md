## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Add your `.env` file with `NCBI_EMAIL=your@email.com`
3. Build the vector database (run once): `python ingest.py`
4. Test retrieval: `python retriever.py`

## Usage (after setup)

from vector_store import load_vector_store
from retriever import retrieve

collection = load_vector_store()
results = retrieve("your medical question here", collection)
