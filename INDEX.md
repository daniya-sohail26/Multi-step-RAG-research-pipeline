# 🔬 Agentic AI Research Assistant - Complete Project Files

## 📚 Documentation Index

Welcome to your **Agentic AI Research Assistant**! This file guides you through the complete project structure and how to get started.

### 📖 Read These First

1. **[QUICKSTART.md](QUICKSTART.md)** ⭐ START HERE
   - 5-minute setup guide
   - Step-by-step instructions
   - Common issues and fixes
   - One-line Windows setup

2. **[README.md](README.md)**
   - Complete documentation
   - Feature overview
   - API key setup
   - Troubleshooting guide
   - Performance tips
   - Rate limit explanation

3. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**
   - What's been built
   - Feature details
   - Architecture overview
   - Use cases
   - Key differentiators

---

## 🚀 Quick Start (Choose Your Path)

### ⚡ Windows Users (Easiest)
```bash
setup.bat
# Follow the prompts, then:
setup.bat run
```

### 🐍 Manual Setup (All Platforms)
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure .env
copy .env.example .env
# Edit .env with your API keys

# 5. Run
streamlit run app.py
```

---

## 📁 Project Structure

### Core Application Files

| File | Purpose | Description |
|------|---------|-------------|
| **app.py** | Main UI | Streamlit web interface with research UI |
| **research_agent.py** | Core Logic | AgenticResearchAssistant class with rate limit handling |
| **config.py** | Configuration | Settings management and validation |
| **utils.py** | Utilities | Helper functions, error handling, retry logic |

### Configuration Files

| File | Purpose |
|------|---------|
| **.env.example** | API key template |
| **requirements.txt** | Python dependencies |
| **.gitignore** | Git ignore rules |

### Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| **QUICKSTART.md** | Fast setup | Everyone |
| **README.md** | Complete docs | Developers |
| **PROJECT_SUMMARY.md** | Overview | Managers |
| **examples.py** | Code samples | Developers |
| **INDEX.md** | This file | Everyone |

### Setup Files

| File | Purpose |
|------|---------|
| **setup.bat** | Windows automated setup |

---

## 🎯 Key Features at a Glance

### ✨ Rate Limit Handling (Main Feature)
```
When you hit a rate limit on one model:
❌ Model 1 (gemini-pro) → Rate Limit
   ↓ Auto-switch
✓ Model 2 (gemini-1.5-pro) → Success!
```

**Available Models:**
- 🥇 Primary: `gemini-pro`
- 🥈 Secondary: `gemini-1.5-pro`
- 🥉 Fallback: `gemini-pro-vision`

### 🔍 Research Capabilities
- Real-time web search with Tavily
- Automatic result summarization
- Vector database caching with FAISS
- Conversation memory management
- Source tracking

### 🎨 User Interface
- Clean Streamlit design
- Real-time status updates
- Research history tracking
- Model status monitoring
- Built-in help documentation

---

## 📊 File-by-File Guide

### app.py - The Web Interface
**What it does:**
- Renders the Streamlit UI
- Handles user input
- Displays research results
- Manages session state
- Shows error messages

**When to edit:**
- Modify UI layout
- Change colors/themes
- Add new features
- Customize interface

### research_agent.py - The Brain
**What it does:**
- Initializes Gemini models
- Conducts research
- Switches models on rate limit
- Manages vector database
- Handles conversations

**Key class:** `AgenticResearchAssistant`

**Main methods:**
- `research()` - Conduct research
- `_switch_model()` - Handle rate limits
- `get_model_status()` - Check models
- `get_vector_db_status()` - Check database

### config.py - Settings Manager
**What it does:**
- Loads environment variables
- Validates API keys
- Defines constants
- Manages configurations

**Key class:** `Config`

**Variables:**
- API keys
- Model names
- Retry settings
- Database paths

### utils.py - Helper Functions
**What it does:**
- Retry logic with backoff
- Error handling
- Model switching helpers
- Vector DB operations
- Response formatting

**Key functions:**
- `retry_with_model_fallback()` - Decorator for retries
- `load_or_create_faiss_index()` - Vector DB management
- `format_response()` - Response formatting

### examples.py - Code Examples
**What it does:**
- Demonstrates how to use the assistant
- Shows different use cases
- Illustrates error handling
- Provides reference code

**Examples included:**
1. Basic research
2. Multiple queries
3. Model status checking
4. Error handling
5. Cache usage
6. Configuration
7. Web search control

---

## 🔑 API Key Setup

### Step 1: Get Google Gemini API Key
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the generated key

### Step 2: Get Tavily API Key
1. Visit: https://tavily.com/signup
2. Sign up (free tier available)
3. Go to dashboard
4. Copy your API key

### Step 3: Configure .env
```bash
# Copy template
copy .env.example .env

# Edit and add your keys
GOOGLE_API_KEY=paste-your-key-here
TAVILY_API_KEY=paste-your-key-here
```

---

## 🧪 Testing the Installation

### Quick Test
```bash
# Run the example
python examples.py

# Should show model status and attempt a query
```

### Full Test
```bash
# Start the app
streamlit run app.py

