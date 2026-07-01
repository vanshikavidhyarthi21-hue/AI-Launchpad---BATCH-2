# Yojana Sahayak

AI-powered chatbot that helps Indian citizens discover government schemes they are eligible for.

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your Anthropic API key:

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

### 3. Collect Data (Phase 1 & 2)

```bash
python scripts/01_scrape_and_extract.py
```

This will:
- Fetch 200+ government schemes from myScheme API
- Extract structured metadata using Claude Haiku
- Save to `data/schemes.json`

### 4. Build Vector Database (Phase 3)

```bash
python scripts/02_build_vectordb.py
```

This will:
- Generate embeddings using `all-MiniLM-L6-v2`
- Store in ChromaDB at `data/chroma_db/`

### 5. Run the App

```bash
streamlit run app.py
```

---

## Project Structure

```
yojana_sahayak/
├── .env.example          # Environment config template
├── .env                  # Your actual API keys (not committed)
├── requirements.txt      # Python dependencies
├── app.py                # Streamlit frontend
├── data/
│   ├── schemes.json      # Scraped scheme data
│   └── chroma_db/        # ChromaDB vector store
├── scripts/
│   ├── 01_scrape_and_extract.py   # Phase 1 & 2: Data collection
│   └── 02_build_vectordb.py       # Phase 3: Vector DB
└── src/
    ├── __init__.py
    ├── rag_pipeline.py   # Retrieval pipeline
    └── chatbot.py        # Chatbot logic
```

---

## Architecture

```
User Input
    │
    ▼
Streamlit UI (app.py)
    │
    ▼
YojanaChatbot (src/chatbot.py)
    │
    ├─► Profile Builder (collect 7 profile fields)
    │
    ├─► YojanaRetriever (src/rag_pipeline.py)
    │       │
    │       ├─► SentenceTransformer Embeddings
    │       └─► ChromaDB Semantic Search + Metadata Filter
    │
    └─► Claude Sonnet 4.6 → Ranked Recommendations
```

---

## Features

- ✅ **One question at a time** — never overwhelming
- ✅ **Semantic search** — finds relevant schemes even without exact keyword matches
- ✅ **Metadata filtering** — narrows search by state, category, income
- ✅ **200+ schemes** — from myScheme.gov.in
- ✅ **Live matching count** — shows matches after each answer
- ✅ **Structured recommendations** — eligibility, benefits, how to apply, official links
- ✅ **Premium UI** — dark glassmorphism design

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| LLM (Chat) | Claude Sonnet 4.6 |
| LLM (Metadata) | Claude Haiku |
| Embeddings | all-MiniLM-L6-v2 |
| Vector DB | ChromaDB |
| Framework | LangChain |
| Frontend | Streamlit |
| Data Source | myScheme.gov.in |
