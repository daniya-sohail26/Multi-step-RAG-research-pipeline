# Quick Start Guide 🚀

## One-Line Setup (Windows)

```batch
copy .env.example .env && python -m venv venv && call venv\Scripts\activate && pip install -r requirements.txt && streamlit run app.py
```

## Step-by-Step Setup

### 1. Get API Keys (5 minutes)

**Google Gemini API Key:**
1. Go to https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

**Tavily API Key:**
1. Go to https://tavily.com/signup
2. Sign up for free
3. Copy your API key from dashboard

### 2. Configure Environment

**Windows:**
```batch
copy .env.example .env
notepad .env
```

**macOS/Linux:**
```bash
cp .env.example .env
nano .env
```

Edit `.env` and paste your keys:
```
GOOGLE_API_KEY=your-key-here
TAVILY_API_KEY=your-key-here
```

### 3. Install Dependencies

**Windows:**
```batch
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Run Application

```bash
streamlit run app.py
```

Browser opens at: `http://localhost:8501`

## ✅ Verify Installation

1. **Check Python**:
   ```bash
   python --version
   ```
   Should show Python 3.8+

2. **Check Virtual Environment**:
   ```bash
   pip list
   ```
   Should show streamlit, langchain, etc.

3. **Test API Keys**:
   - Open app.py in browser
   - Check sidebar for "API Configuration"
   - Keys should show as configured

## 🧪 First Research Query

1. **Enter query**: "What is quantum computing?"
2. **Click**: 🚀 Research button
3. **Wait**: Processing takes 10-30 seconds
4. **View**: Results appear in Summary tab

## 🚨 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| `ModuleNotFoundError` | Run: `pip install -r requirements.txt` |
| `API key not set` | Check `.env` file exists with keys |
| `Rate limit error` | Wait 15 min or try different query |
| `Port 8501 in use` | Run: `streamlit run app.py --server.port 8502` |

## 📊 Rate Limit Handling Quick Reference

**If you hit a rate limit:**
- ✓ System automatically switches to next model
- ✓ Tries up to 3 models by default
- ✓ Waits 2, 4, 8 seconds between attempts
- ✓ Shows status in UI

**To avoid rate limits:**
1. Use "Cache First" option
2. Space out requests
3. Use specific, focused queries
4. Upgrade to paid Google AI plan

## 🎯 Next Steps

1. **Explore Features**:
   - Try web search toggle
   - Check vector DB status
   - Review rate limit settings

2. **Customize Models**:
   - Edit `.env` to change model order
   - Test different fallback combinations

3. **Scale Usage**:
   - Upgrade API quotas
   - Add more models to `.env`
   - Optimize queries

## 📚 Learn More

- [Full README](README.md)
- [Gemini API Docs](https://ai.google.dev)
- [Streamlit Docs](https://docs.streamlit.io)
- [LangChain Docs](https://docs.langchain.com)

---

**Need Help?** Check the Help section in the app sidebar!
