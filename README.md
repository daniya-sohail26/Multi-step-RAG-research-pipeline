# 🔬 Agentic AI Research Assistant

An intelligent research assistant powered by Google Gemini with **automatic rate limit handling and multi-model fallback** capabilities. Conduct deep research with web search, semantic caching, and conversation memory.

## ✨ Key Features

### 🤖 AI Capabilities
- **Web Search Integration**: Conducts real-time web searches using Tavily
- **Intelligent Summarization**: Automatically summarizes research findings
- **Conversation Memory**: Maintains context across multiple queries
- **Semantic Caching**: Stores and retrieves similar past research

### 🔄 Rate Limit Handling
- **Automatic Model Switching**: Seamlessly switches between Gemini models when one hits rate limits
- **Available Models**:
  - 🥇 Primary: `gemini-pro`
  - 🥈 Secondary: `gemini-1.5-pro`
  - 🥉 Fallback: `gemini-pro-vision`
- **Exponential Backoff**: Intelligent retry mechanism with increasing delays
- **Graceful Degradation**: Returns cached results if all models are exhausted

### 🎨 User Interface
- **Clean, Intuitive Design**: Built with Streamlit for easy interaction
- **Real-time Status Updates**: See which model is being used and processing status
- **Research History**: Track all previous queries
- **Advanced Analytics**: View metadata and metrics for each research session
- **Help Documentation**: Built-in guidance on rate limits and features

## 🛠️ Tech Stack

- **Python 3.8+**
- **Streamlit**: Interactive web interface
- **LangChain**: AI orchestration framework
- **Google Generative AI (Gemini)**: Primary LLM
- **FAISS**: Vector database for semantic search
- **Tavily**: Advanced web search API
- **python-dotenv**: Environment configuration

## 📋 Prerequisites

1. **Google API Key**
   - Get it from: https://makersuite.google.com/app/apikey
   - Free tier available with quota limits

2. **Tavily API Key**
   - Get it from: https://tavily.com
   - Free tier available with search quota

3. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/

## 🚀 Installation

### 1. Clone or Setup the Project

```bash
cd d:\AI-RESEARCH-AGENT-PROJECT
```

### 2. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy `.env.example` to `.env`:
```bash
copy .env.example .env
```

2. Edit `.env` and add your API keys:
```
GOOGLE_API_KEY=your-google-api-key-here
TAVILY_API_KEY=your-tavily-api-key-here
PRIMARY_MODEL=gemini-pro
SECONDARY_MODEL=gemini-1.5-pro
FALLBACK_MODEL=gemini-pro-vision
MAX_RETRIES=3
RETRY_DELAY=2
```

## ▶️ Running the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 📖 How to Use

### Basic Usage

1. **Enter a Research Topic**: Type your question in the input field
   - Example: "Latest advances in quantum computing"

2. **Configure Options**:
   - ✓ **Use Web Search**: Enable/disable web search
   - ✓ **Use Cache First**: Check cached results before searching

3. **Start Research**: Click the "🚀 Research" button

4. **View Results**: Results appear with:
   - Summary of findings
   - Metadata and word count
   - Research history tracking

### Advanced Options

Click "Show Advanced Options" to configure:
- Maximum retry attempts (1-5)
- Retry delay in seconds (1-5)

## 🔄 Understanding Rate Limit Handling

### When Rate Limit Is Hit

1. **Detection**: System detects 429 errors or quota exceeded messages
2. **Logging**: Detailed warning logged with model name
3. **Fallback**: Automatically switches to next available model
4. **Retry**: Waits with exponential backoff (2s, 4s, 8s...)
5. **Success**: Research continues with new model
6. **Exhaustion**: If all models fail, graceful error message

### Example Flow

```
Query: "Deep learning in healthcare"
  ↓
Try gemini-pro → Rate Limit Hit ⚠️
  ↓
Wait 2 seconds...
  ↓
Switch to gemini-1.5-pro ✓
  ↓
Success! Research completed
```

### Rate Limit Quotas (as of 2024)

| Model | Free Tier Quota | Premium |
|-------|-----------------|---------|
| gemini-pro | 15 requests/min | Higher |
| gemini-1.5-pro | 2 requests/min | Higher |
| gemini-pro-vision | 15 requests/min | Higher |

