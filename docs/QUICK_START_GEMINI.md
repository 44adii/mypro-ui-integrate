# Quick Start: Migrate to Gemini

To migrate your AI Legal Assistant from Groq to Gemini, follow these 3 simple steps:

## Step 1: Run the Migration Script

```bash
python migrate_to_gemini.py
```

This will automatically update all 6 agent files to use Gemini (gemini-2.0-flash-lite by default).

## Step 2: Install Dependencies

```bash
pip install langchain-google-genai
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

## Step 3: Add API Key to .env

Add this line to your `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

**Get your API key:** https://ai.google.dev/

## Step 4: Test

```bash
streamlit run app.py
```

Test with both English and Hindi queries!

---

## What Changed?

- All agents now use `google/gemini-2.0-flash-lite` instead of `groq/llama-3.3-70b-versatile`
- Added `langchain-google-genai` to requirements.txt
- No changes needed to your code logic

## Rollback

If you need to go back to Groq:
1. Revert the agent files (or use git checkout)
2. Remove `GOOGLE_API_KEY` from `.env`
3. Use `GROQ_API_KEY` instead

---

For detailed information, see `GEMINI_MIGRATION_GUIDE.md`

