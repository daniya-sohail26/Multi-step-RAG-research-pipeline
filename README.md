# Multi-step RAG Research Pipeline

A Streamlit-based deep research assistant that performs multi-query web retrieval, source deduplication, and long-form synthesis using local Ollama models.

## What This Project Is

This project is a multi-step retrieval-augmented generation (RAG) research pipeline.
It is tool-augmented and semi-agentic (query expansion + iterative synthesis), not a fully autonomous planning agent.

## Key Features

- Multi-query deep web research via Tavily
- Local LLM inference via Ollama (no hosted LLM rate limits)
- Source deduplication and citation-aware synthesis
- Long-form report generation in Markdown
- Streamlit UI with clickable source links
- Optional FAISS semantic cache with local embeddings
- Request caching and throttling to reduce repeated calls

## Current Architecture

1. User submits a query in Streamlit
2. Query is expanded into multiple targeted subqueries
3. Tavily returns web results for each subquery
4. Results are normalized and deduplicated by URL
5. Ollama model synthesizes a long-form report with citations
6. UI renders report and sources

## Tech Stack

- Python 3.10+
- Streamlit
- LangChain Community
- Ollama
- Tavily Search
- FAISS

## Prerequisites

1. Python installed
2. Ollama installed from https://ollama.com
3. Tavily API key from https://tavily.com

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

Copy environment template:

```bash
copy .env.example .env
```

Update `.env`:

```env
TAVILY_API_KEY=your_tavily_key_here
PRIMARY_MODEL=mistral
SECONDARY_MODEL=neural-chat
FALLBACK_MODEL=orca-mini
MAX_RETRIES=3
RETRY_DELAY=2
MAX_SEARCH_RESULTS=10
SUMMARY_LENGTH=4000
```

### 3. Pull Ollama models

```bash
ollama pull mistral
ollama pull neural-chat
ollama pull orca-mini
ollama pull nomic-embed-text
```

### 4. Start app

```bash
streamlit run app.py
```

Open http://localhost:8501

## GitHub Rendering Note

If your README previously rendered as plain text, it was likely due to file encoding corruption (null-byte content).
This README has been rewritten cleanly and should render correctly on GitHub.

## Recommended .gitignore

```gitignore
.env
__pycache__/
*.pyc
faiss_index_store/
request_cache.json
.streamlit/
venv/
```

## Troubleshooting

### Ollama port already in use

Error:

`listen tcp 127.0.0.1:11434: bind: Only one usage of each socket address`

Meaning: Ollama is already running. Do not start `ollama serve` again in another terminal.

### Short answers

Increase these values in `.env`:

```env
MAX_SEARCH_RESULTS=12
SUMMARY_LENGTH=6000
```

### No sources shown

Ensure Tavily key is valid and query is specific enough.

## License

MIT
