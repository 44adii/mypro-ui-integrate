# 📚 Complete Codebase Review - NyayaGPT AI Legal Assistant

## 🎯 Project Overview

**NyayaGPT** is a multi-agent AI legal assistant that helps users understand legal issues, identify relevant Indian Penal Code (IPC) sections, find precedent cases, and generate formal legal documents. The system supports both English and Hindi languages and uses CrewAI for orchestration.

---

## 📁 Project Structure

### **Core Application Files**

#### `app.py` (Main Streamlit UI)
- **Purpose**: Web interface for the legal assistant
- **Features**:
  - Text area for legal issue input
  - Language selection dropdown (English/Hindi/Both)
  - Optional lawyer email input with checkbox to send documents
  - Displays final legal document and task outputs
  - Handles email sending via SMTP

#### `main.py` (CLI Entry Point)
- **Purpose**: Command-line interface for testing
- **Function**: Runs the legal assistant crew with a sample input
- **Usage**: Can be run directly for quick testing without UI

#### `crew.py` (Crew Orchestration)
- **Purpose**: Assembles all agents and tasks into a CrewAI crew
- **Components**:
  - Imports 5 agents and 5 tasks
  - Creates `legal_assistant_crew` with all agents and tasks
  - Main orchestration hub

---

### **🤖 Agents** (`agents/` directory)

Each agent is a specialized AI role with specific responsibilities:

#### 1. `case_intake_agent.py`
- **Role**: Case Intake Agent
- **Model**: Gemini 2.0 Flash Lite (temperature=0)
- **Purpose**: First step - analyzes user's legal query and classifies it
- **Output**: Structured JSON with case type, legal domain, summary, entities, jurisdiction
- **Language Support**: English & Hindi
- **Tools**: None (pure LLM analysis)

#### 2. `ipc_section_agent.py`
- **Role**: IPC Section Agent
- **Model**: Gemini 2.0 Flash Lite (temperature=0.3)
- **Purpose**: Identifies relevant Indian Penal Code sections
- **Tools**: `search_multilingual_ipc` (vector DB search)
- **Language Support**: English & Hindi via multilingual search

#### 3. `legal_precedent_agent.py`
- **Role**: Legal Precedent Agent
- **Model**: Gemini 2.0 Flash Lite (temperature=0)
- **Purpose**: Finds relevant legal precedent cases
- **Tools**: `search_legal_precedents` (Tavily search API)
- **Sources**: IndianKanoon.org (trusted legal database)
- **Language Support**: English & Hindi

#### 4. `legal_drafter_agent.py`
- **Role**: Legal Document Drafting Agent
- **Model**: Gemini 2.0 Flash Lite (temperature=0.2)
- **Purpose**: Drafts formal legal documents (FIRs, legal notices, complaints)
- **Tools**: None (uses context from upstream agents)
- **Language Support**: English & Hindi
- **Output Format**: Markdown with structured sections

#### 5. `lawyer_notifier_agent.py`
- **Role**: Lawyer Notifier Agent
- **Model**: Gemini 2.0 Flash Lite (temperature=0.2)
- **Purpose**: Drafts professional outreach emails to lawyers
- **Tools**: `send_lawyer_email_tool` (email sending)
- **Language Support**: English & Hindi
- **Output**: JSON with subject and body

#### 6. `advisory_agent.py` ⚠️ (Not Used)
- **Role**: Legal Advisory Agent
- **Status**: Defined but NOT included in `crew.py`
- **Note**: This agent exists but is not part of the active workflow

---

### **📋 Tasks** (`tasks/` directory)

Tasks define what each agent should do:

#### 1. `case_intake_task.py`
- **Agent**: `case_intake_agent`
- **Purpose**: Interpret legal query and return structured JSON
- **Input**: `{user_input}`, `{language_preference}`
- **Output**: JSON with `case_type`, `legal_domain`, `summary`, `relevant_entities`, `jurisdiction`
- **Language Handling**: Returns output in user's preferred language

#### 2. `ipc_section_task.py`
- **Agent**: `ipc_section_agent`
- **Context**: Depends on `case_intake_task`
- **Purpose**: Identify and retrieve relevant IPC sections (3-5 sections)
- **Language Handling**: Appends `[hindi]`, `[english]`, or `[all]` to search query
- **Output**: JSON array with section/page, language, content, granularity

