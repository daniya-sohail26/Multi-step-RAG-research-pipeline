import os
from dotenv import load_dotenv
from typing import List

# Load environment variables
load_dotenv()

class Config:
    """Configuration management for the AI Research Assistant"""
    
    # API Keys
    HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
    
    # Model Configuration (Ollama Models)
    PRIMARY_MODEL = os.getenv("PRIMARY_MODEL", "mistral")
    SECONDARY_MODEL = os.getenv("SECONDARY_MODEL", "neural-chat")
    FALLBACK_MODEL = os.getenv("FALLBACK_MODEL", "orca-mini")
    
    AVAILABLE_MODELS: List[str] = [PRIMARY_MODEL, SECONDARY_MODEL, FALLBACK_MODEL]
    
    # Rate Limiting
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY = int(os.getenv("RETRY_DELAY", "2"))
    
    # Vector DB
    FAISS_INDEX_PATH = "faiss_index_store"
    
    # Research Settings
    MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
    SUMMARY_LENGTH = int(os.getenv("SUMMARY_LENGTH", "4000"))
    
    @staticmethod
    def validate():
        """Validate that required API keys are set"""
        if not Config.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY not set in environment variables")


# Embedding model configuration (Ollama embedding model)
EMBEDDING_MODEL = "nomic-embed-text"
