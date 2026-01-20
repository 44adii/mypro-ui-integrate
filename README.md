# ⚖️ NyayaGPT: AI Legal Assistant

**NyayaGPT** is an advanced AI-powered legal assistant designed to help users understand Indian Law. It leverages a **Multi-Agent System** and **Retrieval-Augmented Generation (RAG)** to analyze legal queries, identify relevant IPC sections, find precedent cases, and draft formal legal documents in both **English and Hindi**.

---

## 🚀 Key Features

*   **🗣️ Multilingual Support**: Interact in plain English or Hindi.
*   **🤖 Multi-Agent Architecture**: Five specialized AI agents work together:
    *   **Case Intake Agent**: Analyzes identifiers and categorizes the case.
    *   **IPC Section Agent**: Finds relevant Indian Penal Code sections.
    *   **Legal Precedent Agent**: Searches for similar past court judgments.
    *   **Legal Drafter Agent**: Drafts professional legal notices/FIRs.
    *   **Lawyer Notifier Agent**: Connects users with nearby lawyers via email.
*   **📚 RAG (Retrieval-Augmented Generation)**: Uses vector search (Pinecone) to ground answers in actual legal statutes.
*   **⚡ High Performance**: Powered by **Google Gemini 1.5 Flash** (1M Token Context) for deep analysis.
*   **☁️ Cloud Native**: Vectors stored in **Pinecone** for scalable, fast retrieval.

---

## 🛠️ Tech Stack

| Component | Technology |
| :--- | :--- |
| **LLM** | Google Gemini 1.5 Flash |
| **Orchestration** | CrewAI + LangChain |
| **Vector DB** | Pinecone (Serverless) |
| **Frontend** | Streamlit |
| **Embeddings** | HuggingFace (`sentence-transformers`) |
| **Search** | Tavily (Web Search for Precedents) |

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/44adii/mypro1.git
cd mypro1
```

### 2. Install Dependencies
Ensure you have Python 3.10+ installed.
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory and add your API keys:

```env
# AI Models
GOOGLE_API_KEY=your_google_api_key

# Vector Database
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=nyaya-legal-assistant

# Search
TAVILY_API_KEY=your_tavily_api_key

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
```

### 4. Run the Application
```bash
streamlit run app.py
```
The app will open in your browser at `http://localhost:8501`.

---

## 📂 Project Structure

```text
NyayaGPT/
├── agents/                 # AI Agent definitions (CrewAI)
├── tasks/                  # Task definitions for agents
├── tools/                  # Custom tools (Search, Email)
├── utils/                  # Utility scripts (Retry logic)
├── temporary/              # Archive of setup scripts
├── app.py                  # Main Streamlit application
├── multilingual_vectordb_builder.py # Script to ingest data to Pinecone
└── requirements.txt        # Python dependencies
```

---

## 🤝 Contributors

*   **[44adii](https://github.com/44adii)** - Lead Developer

---

## ⚠️ Disclaimer
*NyayaGPT is an AI tool for informational purposes only. It does not provide professional legal advice. Always consult a qualified attorney for legal matters.*
