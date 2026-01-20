# 🚴‍♂️ TriAI: Adaptive Performance Director
**An autonomous AI Agent designed to solve the "Static Plan" problem in endurance sports.**

### 🎯 The Problem
Standard triathlon training plans are static. They don't adapt when an athlete is fatigued or when their life-stress (ATL/TSB) spikes. Most "AI coaches" are just fancy wrappers for generic LLM advice.

### 🚀 The Solution
I built a production-grade AI Agent that uses **RAG (Retrieval-Augmented Generation)** and **Real-time API Integration** to provide grounded, expert coaching.

**Key Technical Features:**
* **Direct Integration:** Connects to the **Intervals.icu API** to fetch live CTL, ATL, and TSB metrics.
* **Knowledge Retrieval (RAG):** Uses a local **ChromaDB** vector store to index specific coaching methodologies (e.g., 80/20 rule).
* **Reliability Engineering:** Implemented explicit error signaling and chaos testing to ensure the agent remains helpful even when data sources are offline.
* **Modern UI:** A **Streamlit** web interface with real-time streaming responses and metric visualization.

### 🛠️ Tech Stack
* **LLM:** OpenAI GPT-4o-mini
* **Database:** ChromaDB (Vector DB)
* **Frameworks:** Streamlit, Requests, Python-dotenv
* **Methodology:** Semantic Search, Context Injection, Zero-shot Prompting

### ⚙️ Setup
1. Clone the repo.
2. Create a `.env` file with `OPENAI_API_KEY`, `INTERVALS_API_KEY`, and `INTERVALS_ATHLETE_ID`.
3. Run `pip install -r requirements.txt`.
4. Launch with `streamlit run app.py`.