⚠️ **Note**: Quotas change frequently. Check [Google AI documentation](https://ai.google.dev) for latest limits.

## 📁 Project Structure

```
d:\AI-RESEARCH-AGENT-PROJECT\
├── app.py                  # Main Streamlit application
├── research_agent.py       # Core research agent logic
├── config.py              # Configuration management
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment variables
├── README.md              # This file
└── faiss_index_store/     # Vector database (created on first run)
    ├── index.faiss
    ├── index.pkl
    └── docstore.pkl
```

## 🔧 Configuration

### Environment Variables

```env
# Required
GOOGLE_API_KEY=sk-...
SERPAPI_API_KEY=sk-...

# Optional
PRIMARY_MODEL=gemini-pro
SECONDARY_MODEL=gemini-1.5-pro
FALLBACK_MODEL=gemini-pro-vision
MAX_RETRIES=3
RETRY_DELAY=2
```

### Model Configuration

Edit models in `.env` to customize fallback order:

```env
PRIMARY_MODEL=gemini-1.5-pro      # Try this first
SECONDARY_MODEL=gemini-pro         # Try this second
FALLBACK_MODEL=gemini-pro-vision   # Try this last
```

## 🐛 Troubleshooting

### "GOOGLE_API_KEY not set"

**Solution**: Check that `.env` file exists and contains your API key

```bash
# Check if .env exists
dir | findstr ".env"

# View .env content
type .env
```

### "Rate limit exceeded after X attempts"

**Solutions**:
1. Wait 15-30 minutes before trying again
2. Upgrade to a paid Google AI plan
3. Reduce MAX_RETRIES in `.env` for faster failure notification
4. Try again with different query to test other models

### "Module not found" errors

**Solution**: Reinstall dependencies

```bash
pip install --upgrade -r requirements.txt
```

### Vector DB Issues

**Solution**: Delete and recreate FAISS index

```bash
# Delete existing index
rmdir /s faiss_index_store

# Run app again to create fresh index
streamlit run app.py
```

## 📊 Monitoring & Debugging

### Enable Detailed Logging

Add to `app.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Sidebar Information

- **Model Information**: See current model and available fallbacks
- **Vector Database**: Check index status
- **Research History**: View all conducted queries
- **Rate Limit Help**: Built-in documentation

## 🔒 Privacy & Security

- ✓ All queries stored locally in FAISS vector DB
- ✓ No external data persistence
- ✓ API keys never logged or exposed
- ✓ Use `.gitignore` to exclude `.env` from version control

Recommended `.gitignore`:
```
.env
faiss_index_store/
__pycache__/
*.pyc
venv/
.streamlit/
```

## 🚀 Performance Tips

1. **Use Cache**: Enable "Use Cache First" to avoid web searches
2. **Specific Queries**: More specific questions get better results
3. **Monitor Models**: Check sidebar to see active model
4. **Batch Requests**: Group related queries for efficiency
5. **Off-Peak Usage**: Use during off-peak hours to avoid rate limits

## 🤝 Contributing

To improve this project:

1. Test different Gemini models
2. Report rate limit issues
3. Suggest UI improvements
4. Add new search tools (Bing, Google Scholar, etc.)

## 📚 Resources

- [Google Gemini API Docs](https://ai.google.dev)
- [LangChain Documentation](https://docs.langchain.com)
- [Streamlit Docs](https://docs.streamlit.io)
- [FAISS Documentation](https://faiss.ai)
- [Tavily API Docs](https://tavily.com/docs)

## 📝 License

MIT License - Feel free to use and modify

## 🆘 Getting Help

1. Check the built-in Help section in the sidebar
2. Review error messages in the UI
3. Check logs in console for detailed debugging
4. Verify API keys are valid
5. Test each API independently

## 🎯 Future Enhancements

- [ ] Support for more LLM providers (OpenAI, Claude, etc.)
- [ ] Document upload and analysis
- [ ] Multi-agent collaboration
- [ ] Speech-to-text input
- [ ] Export research to PDF
- [ ] Citation management
- [ ] Custom model fine-tuning
- [ ] Real-time collaborative research

## 📞 Support

For issues or questions:
1. Check the "Help & Rate Limits" section in sidebar
2. Review the troubleshooting guide above
3. Verify API credentials
4. Check model status in the UI

---

**Happy Researching! 🚀**

Built with ❤️ using Gemini, LangChain, and Streamlit
#   M u l t i - s t e p - R A G - r e s e a r c h - p i p e l i n e  
 