# ⚖️ AI Legal Assistant

Welcome to the **AI Legal Assistant**!  
This project is an interactive web app that leverages multi-agent AI to help users analyze legal issues, identify relevant Indian Penal Code (IPC) sections, retrieve precedent cases, and generate formal legal documents—all from a plain English description.

---

## 🚀 Features

- 📝 **Plain English Input:** Describe your legal issue in your own words.
- 🤖 **Multi-Agent AI Workflow:** Specialized agents extract facts, identify IPC sections, retrieve case law, and generate documents.
- 📚 **Retrieval-Augmented Generation (RAG):** Combines semantic search with generative AI for accurate, grounded responses.
- 🧠 **Precedent Search:** Finds relevant judicial precedents for your scenario.
- 📄 **Formal Document Generation:** Outputs a structured legal summary or draft document.
- 🌐 **Streamlit Web App:** Clean, interactive, and user-friendly interface.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** (UI)
- **CrewAI** (Multi-agent orchestration)
- **dotenv** (Environment management)
- **ChromaDB** & **LangChain** (Semantic search, if enabled)

---

## 🖥️ How to Run Locally

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/ai-legal-assistant-crewai.git
   cd ai-legal-assistant-crewai
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `.env_template` to `.env` and fill in required keys (API keys, etc.).

4. **Run the app:**
   ```sh
   streamlit run app.py
   ```

5. **Open in your browser:**  
   Streamlit will provide a local URL (usually http://localhost:8501).

---

## 📝 Usage

1. Enter your legal issue in the text area (e.g., “Someone broke into my house at night and stole my valuables.”).
2. Click **"Run Legal Assistant"**.
3. Wait for the AI to analyze your case.
4. View the structured output, including relevant IPC sections, precedent cases, and a formal legal summary.

---

## 🧩 Agentic AI & RAG

- **Agentic AI:** The backend uses CrewAI to orchestrate multiple specialized agents, each handling a part of the legal reasoning process.
- **RAG (Retrieval-Augmented Generation):** The system retrieves relevant legal sections and case law, then uses this information to generate accurate, context-aware responses.

---

## 📦 Extending the Project

- Add more legal codes (e.g., CrPC, Evidence Act) by updating the data and agent logic.
- Integrate additional data sources or APIs for richer precedent search.
- Enhance the UI for multi-turn conversations or clarification prompts.

---

## ⚠️ Disclaimer

> This tool is for informational purposes only and **does not constitute legal advice**. For professional legal counsel, please consult a qualified attorney.

---

## 🙌 Contributing

Pull requests and suggestions are welcome!  
Feel free to open an issue or submit a PR to improve the assistant.

---

**Made with ❤️ using Streamlit, CrewAI, and
