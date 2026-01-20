from tools.multilingual_ipc_search_tool import search_multilingual_ipc
import time

print("🔍 Testing Pinecone Search...")
try:
    query = "What is the punishment for theft?"
    # The tool returns a list of dicts
    results = search_multilingual_ipc.func(query)
    
    if not results:
        print("❌ No results found. (Index might be empty or populating)")
    elif "error" in results[0]:
        print(f"❌ Error: {results[0]['error']}")
    else:
        print(f"✅ Success! Found {len(results)} results.")
        for r in results:
            print(f" - [{r.get('language')}] {r.get('content')[:50]}...")
except Exception as e:
    print(f"❌ Exception: {e}")
