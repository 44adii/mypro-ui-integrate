# Language Selection Feature

## Overview
Your AI Legal Assistant now supports language selection for responses. Users can choose between English, Hindi, or both languages.

## What Changed

### 1. **app.py** - User Interface
- Added a language dropdown selector
- Options: "english", "hindi", "both"
- Passes `language_preference` to the crew

### 2. **agents/ipc_section_agent.py** - Agent Configuration
- Switched from `search_ipc_sections` to `search_multilingual_ipc`
- Updated backstory to mention multilingual support
- Agent now handles both English and Hindi queries

### 3. **tasks/ipc_section_task.py** - Task Instructions
- Updated description to handle language preferences
- Agent will append `[hindi]`, `[english]`, or `[all]` to search queries based on user preference
- Updated expected output format to include language fields

### 4. **tools/multilingual_ipc_search_tool.py** - Search Tool
- Detects language hints in queries (e.g., `[hindi]`, `[english]`, `[all]`)
- Filters results based on detected language preference
- Reads from `PERSIST_DIRECTORY_PATH` environment variable (your .env setting)

## How It Works

1. **User selects language** in the Streamlit UI dropdown
2. **Selection is passed** to the crew as `language_preference` input
3. **Agent receives the task** with instructions to append a language hint
4. **Tool searches** the multilingual vector store with the language filter
5. **Results are filtered** and returned in the requested language(s)

## Usage Examples

### In the App UI:
1. Select "english" → returns only English IPC sections
2. Select "hindi" → returns only Hindi IPC sections  
3. Select "both" → returns sections from both languages

### Tool Usage:
```python
# Search in Hindi
results = search_multilingual_ipc.func("theft laws [hindi]")

# Search in English
results = search_multilingual_ipc.func("theft laws [english]")

# Search in both languages
results = search_multilingual_ipc.func("theft laws [all]")
```

## Environment Configuration

Your `.env` file should have:
```env
PERSIST_DIRECTORY_PATH=./CHROMA_DB_IPC_MULTI
IPC_MULTI_COLLECTION=ipc_multilingual
```

## Next Steps

You may want to update these agents/tasks to also respect language preferences:
- `legal_precedent_agent.py` - Add multilingual precedent search
- `legal_drafter_task.py` - Generate documents in the selected language

## Testing

To test the multilingual feature:

```bash
# Run the app
streamlit run app.py

# Select different language options and observe results
```

The vector store contains:
- 575 records from ipc.json (English, structured sections)
- 119 records from ipc_english_pages.json (English, PDF-extracted)
- 100 records from ipc_hindi.json (Hindi, PDF-extracted)

Total: 794 documents indexed in the multilingual vector store.


