# Gemini API Migration Guide

This guide will help you migrate from Groq to Google Gemini API for all your agents.

## Step 1: Install Required Packages

Add the LangChain Google Gemini integration to your `requirements.txt`:

```bash
pip install langchain-google-genai
```

Or add it to your `requirements.txt` file and run:
```bash
pip install -r requirements.txt
```

## Step 2: Update Environment Variables

Add your Gemini API key to your `.env` file:

```env
# Remove or comment out GROQ_API_KEY if not needed
# GROQ_API_KEY=your_groq_api_key_here

# Add Gemini API key
GOOGLE_API_KEY=your_gemini_api_key_here
```

**Get your Gemini API key:**
1. Go to https://makersuite.google.com/app/apikey or https://ai.google.dev/
2. Create a new API key
3. Copy and paste it into your `.env` file

## Step 3: Update Agent LLM Configurations

You need to change the LLM model in **all 6 agent files**. Here's what to change:

### Current Format (Groq):
```python
from crewai import Agent, LLM

llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.2)
```

### New Format (Gemini):
```python
from crewai import Agent, LLM

llm = LLM(model="google/gemini-2.0-flash-lite", temperature=0.2)
```

## Step 4: Update All Agent Files

### Files to Update:
1. `agents/case_intake_agent.py`
2. `agents/ipc_section_agent.py`
3. `agents/legal_precedent_agent.py`
4. `agents/legal_drafter_agent.py`
5. `agents/lawyer_notifier_agent.py`
6. `agents/advisory_agent.py` (if used)

### Available Gemini Models:
- `google/gemini-2.0-flash-lite` (Recommended - very fast, cost-efficient)
- `google/gemini-2.0-flash` (Fast, higher quality than lite)
- `google/gemini-1.5-pro` (Higher quality, slower)
- `google/gemini-pro` (Legacy model)

## Step 5: Optional - Remove Groq

If you're completely removing Groq:

```bash
pip uninstall groq
```

And remove from `requirements.txt` if listed there.

---

## Quick Migration Script

If you want to migrate all agents at once, here's a Python script:

```python
import os
import re

# Agent files to update
agent_files = [
    "agents/case_intake_agent.py",
    "agents/ipc_section_agent.py",
    "agents/legal_precedent_agent.py",
    "agents/legal_drafter_agent.py",
    "agents/lawyer_notifier_agent.py",
    "agents/advisory_agent.py"
]

# Replace model from groq to gemini
old_model = 'groq/llama-3.3-70b-versatile'
new_model = 'google/gemini-1.5-flash'

for file_path in agent_files:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        
        content = content.replace(old_model, new_model)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"✓ Updated {file_path}")

print("\n✅ Migration complete!")
print("Don't forget to:")
print("1. Add GOOGLE_API_KEY to your .env file")
print("2. Run: pip install langchain-google-genai")
print("3. Test the application")
```

---

## Testing

After migration, test your application:

```bash
streamlit run app.py
```

Try with both English and Hindi queries to ensure everything works correctly.

---

## Troubleshooting

### "google/gemini model not found"
- Make sure you installed `langchain-google-genai`
- Verify `GOOGLE_API_KEY` is set in `.env`
- Try restarting the application

### "Invalid API key"
- Double-check your Gemini API key
- Make sure there are no extra spaces in `.env`
- Regenerate the key if needed

### LangChain Error
- Run: `pip install --upgrade langchain-google-genai`
- Make sure you have the latest version of `crewai` installed

---

## Model Comparison

| Feature | Groq (Llama) | Gemini 1.5 Flash |
|---------|--------------|------------------|
| Speed | Very Fast | Fast |
| Cost | Free Tier Available | Generous Free Tier |
| Multilingual | Good | Excellent (Native Hindi) |
| Quality | Good | Excellent |
| Context Window | Large | Very Large (1M tokens) |

**Note:** Gemini has native Hindi support which may improve your Hindi output quality!

---

## Rollback Instructions

If you need to rollback to Groq:

1. Revert agent files to use `groq/llama-3.3-70b-versatile`
2. Ensure `GROQ_API_KEY` is in your `.env`
3. Run the application again

---

## Additional Resources

- [Google AI Studio](https://makersuite.google.com/)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [LangChain Google Integration](https://python.langchain.com/docs/integrations/llms/google_vertex_ai_generative_models)