#### 3. `legal_precedent_task.py`
- **Agent**: `legal_precedent_agent`
- **Context**: Depends on `case_intake_task` and `ipc_section_task`
- **Purpose**: Search for relevant Indian legal precedents
- **Output**: Cohesive paragraph summarizing key precedent cases
- **Language Handling**: Respects `language_preference`

#### 4. `legal_drafter_task.py`
- **Agent**: `legal_drafter_agent`
- **Context**: Depends on `case_intake_task`, `ipc_section_task`, `legal_precedent_task`
- **Purpose**: Draft formal legal document
- **Output Format**: Markdown with:
  - Title (ALL CAPS)
  - Date, Parties
  - Factual Summary
  - Applicable IPC Sections
  - Demand/Request
  - Sender Details
- **Language Handling**: Strict language rules - entire document in chosen language

#### 5. `lawyer_notifier_task.py`
- **Agent**: `lawyer_notifier_agent`
- **Context**: Depends on `case_intake_task` and `ipc_section_task`
- **Purpose**: Draft lawyer outreach email
- **Output**: JSON with `subject` and `body` keys
- **Email Format**: Structured bullet points with greeting, purpose, case summary, facts, IPC sections, request, contact, sign-off

---

### **🛠️ Tools** (`tools/` directory)

#### 1. `multilingual_ipc_search_tool.py`
- **Tool Name**: "Multilingual IPC Sections Search Tool"
- **Purpose**: Searches IPC vector database (ChromaDB) for relevant sections
- **Features**:
  - Supports English and Hindi sources
  - Language detection from query hints: `[hindi]`, `[english]`, `[all]`
  - Uses HuggingFace embeddings
  - Returns top 5 results with metadata (section/page, language, granularity, content)
- **Vector DB**: `CHROMA_DB_IPC_MULTI` (multilingual collection)

#### 2. `ipc_sections_search_tool.py` ⚠️ (Legacy)
- **Status**: Older version, not actively used
- **Purpose**: English-only IPC section search
- **Note**: Replaced by `multilingual_ipc_search_tool.py`

#### 3. `legal_precedent_search_tool.py`
- **Tool Name**: "Legal Precedent Search Tool"
- **Purpose**: Searches for legal precedent cases using Tavily Search API
- **Features**:
  - Restricts search to trusted sources (IndianKanoon.org)
  - Returns case titles, summaries, and links
  - Max 10 results
- **Requires**: `TAVILY_API_KEY` in .env

#### 4. `email_tool.py`
- **Function**: `send_email_smtp()`
- **Purpose**: Low-level SMTP email sending functionality
- **Features**:
  - Supports plain text and HTML emails
  - Uses environment variables for SMTP config
  - Required env vars: `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `SMTP_FROM_EMAIL`
  - Optional: `SMTP_FROM_NAME`

#### 5. `lawyer_email_tool.py`
- **Tool Name**: "Send Lawyer Email"
- **Purpose**: CrewAI tool wrapper for `send_email_smtp()`
- **Usage**: Used by `lawyer_notifier_agent` to send emails

#### 6. `pdf_to_json.py`
- **Purpose**: Utility script to convert IPC PDFs to JSON format
- **Features**:
  - Extracts text per page from PDFs
  - Splits into sections using regex patterns (English/Hindi)
  - Supports two modes: "sections" or "pages"
  - Outputs structured JSON with metadata (id, language, granularity, section/page, text)
- **Usage**: Run to preprocess PDFs before building vector database

---

### **🗄️ Vector Database Builders**

#### `ipc_vectordb_builder.py` ⚠️ (Legacy)
- **Purpose**: Builds English-only IPC vector database
- **Status**: Older version, replaced by multilingual version
- **Output**: Single-language ChromaDB collection

#### `multilingual_vectordb_builder.py`
- **Purpose**: Builds multilingual IPC vector database
- **Features**:
  - Processes multiple JSON files (comma-separated in `IPC_JSON_PATHS`)
  - Handles both structured IPC JSON and PDF-extracted formats
  - Creates unified multilingual collection
  - Uses HuggingFace embeddings
- **Configuration**:
  - `IPC_JSON_PATHS`: Comma-separated JSON file paths
  - `IPC_MULTI_PERSIST_DIR`: Output directory (default: `./CHROMA_DB_IPC_MULTI`)
  - `IPC_MULTI_COLLECTION`: Collection name (default: `ipc_multilingual`)

#### `query_vectordb.py`
- **Purpose**: Testing/utility script to query vector database
- **Usage**: Quick testing of vector DB search functionality

---

### **📊 Data Files**

- `ipc.json`: Structured IPC data (English)
- `ipc_english.json`: English IPC sections (processed from PDF)
- `ipc_hindi.json`: Hindi IPC sections (processed from PDF)
- `ipc_english_pages.json`: English IPC pages format
- `ipc_section_english.pdf`: Source PDF (English)
- `ipc_section_hindi.pdf`: Source PDF (Hindi)
- `sample_inputs.txt`: Example legal queries for testing

---

## 🔄 Workflow Overview

### **Task Execution Order** (based on context dependencies):

1. **Case Intake Task** → Analyzes user input, classifies case
2. **IPC Section Task** → Uses case intake output, finds relevant IPC sections
3. **Legal Precedent Task** → Uses case intake + IPC sections, finds case law
4. **Lawyer Notifier Task** → Uses case intake + IPC sections, drafts lawyer email
5. **Legal Drafter Task** → Uses all previous outputs, drafts final document

### **Data Flow**:
```
User Input → Case Intake → IPC Search → Precedent Search → Document Drafting
                                      ↘ Lawyer Email Drafting (parallel)
