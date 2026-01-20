# multilingual_ipc_search_tool.py

import os

from dotenv import load_dotenv
from crewai.tools import tool
# from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Global cache for embeddings to prevent reloading on every tool call
_CACHED_EMBEDDINGS = None

def get_embeddings():
    """Lazy load and cache embeddings."""
    global _CACHED_EMBEDDINGS
    if _CACHED_EMBEDDINGS is None:
        print("Loading Embedding Model (this should happen only once)...")
        _CACHED_EMBEDDINGS = HuggingFaceEmbeddings()
    return _CACHED_EMBEDDINGS


@tool("Multilingual IPC Sections Search Tool")
def search_multilingual_ipc(query: str) -> list[dict]:
    """
    Search multilingual IPC vector database for sections relevant to the input query.
    Supports both English and Hindi sources. 

    The tool will detect the language of the query and search accordingly. To explicitly search
    in a specific language, include language hints in your query like "[hindi]" or "[english]".

    Args:
        query (str): User query in natural language. Can include language preference hints.

    Returns:
        list[dict]: List of matching IPC sections with metadata and content.
    """
    # Load environment variables
    load_dotenv()

    # Detect language preference from query
    language_filter = None
    if "[hindi]" in query.lower():
        language_filter = "hindi"
        query = query.replace("[hindi]", "").strip()
    elif "[english]" in query.lower():
        language_filter = "english"
        query = query.replace("[english]", "").strip()
    elif "[both]" in query.lower() or "[all]" in query.lower():
        language_filter = None
        query = query.replace("[both]", "").replace("[all]", "").strip()

    # Pinecone configuration
    index_name = os.getenv("PINECONE_INDEX_NAME")
    if not index_name:
        return [{"error": "PINECONE_INDEX_NAME not found in .env"}]

    # Use cached embeddings
    embedding_function = get_embeddings()

    from langchain_pinecone import PineconeVectorStore
    
    vector_db = PineconeVectorStore(
        index_name=index_name,
        embedding=embedding_function
    )

    top_k = 3  # Reduced to avoid context exhaustion

    # Perform similarity search
    docs = vector_db.similarity_search(query, k=top_k)

    # Format results with language support
    results = []
    for doc in docs:
        metadata = doc.metadata
        result = {
            "language": metadata.get("language", "unknown"),
            "granularity": metadata.get("granularity", "unknown"),
            "content": doc.page_content
        }
        
        # Add section or page info based on granularity
        if metadata.get("section"):
            result["section"] = metadata.get("section")
        if metadata.get("page"):
            result["page"] = metadata.get("page")
        
        # Add original ID
        if metadata.get("id"):
            result["id"] = metadata.get("id")
        
        results.append(result)

    # Apply language filter if specified
    if language_filter:
        results = [r for r in results if r.get("language") == language_filter]

    return results


# Example usage - uncomment for testing
# if __name__ == "__main__":
#     query = "What are the legal sections for theft?"
#     results = search_multilingual_ipc.func(query)
#     print(f"Found {len(results)} results")
#     for r in results:
#         print(f"\nLanguage: {r['language']}")
#         print(f"Content: {r['content'][:200]}...")

