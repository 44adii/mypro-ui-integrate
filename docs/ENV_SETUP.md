# Environment Setup Guide

This guide explains how to set up your `.env` file for the AI Legal Assistant.

## Required Environment Variables

### 1. AI Model API Key (REQUIRED - Choose ONE)

You need **either** Groq **or** Gemini API key, depending on which model you're using:

#### Option A: Using Groq (Original Configuration)
```env
# Get your Groq API key from https://console.groq.com/
GROQ_API_KEY=your_groq_api_key_here
```

#### Option B: Using Google Gemini (After Migration)
```env
# Get your Gemini API key from https://ai.google.dev/
GOOGLE_API_KEY=your_gemini_api_key_here
# or alternatively
GEMINI_API_KEY=your_gemini_api_key_here
```

### 2. Tavily API Key (Optional but Recommended)

```env
# Get your Tavily API key from https://tavily.com/
# Optional but recommended for legal precedent search
TAVILY_API_KEY=your_tavily_api_key_here
```

**How to get API keys:**
- **GROQ_API_KEY**: Sign up at https://console.groq.com/ and create an API key
- **GOOGLE_API_KEY**: Sign up at https://ai.google.dev/ and create an API key
- **TAVILY_API_KEY**: Sign up at https://tavily.com/ and get your free API key

---

## Optional: Email Configuration

To enable the lawyer notification email feature, add these SMTP settings:

```env
# SMTP Server Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_specific_password_here
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_FROM_NAME=AI Legal Assistant
```

### Gmail Setup Instructions:

1. Enable 2-Factor Authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Create an "App Password" for "Mail"
4. Copy the generated 16-character password
5. Use this password as your `SMTP_PASS` value

**Note:** If email is not configured, the lawyer notification feature will still work to draft emails, but won't actually send them.

---

## Optional: Vector Store Configuration

For multilingual support (English/Hindi):

```env
# Path where the ChromaDB vector store is persisted
PERSIST_DIRECTORY_PATH=./CHROMA_DB_IPC_MULTI

# Collection name for multilingual IPC data
IPC_MULTI_COLLECTION=ipc_multilingual

# JSON files to include when building vector store
IPC_JSON_PATHS=ipc.json,ipc_english_pages.json,ipc_hindi.json
```

---

## Complete Example `.env` Files

### For Groq Setup:
```env
# ==========================================
# REQUIRED: API Keys
# ==========================================
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# ==========================================
# OPTIONAL: Email Configuration
# ==========================================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_specific_password_here
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_FROM_NAME=AI Legal Assistant

# ==========================================
# OPTIONAL: Vector Store Configuration
# ==========================================
PERSIST_DIRECTORY_PATH=./CHROMA_DB_IPC_MULTI
IPC_MULTI_COLLECTION=ipc_multilingual
IPC_JSON_PATHS=ipc.json,ipc_english_pages.json,ipc_hindi.json
```

### For Gemini Setup (After Migration):
```env
# ==========================================
# REQUIRED: API Keys
# ==========================================
GOOGLE_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

# ==========================================
# OPTIONAL: Email Configuration
# ==========================================
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_specific_password_here
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_FROM_NAME=AI Legal Assistant

# ==========================================
# OPTIONAL: Vector Store Configuration
# ==========================================
PERSIST_DIRECTORY_PATH=./CHROMA_DB_IPC_MULTI
IPC_MULTI_COLLECTION=ipc_multilingual
IPC_JSON_PATHS=ipc.json,ipc_english_pages.json,ipc_hindi.json
```

---

## Setup Steps

1. Copy the example configuration above
2. Create a file named `.env` in your project root
3. Fill in your actual API keys and configuration
4. Save the file
5. **Important**: Never commit `.env` to version control (it should be in `.gitignore`)

---

## Verification

After setting up your `.env` file, test the configuration:

```bash
# Run the app
streamlit run app.py

# Test with a simple legal query
# If everything is configured correctly, you should see:
# - Legal analysis output
# - Relevant IPC sections
# - Precedent cases (if TAVILY_API_KEY is set)
# - Formal legal document
```

---

## Troubleshooting

### "Missing SMTP configuration"
- This is normal if you haven't configured email yet
- The lawyer notification will still draft emails, but won't send them
- See "Email Configuration" section above to enable sending

### "API KEY not found" or "GOOGLE_API_KEY/GEMINI_API_KEY must be set"
- Make sure you created a `.env` file in the project root
- Check that your API key is spelled correctly (GROQ_API_KEY or GOOGLE_API_KEY)
- Ensure there are no spaces around the `=` sign
- If using Gemini, make sure you ran: `pip install langchain-google-genai`

### Hindi output not working
- Make sure the multilingual vector store is built
- Run: `python multilingual_vectordb_builder.py`
- Check that `CHROMA_DB_IPC_MULTI` directory exists

### Email sending fails
- Verify your SMTP credentials are correct
- For Gmail, make sure you're using an App Password, not your regular password
- Check that 2-Factor Authentication is enabled on your Google account

