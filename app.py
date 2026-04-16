import streamlit as st
import logging
from research_agent import AgenticResearchAssistant
from utils import RateLimitError, ModelSwitchError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Clean and minimal
st.markdown("""
    <style>
    .main {
        max-width: 900px;
    }
    .header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .subheader {
        font-size: 1rem;
        color: #999;
        text-align: center;
        margin-bottom: 2rem;
    }
    .search-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 1.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15);
    }
    .result-box {
        background: white;
        padding: 2rem;
        border-radius: 1rem;
        border-left: 4px solid #667eea;
        margin: 1.5rem 0;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }
    .result-header {
        font-size: 0.95rem;
        color: #667eea;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .source-chip {
        background: #eef2ff;
        border: 1px solid #dbe4ff;
        border-radius: 0.6rem;
        padding: 0.55rem 0.8rem;
        margin: 0.4rem 0;
    }
    .error-box {
        background: #fff5f5;
        border-left: 4px solid #f56565;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
    }
    .success-box {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1.5rem;
        border-radius: 0.75rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Session state
if "assistant" not in st.session_state:
    st.session_state.assistant = None
    st.session_state.initialized = False

if "results" not in st.session_state:
    st.session_state.results = []


def initialize_assistant():
    """Initialize research assistant"""
    try:
        st.session_state.assistant = AgenticResearchAssistant()
        st.session_state.initialized = True
        return True
    except Exception as e:
        logger.error(f"Init failed: {e}")
        return False


# Header
st.markdown('<div class="header">🔬</div>', unsafe_allow_html=True)
st.markdown('<div class="header">AI Research</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Deep web research with intelligent summarization</div>', 
           unsafe_allow_html=True)

# Initialize if needed
if not st.session_state.initialized:
    with st.spinner("🚀 Starting research engine..."):
        if not initialize_assistant():
            st.markdown("""
            <div class="error-box">
            <strong>⚠️ Configuration Required</strong><br/>
            
            <strong>Step 1: Install Ollama</strong><br/>
            Download and install from <a href="https://ollama.ai" target="_blank">https://ollama.ai</a>
            
            <strong>Step 2: Download Models</strong><br/>
            Open terminal and run:
            <pre>ollama pull mistral
ollama pull neural-chat
ollama pull orca-mini</pre>
            
            <strong>Step 3: Start Ollama</strong><br/>
            Run: <code>ollama serve</code>
            
            <strong>Step 4: Get Tavily API Key</strong><br/>
            Sign up at <a href="https://tavily.com/signup" target="_blank">https://tavily.com/signup</a>
            
            <strong>Step 5: Update .env</strong><br/>
            <pre>TAVILY_API_KEY=your-key</pre>
            
            <strong>Step 6: Refresh this page (F5)</strong>
            </div>
            """, unsafe_allow_html=True)
            st.stop()

# Search interface
st.markdown('<div class="search-box">', unsafe_allow_html=True)

col1, col2 = st.columns([4.5, 0.5])
with col1:
    query = st.text_input(
        "What would you like to research?",
        placeholder="E.g., Latest AI breakthroughs | Quantum computing applications",
        label_visibility="collapsed"
    )
with col2:
    search_btn = st.button("🚀", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Handle search
if search_btn and query:
    placeholder = st.empty()
    
    try:
        with placeholder.container():
            st.info("🔍 Researching across the web...")
        
        # Get research
        result = st.session_state.assistant.research(query, use_web_search=True)
        
        placeholder.empty()
        
        # Show results
        model_status = st.session_state.assistant.get_model_status()
        st.markdown(f'<div class="result-header">✓ Research complete • {model_status["current_model"]} • {result["word_count"]} words</div>', 
                   unsafe_allow_html=True)

        # Content
        st.markdown(result["response"])
        
        # Sources
        if result.get("sources"):
            st.divider()
            st.subheader("Sources")
            for idx, source in enumerate(result["sources"], start=1):
                if isinstance(source, dict):
                    title = source.get("title", f"Source {idx}")
                    url = source.get("url", "")
                    snippet = source.get("snippet", "")
                    st.markdown('<div class="source-chip">', unsafe_allow_html=True)
                    if url:
                        st.markdown(f"{idx}. [{title}]({url})")
                    else:
                        st.markdown(f"{idx}. {title}")
                    if snippet:
                        st.caption(snippet[:220] + ("..." if len(snippet) > 220 else ""))
                    st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.caption(f"{idx}. {str(source)}")
        
        # Save to history
        st.session_state.results.append(query)
        
    except RateLimitError:
        placeholder.empty()
        st.markdown("""
        <div class="error-box">
        <strong>⚠️ Rate Limit Exceeded</strong><br/>
        All AI models hit their limits. Wait 15-30 minutes or upgrade your plan.
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        placeholder.empty()
        logger.error(f"Error: {e}")
        st.markdown(f"""
        <div class="error-box">
        <strong>❌ Error</strong><br/>
        {str(e)[:150]}
        </div>
        """, unsafe_allow_html=True)

elif search_btn:
    st.warning("📝 Please enter a research query")

# History
if st.session_state.results:
    with st.expander(f"📚 History ({len(st.session_state.results)})"):
        for i, q in enumerate(reversed(st.session_state.results), 1):
            st.caption(f"{i}. {q[:70]}...")