# In the browser:
# 1. Try a simple query
# 2. Check sidebar for model status
# 3. Try web search toggle
```

---

## ⚠️ Rate Limit Q&A

### Q: What happens when I hit a rate limit?
**A:** The system automatically:
1. Detects the rate limit error
2. Logs a warning
3. Switches to the next model
4. Waits 2-8 seconds (with backoff)
5. Retries the research

### Q: If one model hits a rate limit, can I use another?
**A:** YES! This is the main feature:
- You don't need to do anything
- System automatically switches
- Up to 3 models are tried
- Each model has its own quota

### Q: Which model should I use?
**A:** The system tries them in order:
1. `gemini-pro` (15 req/min free tier)
2. `gemini-1.5-pro` (2 req/min free tier)
3. `gemini-pro-vision` (15 req/min free tier)

### Q: How do I avoid rate limits?
**A:**
1. Use "Cache First" option
2. Space out requests
3. Use specific queries
4. Upgrade to paid plan
5. Use off-peak times

### Q: What if all models hit limits?
**A:**
1. System returns cached results
2. Shows friendly error message
3. Suggests waiting 15-30 minutes
4. Logs the error

---

## 🆘 Troubleshooting

### "API key not set"
```bash
# Check .env file exists
dir | findstr ".env"

# Check API keys are present
type .env | findstr "API_KEY"

# Restart app
streamlit run app.py
```

### "Rate limit exceeded after retries"
```bash
# Wait 15-30 minutes
# Or upgrade to paid plan
# Or try different queries

# Check model status in sidebar
```

### "Module not found"
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Restart Python/shell
```

### "Port 8501 already in use"
```bash
# Use different port
streamlit run app.py --server.port 8502
```

---

## 📈 Performance Tips

### For Faster Results
1. ✓ Use "Cache First" option
2. ✓ Ask specific questions
3. ✓ Disable web search for known topics
4. ✓ Use during off-peak hours

### To Avoid Rate Limits
1. ✓ Space queries (30 sec apart)
2. ✓ Use cached results
3. ✓ Upgrade to paid plan
4. ✓ Batch similar queries

### For Better Results
1. ✓ Be specific in queries
2. ✓ Use technical terms
3. ✓ Ask follow-up questions
4. ✓ Review sources

---

## 🔄 Update & Maintenance

### Check for Updates
```bash
# Requirements may change
pip install --upgrade -r requirements.txt

# Check new Gemini models
# Visit: https://ai.google.dev
```

### Clear Cache
```bash
# Delete vector database
rmdir /s faiss_index_store

# Fresh index created on next search
```

### View Logs
```bash
# Check console output for debugging
# Logs show model switches, errors, etc.
```

---

## 📚 Additional Resources

### Documentation
- [Full README](README.md)
- [Quick Start Guide](QUICKSTART.md)
- [Project Summary](PROJECT_SUMMARY.md)
- [Code Examples](examples.py)

### External Resources
- [Google Gemini API Docs](https://ai.google.dev)
- [LangChain Documentation](https://docs.langchain.com)
- [Streamlit Docs](https://docs.streamlit.io)
- [FAISS Guide](https://faiss.ai)
- [Tavily API Docs](https://tavily.com/docs)

### Related Projects
- [LangChain Examples](https://github.com/langchain-ai/langchain)
- [Streamlit Showcase](https://streamlit.io/gallery)
- [FAISS Tutorials](https://github.com/facebookresearch/faiss)

---

## 🎓 Learning Path

### Beginner
1. Read QUICKSTART.md
2. Run setup.bat
3. Try simple queries
4. Review results

### Intermediate
1. Read README.md
2. Check model status in sidebar
3. Explore advanced options
4. Try web search control

### Advanced
1. Review PROJECT_SUMMARY.md
2. Study code (app.py, research_agent.py)
3. Run examples.py
4. Modify configuration
5. Add custom models

### Expert
1. Extend research_agent.py
2. Add new tools/integrations
3. Customize rate limit handling
4. Deploy as production service

---

## ✅ Checklist Before First Use

- [ ] Python 3.8+ installed
- [ ] API keys obtained
- [ ] .env file configured
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] QUICKSTART.md read
- [ ] Streamlit running (`streamlit run app.py`)
- [ ] Browser opens to localhost:8501
- [ ] Can enter a query
- [ ] Results display successfully

---

## 🎉 You're Ready!

You now have a complete **Agentic AI Research Assistant** with:

✅ Automatic rate limit handling  
✅ Multi-model fallback system  
✅ Deep research capabilities  
✅ Clean UI interface  
✅ Complete documentation  
✅ Example code  

### Next Steps:
1. **Start with**: [QUICKSTART.md](QUICKSTART.md)
2. **Setup**: Run `setup.bat` (Windows) or manual setup
3. **Configure**: Add your API keys to `.env`
4. **Launch**: `streamlit run app.py`
5. **Research**: Start exploring!

---

## 📞 Quick Links

| Need | Go To |
|------|-------|
| Fast setup | [QUICKSTART.md](QUICKSTART.md) |
| Full docs | [README.md](README.md) |
| What's built | [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) |
| Code examples | [examples.py](examples.py) |
| API keys | https://makersuite.google.com/app/apikey |
| Web search key | https://tavily.com |
| Support | Sidebar → Help & Rate Limits |

---

**Happy Researching! 🔬**

*Built with ❤️ using Gemini, LangChain, and Streamlit*

**Last Updated:** April 16, 2026
