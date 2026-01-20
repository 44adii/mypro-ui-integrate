# Multilingual IPC Setup Guide

## Overview
Your project now supports multilingual IPC data with vector store search capabilities.

## JSON Files Being Used

1. **ipc.json** - Original structured IPC sections (575 records)
   - Format: Has `section_title`, `section_desc`, `chapter`, `Section` fields
   
2. **ipc_english_pages.json** - English IPC from PDF (119 pages)
   - Format: PDF-extracted with `language`, `granularity`, `page`, `text` fields
   
3. **ipc_hindi.json** - Hindi IPC from PDF (100 pages)
   - Format: PDF-extracted with `language`, `granularity`, `page`, `text` fields

## Vector Store Configuration

### Environment Variables

In your `.env` file, you can set:

```env
# Main persistence directory (used by multilingual tool)
PERSIST_DIRECTORY_PATH=./CHROMA_DB_IPC_MULTI

# Multilingual-specific settings (optional)
IPC_MULTI_PERSIST_DIR=./CHROMA_DB_IPC_MULTI
IPC_MULTI_COLLECTION=ipc_multilingual

# Which JSONs to include in the vector store
IPC_JSON_PATHS=ipc.json,ipc_english_pages.json,ipc_hindi.json
```

### Building the Vector Store

To rebuild the multilingual vector store:

```bash
python multilingual_vectordb_builder.py
```

Or with custom JSON paths:

```python
import os
os.environ['IPC_JSON_PATHS'] = 'ipc.json,ipc_english_pages.json,ipc_hindi.json'
from multilingual_vectordb_builder import build_multilingual_vectordb
build_multilingual_vectordb()
```

## Using the Multilingual Search Tool

### Import and Use

```python
from tools.multilingual_ipc_search_tool import search_multilingual_ipc

# Search without language filter
results = search_multilingual_ipc.func("What are theft laws?")

# Search with language filter
hindi_results = search_multilingual_ipc.func("चोरी के कानून", language_filter="hindi")
english_results = search_multilingual_ipc.func("theft laws", language_filter="english")
```

### Result Format

Each result contains:
- `language`: "english" or "hindi"
- `granularity`: "section" or "page"
- `content`: The actual text content
- `section`: Section number (if available)
- `page`: Page number (if available)
- `id`: Unique identifier

### Integration with Your Agents

To use the multilingual tool in your CrewAI agents:

1. Import the tool:
```python
from tools.multilingual_ipc_search_tool import search_multilingual_ipc
```

2. Use it in your agent's tools:
```python
agent.tools = [search_multilingual_ipc]
```

## Current Setup

✅ **Vector Store Built**
- Collection: `ipc_multilingual`
- Location: `./CHROMA_DB_IPC_MULTI`
- Documents: 794 total (575 from ipc.json + 119 English pages + 100 Hindi pages)
- Uses: `PERSIST_DIRECTORY_PATH` from your .env

✅ **Search Tool Ready**
- File: `tools/multilingual_ipc_search_tool.py`
- Supports: English and Hindi queries
- Language filtering: Optional
- Reads from: `PERSIST_DIRECTORY_PATH` environment variable

## Next Steps

To integrate the multilingual search into your legal assistant:

1. Update your agents to use `search_multilingual_ipc` instead of the old `search_ipc_sections`
2. Test the search with queries in both English and Hindi
3. Optionally add language detection to automatically use the correct language filter

## Example Query Test

```python
from tools.multilingual_ipc_search_tool import search_multilingual_ipc

# Test English query
results = search_multilingual_ipc.func("IPC section for murder")
print(f"Found {len(results)} results")
for r in results:
    print(f"\nLanguage: {r['language']}")
    print(f"Content: {r['content'][:150]}...")
```


