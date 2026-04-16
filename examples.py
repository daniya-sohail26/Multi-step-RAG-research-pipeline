"""
Example usage of the Agentic AI Research Assistant

This file demonstrates how to use the research_agent module directly
without the Streamlit UI, useful for automation and integration.
"""

from research_agent import AgenticResearchAssistant
from utils import RateLimitError, ModelSwitchError
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def example_basic_research():
    """Example 1: Basic research query"""
    print("=" * 60)
    print("Example 1: Basic Research Query")
    print("=" * 60)
    
    try:
        # Initialize assistant
        assistant = AgenticResearchAssistant()
        print("✓ Assistant initialized")
        
        # Conduct research
        query = "What are the latest advances in artificial intelligence?"
        print(f"\nResearching: {query}")
        
        result = assistant.research(query)
        
        print("\n--- Results ---")
        print(f"Query: {result['query']}")
        print(f"Response: {result['response'][:200]}...")
        print(f"Word Count: {result['word_count']}")
        print(f"Timestamp: {result['timestamp']}")
        
    except RateLimitError as e:
        print(f"❌ Rate Limit Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_multiple_queries():
    """Example 2: Multiple queries with conversation memory"""
    print("\n" + "=" * 60)
    print("Example 2: Multiple Queries")
    print("=" * 60)
    
    try:
        assistant = AgenticResearchAssistant()
        
        queries = [
            "What is machine learning?",
            "How is it used in healthcare?",
            "What are its limitations?"
        ]
        
        for i, query in enumerate(queries, 1):
            print(f"\nQuery {i}: {query}")
            result = assistant.research(query)
            print(f"Response: {result['response'][:150]}...")
        
        # Get conversation history
        history = assistant.get_conversation_history()
        print(f"\n✓ Conversation history: {len(history)} exchanges")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_model_status():
    """Example 3: Check model status and available models"""
    print("\n" + "=" * 60)
    print("Example 3: Model Status")
    print("=" * 60)
    
    try:
        assistant = AgenticResearchAssistant()
        
        # Get model status
        status = assistant.get_model_status()
        print(f"Current Model: {status['current_model']}")
        print(f"Current Index: {status['current_index']}")
        print(f"Available Models:")
        for i, model in enumerate(status['available_models']):
            marker = "→" if i == status['current_index'] else " "
            print(f"  {marker} {model}")
        
        # Get vector DB status
        db_status = assistant.get_vector_db_status()
        print(f"\nVector DB Status:")
        print(f"  Initialized: {db_status['initialized']}")
        print(f"  Path: {db_status['path']}")
        print(f"  Exists: {db_status['exists']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_error_handling():
    """Example 4: Handle rate limit errors gracefully"""
    print("\n" + "=" * 60)
    print("Example 4: Error Handling")
    print("=" * 60)
    
    try:
        assistant = AgenticResearchAssistant()
        
        # Simulate rapid requests that might trigger rate limits
        queries = [
            "AI trends 2024",
            "Quantum computing",
            "Neural networks",
        ]
        
        successful = 0
        failed = 0
        
        for query in queries:
            try:
                result = assistant.research(query)
                successful += 1
                print(f"✓ {query}: Success")
            except RateLimitError as e:
                failed += 1
                print(f"❌ {query}: Rate limit - {str(e)[:50]}...")
            except Exception as e:
                failed += 1
                print(f"❌ {query}: Error - {str(e)[:50]}...")
        
        print(f"\nSummary: {successful} successful, {failed} failed")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_cache_usage():
    """Example 5: Use vector DB cache"""
    print("\n" + "=" * 60)
    print("Example 5: Vector DB Caching")
    print("=" * 60)
    
    try:
        assistant = AgenticResearchAssistant()
        
        # First query - will search web
        print("Query 1: Research on machine learning")
        result1 = assistant.research("machine learning basics")
        print(f"✓ Completed in 1st attempt")
        
        # Similar query - might use cache
        print("\nQuery 2: Similar query about machine learning")
        result2 = assistant.research("machine learning fundamentals")
        print(f"✓ Completed")
        
        print("\n(Check timestamps and response similarity)")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def example_custom_configuration():
    """Example 6: Using custom configuration"""
    print("\n" + "=" * 60)
    print("Example 6: Custom Configuration Info")
    print("=" * 60)
    
    from config import Config
    
    print("Current Configuration:")
    print(f"  Primary Model: {Config.PRIMARY_MODEL}")
    print(f"  Secondary Model: {Config.SECONDARY_MODEL}")
    print(f"  Fallback Model: {Config.FALLBACK_MODEL}")
    print(f"  Max Retries: {Config.MAX_RETRIES}")
    print(f"  Retry Delay: {Config.RETRY_DELAY}s")
    print(f"  Max Search Results: {Config.MAX_SEARCH_RESULTS}")
    print(f"  Summary Length: {Config.SUMMARY_LENGTH}")
    print(f"  FAISS Index Path: {Config.FAISS_INDEX_PATH}")


def example_web_search_control():
    """Example 7: Control web search behavior"""
    print("\n" + "=" * 60)
    print("Example 7: Web Search Control")
    print("=" * 60)
    
    try:
        assistant = AgenticResearchAssistant()
        
        # With web search
        print("Query with web search enabled:")
        result1 = assistant.research("Recent AI breakthroughs", use_web_search=True)
        print(f"✓ Completed with web search")
        
        # Without web search (use cache/knowledge only)
        print("\nQuery without web search (cached knowledge only):")
        result2 = assistant.research("What is AI?", use_web_search=False)
        print(f"✓ Completed without web search")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Run all examples"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║  Agentic AI Research Assistant - Usage Examples          ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    examples = [
        ("Basic Research", example_basic_research),
        ("Multiple Queries", example_multiple_queries),
        ("Model Status", example_model_status),
        ("Error Handling", example_error_handling),
        ("Cache Usage", example_cache_usage),
        ("Configuration", example_custom_configuration),
        ("Web Search Control", example_web_search_control),
    ]
    
    print("\nAvailable Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    # Check if .env is configured
    if not os.getenv("GOOGLE_API_KEY") or not os.getenv("SERPAPI_API_KEY"):
        print("\n⚠️  Warning: API keys not configured!")
        print("   Please set GOOGLE_API_KEY and SERPAPI_API_KEY in .env file")
        print("   Examples will not work without valid API keys")
        return
    
    # Run example 1 and 3 by default
    print("\n📚 Running Example 1 & 3...")
    try:
        example_basic_research()
        example_model_status()
    except Exception as e:
        print(f"Error running examples: {e}")
    
    print("\n✓ Examples complete!")
    print("\nTo run other examples, modify main() function or import directly")


if __name__ == "__main__":
    main()