```

---

## 🌐 Language Support

The entire system supports **multilingual output** (English/Hindi/Both):
- All agents have bilingual capabilities in their backstories
- Tasks explicitly check `language_preference` input
- Tools support language filtering (multilingual IPC search)
- Vector database contains both English and Hindi content

---

## 🔧 Configuration & Dependencies

### **Key Environment Variables** (from `requirements.txt` and code analysis):
- `GOOGLE_API_KEY` or `GEMINI_API_KEY` - For Gemini LLM
- `TAVILY_API_KEY` - For legal precedent search
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS` - For email functionality
- `IPC_MULTI_PERSIST_DIR` - Vector database directory
- `IPC_MULTI_COLLECTION` - Vector database collection name
- `IPC_JSON_PATHS` - Comma-separated JSON file paths for vector DB

### **Main Dependencies**:
- `crewai` - Multi-agent orchestration
- `langchain-*` - LLM framework and vector DB integration
- `streamlit` - Web UI
- `tavily-python` - Legal precedent search
- `sentence-transformers` - Embeddings for vector search
- `pypdf` - PDF processing

---

## ⚠️ Notable Issues/Observations

1. **Unused Agent**: `advisory_agent.py` is defined but not included in `crew.py`
2. **Legacy Tools**: `ipc_sections_search_tool.py` exists but is replaced by multilingual version
3. **Legacy Builder**: `ipc_vectordb_builder.py` exists but multilingual version is used
4. **Task Order**: In `crew.py`, tasks are listed in a different order than execution dependencies
5. **Email Integration**: Lawyer email is sent from `app.py` directly, but also has a dedicated agent/task (may be redundant)

---

## 📝 Key Files Summary

| File | Purpose | Status |
|------|---------|--------|
| `app.py` | Streamlit web UI | ✅ Active |
| `crew.py` | Crew orchestration | ✅ Active |
| `main.py` | CLI entry point | ✅ Active |
| `agents/case_intake_agent.py` | Case classification | ✅ Active |
| `agents/ipc_section_agent.py` | IPC section search | ✅ Active |
| `agents/legal_precedent_agent.py` | Precedent search | ✅ Active |
| `agents/legal_drafter_agent.py` | Document drafting | ✅ Active |
| `agents/lawyer_notifier_agent.py` | Lawyer email | ✅ Active |
| `agents/advisory_agent.py` | Advisory (unused) | ⚠️ Not in crew |
| `tools/multilingual_ipc_search_tool.py` | IPC search tool | ✅ Active |
| `tools/legal_precedent_search_tool.py` | Precedent search tool | ✅ Active |
| `tools/email_tool.py` | Email sending | ✅ Active |
| `multilingual_vectordb_builder.py` | Vector DB builder | ✅ Active |

---

## 🚀 Quick Start Flow

1. **Setup**: Install dependencies, configure `.env` file
2. **Build Vector DB**: Run `multilingual_vectordb_builder.py` to create IPC vector database
3. **Run App**: Execute `streamlit run app.py`
4. **Use**: Enter legal query, select language, get structured legal document

---

This codebase is a well-structured multi-agent legal assistant system with strong multilingual support and comprehensive legal analysis capabilities!


