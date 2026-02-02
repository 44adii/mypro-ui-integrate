# NyayaGPT - AI Legal Assistant ⚖️

**NyayaGPT** is a next-generation AI Legal Assistant designed to simplify legal access for everyone. It uses **Google Gemini 2.5 Flash Lite** and a **CrewAI Multi-Agent System** to listen to legal problems, classify them, and automatically draft official legal documents like FIRs.

## 🚀 Key Features

*   **🔐 Dual-Mode Authentication**:
    *   **Phone Login**: Sign in instantly using a mobile number.
    *   **Email Login**: Standard email/password authentication.
*   **🎙️ Voice-First Interface**: Speak your problem efficiently. Uses **Faster-Whisper** for high-accuracy local transcription (Hindi/English support).
*   **🧠 Multi-Agent Analysis**:
    *   **Case Intake Agent**: Structures raw unstructured user stories.
    *   **Advisory Agent**: Determines if a case is Civil/Criminal and advises the immediate next step (e.g., "File FIR").
    *   **Legal Drafter Agent**: Writes **Standard Official Legal Letters** (To The SHO/Court Format) instead of generic AI text.
*   **📄 Professional Tools**:
    *   **PDF Generation**: Instantly download drafted legal documents as formatted PDFs (`jspdf`).
    *   **Lawyer Connect**: One-click "Email to Lawyer" feature to send drafts to legal professionals.
*   **⚡ Modern Stack**: Built with **React + Vite** (Frontend) and **FastAPI** (Backend) for blazing fast performance.

## 🛠️ Tech Stack

*   **Frontend**: React, TailwindCSS, Lucide Icons, jsPDF
*   **Backend**: FastAPI, Uvicorn, Python 3.12
*   **AI Core**: CrewAI (Agent Orchestration), Google Gemini 2.5 Flash Lite (LLM), Faster-Whisper (ASR)
*   **Deployment**: Ready for local hosting or cloud deployment.

## 📦 Installation & Setup

1.  **Clone the Repo**
    ```bash
    git clone https://github.com/44adii/mypro-ui-integrate.git
    cd mypro-ui-integrate
    ```

2.  **Backend Setup**
    ```bash
    cd backend
    pip install -r requirements.txt
    
    # Create .env file with your API Key
    echo "GOOGLE_API_KEY=your_key_here" > .env
    
    # Run Server
    uvicorn main:app --reload --port 8001
    ```

3.  **Frontend Setup**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

4.  **Usage**
    *   Open `http://localhost:5173`.
    *   Click the microphone to speak your legal issue.
    *   Click **"Analyze"** to get a strategy.
    *   Click **"Date & Draft"** to get a downloadable PDF.

## 🛡️ License

MIT License. Free to use for educational and legal aid innovation.
