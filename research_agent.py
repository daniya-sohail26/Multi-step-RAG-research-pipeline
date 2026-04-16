import os
import time
import logging
import hashlib
import json
import re
from typing import Any, Dict, List
from config import Config, EMBEDDING_MODEL
from utils import (
    RateLimitError, 
    ModelSwitchError,
    load_or_create_faiss_index,
    format_response,
    log_research_session
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Request cache to prevent duplicate API calls
_REQUEST_CACHE: Dict[str, Any] = {}
_CACHE_FILE = "request_cache.json"
_CACHE_VERSION = "v3_deep_research_longform"

def _load_cache():
    """Load request cache from disk"""
    global _REQUEST_CACHE
    if os.path.exists(_CACHE_FILE):
        try:
            with open(_CACHE_FILE, 'r') as f:
                _REQUEST_CACHE = json.load(f)
        except:
            _REQUEST_CACHE = {}

def _save_cache():
    """Save request cache to disk"""
    try:
        with open(_CACHE_FILE, 'w') as f:
            json.dump(_REQUEST_CACHE, f)
    except Exception as e:
        logger.warning(f"Failed to save cache: {e}")

def _get_cache_key(text: str) -> str:
    """Generate cache key from text"""
    return hashlib.md5(f"{_CACHE_VERSION}:{text}".encode()).hexdigest()

def _cached_invoke(key: str, func, *args, **kwargs) -> Any:
    """Invoke function with caching"""
    if key in _REQUEST_CACHE:
        logger.info(f"✓ Cache hit - returning cached response")
        return _REQUEST_CACHE[key]
    
    result = func(*args, **kwargs)
    _REQUEST_CACHE[key] = result
    _save_cache()
    return result


class AgenticResearchAssistant:
    """Agentic AI Research Assistant with NO rate limits - uses local models"""
    
    def __init__(self):
        """Initialize the research assistant"""
        Config.validate()
        _load_cache()
        
        self.tavily_api_key = Config.TAVILY_API_KEY
        self.available_models = Config.AVAILABLE_MODELS
        self.current_model_index = 0
        self.vector_db = None
        self.embeddings = None
        self.search_tool = None
        self.llm = None
        self.conversation_history = []
        self.last_request_time = 0
        self.min_request_interval = 0.5  # Minimum time between requests (seconds)
        
        self._initialize_components()
        
    def _initialize_components(self):
        """Initialize all AI components"""
        try:
            from langchain_community.embeddings import OllamaEmbeddings
            from langchain_community.tools.tavily_search import TavilySearchResults

            logger.info("Initializing AI components...")

            # Initialize embeddings using Ollama to avoid torch/transformers issues.
            self.embeddings = OllamaEmbeddings(
                model=EMBEDDING_MODEL,
                base_url="http://localhost:11434"
            )

            # Initialize search tool with Tavily
            self.search_tool = TavilySearchResults(
                api_key=self.tavily_api_key,
                max_results=Config.MAX_SEARCH_RESULTS
            )

            # Initialize vector database; continue without it if embeddings are unavailable.
            try:
                self.vector_db = load_or_create_faiss_index(
                    embeddings=self.embeddings,
                    index_path=Config.FAISS_INDEX_PATH
                )
            except Exception as vector_error:
                logger.warning(f"Vector DB disabled due to embedding setup error: {vector_error}")
                self.vector_db = None

            # Initialize LLM with primary model
            self.llm = self._create_llm(self.available_models[0])

            logger.info("✓ AI components initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            raise
    
    def _create_llm(self, model: str):
        """Create a Language Model instance using Ollama (LOCAL, NO RATE LIMITS)"""
        from langchain_community.llms import Ollama
        
        try:
            # Use Ollama for local inference - NO RATE LIMITS
            logger.info(f"Connecting to Ollama model: {model}")
            
            # Ollama runs locally at http://localhost:11434
            llm = Ollama(
                model=model,
                base_url="http://localhost:11434",
                temperature=0.3
            )
            
            # Test connection
            try:
                test_response = llm.invoke("Say 'ready'")
                logger.info(f"✓ Connected to Ollama model: {model}")
            except Exception as e:
                logger.error(f"Failed to connect to Ollama. Make sure Ollama is running: {e}")
                logger.error(f"Download Ollama from https://ollama.ai and run: ollama pull {model}")
                raise
            
            return llm
        except Exception as e:
            logger.error(f"Failed to initialize Ollama model {model}: {e}")
            raise
    
    def _switch_model(self) -> bool:
        """
        Switch to the next available model on rate limit
        
        Returns:
            True if switch was successful, False if all models exhausted
        """
        self.current_model_index += 1
        
        if self.current_model_index >= len(self.available_models):
            logger.error("All models have been exhausted")
            return False
        
        current_model = self.available_models[self.current_model_index]
        logger.warning(f"Switching to model: {current_model}")
        
        try:
            self.llm = self._create_llm(current_model)
            return True
        except Exception as e:
            logger.error(f"Failed to switch to model {current_model}: {e}")
            return False
    
    def research(self, query: str, use_web_search: bool = True) -> Dict:
        """
        Conduct research with caching and throttling (NO RATE LIMITS)
        
        Args:
            query: Research topic or question
            use_web_search: Whether to perform web search
        
        Returns:
            Dictionary with query, response, and metadata
        """
        logger.info(f"Starting research on: {query}")
        self.conversation_history.append({"role": "user", "query": query})
        
        # Apply request throttling to prevent rate limits
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            logger.info(f"Throttling request - sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        
        sources: List[Dict[str, str]] = []

        try:
            # Check vector DB for similar past research first
            similar_docs = self._search_vector_db(query)
            
            if similar_docs and not use_web_search:
                logger.info("✓ Found similar research in vector DB - using cached result")
                response = similar_docs[0] if similar_docs else ""
            else:
                # Perform web search and summarization
                if use_web_search:
                    logger.info(f"🔍 Running deep web research for: {query}")

                    deep_queries = self._build_deep_queries(query)
                    collected_results: List[Dict[str, str]] = []

                    for deep_query in deep_queries:
                        search_cache_key = _get_cache_key(f"search:{deep_query}")
                        raw_results = _cached_invoke(
                            search_cache_key,
                            lambda dq=deep_query: self.search_tool.invoke(dq)
                        )
                        collected_results.extend(self._normalize_search_results(raw_results))

                    deduped = self._dedupe_sources(collected_results)
                    sources = deduped[:12]

                    if not sources:
                        response = "I could not gather enough web sources for this query. Please try a more specific query."
                    else:
                        search_text = self._build_research_context(sources)
                        summary_cache_key = _get_cache_key(f"summary:{query}:{search_text[:300]}")
                        response = _cached_invoke(
                            summary_cache_key,
                            lambda: self._summarize_results(query, search_text)
                        )
                else:
                    logger.info("📝 Generating response without web search")
                    gen_cache_key = _get_cache_key(f"gen:{query}")
                    response = _cached_invoke(
                        gen_cache_key,
                        lambda: self.llm.invoke(f"Answer this question: {query}")
                    )
            
            # Store in vector database
            self._store_in_vector_db(query, response)
            
            # Format and return response
            result = format_response(
                query=query,
                response=response,
                sources=sources
            )
            
            model_used = self.available_models[self.current_model_index]
            log_research_session(query, response, model_used)
            self.conversation_history.append({"role": "assistant", "response": response})
            
            return result
                
        except Exception as e:
            logger.error(f"Research error: {e}")
            raise

    def _build_deep_queries(self, query: str) -> List[str]:
        """Expand one question into multiple web-research subqueries."""
        return [
            query,
            f"{query} key features and architecture",
            f"{query} benefits limitations and challenges",
            f"{query} best practices implementation examples",
            f"{query} pricing comparison alternatives",
            f"{query} real world case study",
            f"{query} latest trends 2025 2026",
        ]

    def _normalize_search_results(self, raw_results: Any) -> List[Dict[str, str]]:
        """Normalize Tavily tool output into a standard source schema."""
        normalized: List[Dict[str, str]] = []

        if isinstance(raw_results, dict):
            candidates = raw_results.get("results", [])
        elif isinstance(raw_results, list):
            candidates = raw_results
        else:
            candidates = []

        for item in candidates:
            if not isinstance(item, dict):
                continue
            url = str(item.get("url", "")).strip() or str(item.get("link", "")).strip() or str(item.get("href", "")).strip()
            title = str(item.get("title", "")).strip() or "Untitled Source"
            snippet = str(item.get("content", "")).strip() or str(item.get("snippet", "")).strip()

            if not url:
                continue
            normalized.append({
                "title": title,
                "url": url,
                "snippet": snippet[:700]
            })

        return normalized

    def _dedupe_sources(self, sources: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Deduplicate source list by URL while preserving first-seen ordering."""
        deduped: List[Dict[str, str]] = []
        seen_urls = set()

        for source in sources:
            url = source.get("url", "")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            deduped.append(source)

        return deduped

    def _build_research_context(self, sources: List[Dict[str, str]]) -> str:
        """Build structured context block for synthesis prompt."""
        blocks = []
        for i, source in enumerate(sources, start=1):
            blocks.append(
                f"[{i}] Title: {source['title']}\n"
                f"URL: {source['url']}\n"
                f"Excerpt: {source['snippet']}"
            )
        return "\n\n".join(blocks)
    
    def _search_vector_db(self, query: str) -> List[str]:
        """Search vector database for similar research"""
        if not self.vector_db:
            return []
        
        try:
            results = self.vector_db.similarity_search(query, k=2)
            return [doc.page_content for doc in results]
        except Exception as e:
            logger.warning(f"Vector DB search failed: {e}")
            return []
    
    def _store_in_vector_db(self, query: str, response: str):
        """Store research results in vector database"""
        if not self.vector_db or not self.embeddings:
            return
        
        try:
            from langchain_community.vectorstores import FAISS
            
            combined_text = f"Query: {query}\n\nResponse: {response}"
            
            if self.vector_db:
                self.vector_db.add_texts([combined_text])
            else:
                self.vector_db = FAISS.from_texts([combined_text], self.embeddings)
            
            self.vector_db.save_local(Config.FAISS_INDEX_PATH)
            logger.info("✓ Research stored in vector DB")
        except Exception as e:
            logger.warning(f"Failed to store in vector DB: {e}")
    
    def _summarize_results(self, query: str, search_results: str) -> str:
        """Summarize search results using LLM"""
        try:
            summary_prompt = f"""
            You are a deep-research analyst. Based on the web sources below, produce a detailed report.

            User Query: {query}

            Requirements:
            1. Write 1200-2500 words.
            2. Cover: overview, core features, implementation patterns, risks, recommendations, and an action plan.
            3. Cite evidence using bracket references like [1], [2] mapped to the source numbers below.
            4. If sources disagree, explicitly note the disagreement.
            5. Keep claims grounded in the provided source excerpts.
            6. Output must be clean Markdown with these exact sections:
               # Executive Summary
               # Key Findings
               # Feature Breakdown
               # Implementation Guidance
               # Risks and Trade-offs
               # Recommendations
               # Final Verdict
            7. Do NOT append a raw 'Sources' dump. Use inline citations only.

            Sources:
            {search_results}

            Deep Research Report:
            """
            
            response = self.llm.invoke(summary_prompt)
            if not response:
                return "No summary available"

            cleaned = self._clean_report(str(response))
            final_report = self._expand_if_too_short(query, search_results, cleaned)
            return final_report[:Config.SUMMARY_LENGTH]
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return search_results[:Config.SUMMARY_LENGTH]

    def _clean_report(self, report: str) -> str:
        """Normalize markdown and remove noisy source dumps from model output."""
        text = report.strip()

        # Remove common trailing raw sources blocks if the model emits them.
        text = re.sub(r"\n#{0,3}\s*Sources\s*\n[\s\S]*$", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\n📎\s*Sources\s*\n[\s\S]*$", "", text, flags=re.IGNORECASE)

        # Ensure there is at least one top-level heading for good UI rendering.
        if not text.startswith("#"):
            text = "# Executive Summary\n\n" + text

        return text

    def _expand_if_too_short(self, query: str, search_results: str, report: str) -> str:
        """Ask for continuation if report is too short for deep-research quality."""
        word_count = len(report.split())
        if word_count >= 900:
            return report

        continuation_prompt = f"""
        Continue and deepen the report below for query: {query}

        Existing Report:
        {report}

        Additional Source Context:
        {search_results}

        Requirements:
        - Add 700-1400 more words.
        - Add concrete implementation details, examples, and decision criteria.
        - Keep Markdown section structure and citation style [n].
        - Do not repeat previous paragraphs verbatim.
        """

        try:
            continuation = self.llm.invoke(continuation_prompt)
            if continuation:
                return (report + "\n\n" + self._clean_report(str(continuation))).strip()
        except Exception as continuation_error:
            logger.warning(f"Continuation generation failed: {continuation_error}")

        return report
    
    def get_conversation_history(self) -> List[Dict]:
        """Get the conversation history"""
        return self.conversation_history
    
    def clear_conversation_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_vector_db_status(self) -> Dict:
        """Get status of vector database"""
        return {
            "initialized": self.vector_db is not None,
            "path": Config.FAISS_INDEX_PATH,
            "exists": os.path.exists(Config.FAISS_INDEX_PATH)
        }
    
    def get_model_status(self) -> Dict:
        """Get current model status and available models"""
        return {
            "current_model": self.available_models[self.current_model_index],
            "current_index": self.current_model_index,
            "available_models": self.available_models,
            "total_models": len(self.available_models)
        }
