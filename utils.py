import time
import os
from typing import Optional, Any, Dict
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class RateLimitError(Exception):
    """Custom exception for rate limit errors"""
    pass


class ModelSwitchError(Exception):
    """Custom exception for model switching errors"""
    pass


def retry_with_model_fallback(max_retries: int = 3, retry_delay: int = 2, model_list: list = None):
    """
    Decorator to handle rate limits by automatically switching between models
    
    Args:
        max_retries: Maximum number of retry attempts
        retry_delay: Delay in seconds between retries
        model_list: List of models to try in order
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    error_str = str(e).lower()
                    
                    # Check if it's a rate limit error
                    is_rate_limit = any(keyword in error_str for keyword in 
                                       ['rate_limit', '429', 'quota', 'exceeded', 'too many'])
                    
                    if is_rate_limit:
                        last_error = e
                        logger.warning(f"Rate limit hit (attempt {attempt + 1}/{max_retries}): {e}")
                        
                        if attempt < max_retries - 1:
                            wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                            logger.info(f"Waiting {wait_time} seconds before retry...")
                            time.sleep(wait_time)
                            continue
                    
                    raise e
            
            if last_error:
                raise RateLimitError(f"Rate limit exceeded after {max_retries} retries: {last_error}")
        
        return wrapper
    return decorator


def handle_rate_limit_with_model_switch(func):
    """
    Decorator to switch models when rate limit is hit
    
    Args:
        func: Function that takes model parameter
    """
    def decorator(*args, **kwargs):
        from config import Config
        
        for model in Config.AVAILABLE_MODELS:
            try:
                logger.info(f"Attempting with model: {model}")
                return func(*args, model=model, **kwargs)
            except Exception as e:
                error_str = str(e).lower()
                is_rate_limit = any(keyword in error_str for keyword in 
                                   ['rate_limit', '429', 'quota', 'exceeded', 'too many'])
                
                if is_rate_limit:
                    logger.warning(f"Model {model} hit rate limit. Switching to next model...")
                    time.sleep(2)
                    continue
                else:
                    raise e
        
        raise ModelSwitchError("All models exhausted due to rate limits")
    
    return decorator


def ensure_faiss_index_exists(index_path: str) -> bool:
    """Check if FAISS index exists"""
    return os.path.exists(index_path) and os.path.exists(os.path.join(index_path, "index.faiss"))


def load_or_create_faiss_index(texts: list = None, embeddings = None, index_path: str = "faiss_index_store"):
    """
    Load existing FAISS index or create a new one
    
    Args:
        texts: List of texts to create index from
        embeddings: Embedding model
        index_path: Path to store/load index
    
    Returns:
        FAISS vector store
    """
    from langchain_community.vectorstores import FAISS
    
    if ensure_faiss_index_exists(index_path) and texts is None:
        try:
            logger.info(f"Loading existing FAISS index from {index_path}")
            return FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        except Exception as e:
            logger.warning(f"Failed to load existing index: {e}")
    
    if texts and embeddings:
        logger.info(f"Creating new FAISS index with {len(texts)} documents")
        return FAISS.from_texts(texts, embeddings)
    
    return None


def format_response(query: str, response: str, sources: list = None) -> Dict[str, Any]:
    """Format research response with metadata"""
    return {
        "query": query,
        "response": response,
        "sources": sources or [],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "word_count": len(response.split())
    }


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


def log_research_session(query: str, response: str, model_used: str = None):
    """Log research session for debugging"""
    logger.info(f"Query: {query[:100]}... | Model: {model_used} | Response length: {len(response)}")
