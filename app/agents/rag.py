from qdrant_client import QdrantClient
from app.agents.state import AgentState
from app.config import settings

def fetch_policy_context(state: AgentState) -> dict:
    try:
        # Connect to Qdrant vector database
        client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)
        
        # In production: Run embeddings search against client.search()
        # Fallback simulation rule for demo:
        retrieved_rules = (
            "1. All DB queries must use parameterized execution.\n"
            "2. External HTTP calls require circuit breakers and a 5s timeout.\n"
            "3. Sensitive environment variables must be loaded through Secret Manager."
        )
    except Exception:
        retrieved_rules = "Default Policy: Ensure clean code, error handling, and unit test coverage."

    return {"policy_context": retrieved_rules}