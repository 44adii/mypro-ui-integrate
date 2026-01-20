import json
import os
from typing import List, Dict

from dotenv import load_dotenv
from langchain_community.docstore.document import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def load_json(path: str) -> List[Dict]:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"JSON not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def prepare_documents(records: List[Dict]) -> List[Document]:
    documents: List[Document] = []
    for rec in records:
        # Handle different JSON formats
        language = rec.get("language", "unknown")
        granularity = rec.get("granularity", "unknown")
        section = rec.get("section") or rec.get("Section")
        page = rec.get("page")
        
        # Handle ipc.json format (structured IPC sections)
        if "section_title" in rec and "section_desc" in rec:
            # This is the original ipc.json format
            language = "english"
            granularity = "section"
            content = f"Section {rec.get('Section')}: {rec.get('section_title')}\n\n{rec.get('section_desc')}"
            metadata = {
                "id": f"ipc_{rec.get('Section')}",
                "language": language,
                "granularity": granularity,
                "section": str(rec.get("Section")),
                "chapter": str(rec.get("chapter")),
                "chapter_title": rec.get("chapter_title"),
                "section_title": rec.get("section_title")
            }
            documents.append(Document(page_content=content, metadata=metadata))
        else:
            # Handle PDF-extracted format (from tools/pdf_to_json.py)
            text = rec.get("text", "")
            header_bits = []
            if section:
                header_bits.append(f"Section {section}")
            if page:
                header_bits.append(f"Page {page}")
            header = " | ".join(header_bits)
            
            content = f"{header}\n\n{text}" if header else text
            
            metadata = {
                "id": rec.get("id"),
                "language": language,
                "granularity": granularity,
            }
            if section:
                metadata["section"] = section
            if page:
                metadata["page"] = page
            
            documents.append(Document(page_content=content, metadata=metadata))
    return documents


def build_multilingual_vectordb():
    load_dotenv()

    # Comma-separated list of JSON files to ingest
    # Example: IPC_JSON_PATHS=ipc_english_pages.json,ipc_hindi.json,ilsum_hindi_compact.json
    json_paths_csv = os.getenv("IPC_JSON_PATHS", "ipc_english.json,ipc_hindi.json")
    persist_dir_path = os.getenv("IPC_MULTI_PERSIST_DIR", "./CHROMA_DB_IPC_MULTI")
    collection_name = os.getenv("IPC_MULTI_COLLECTION", "ipc_multilingual")

    paths = [p.strip() for p in json_paths_csv.split(",") if p.strip()]
    if not paths:
        raise ValueError("No JSON paths provided in IPC_JSON_PATHS")

    # Load and combine data from all provided JSONs
    all_records: List[Dict] = []
    for p in paths:
        recs = load_json(p)
        all_records.extend(recs)

    # Prepare docs
    documents = prepare_documents(all_records)

    # Build embeddings + vector store
    embeddings = HuggingFaceEmbeddings()
    
    index_name = os.getenv("PINECONE_INDEX_NAME")
    if not index_name:
        raise ValueError("PINECONE_INDEX_NAME not set in .env")

    # Pinecone setup
    from pinecone import Pinecone, ServerlessSpec
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    
    # Check if index exists
    existing_indexes = [i.name for i in pc.list_indexes()]
    if index_name not in existing_indexes:
        print(f"Index '{index_name}' not found. Creating it (Dimensions: 768, Metric: cosine)...")
        try:
             # Create serverless index 
            pc.create_index(
                name=index_name,
                dimension=768, 
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                ) 
            )
            print(f"Created index '{index_name}'.")
        except Exception as e:
            print(f"Failed to create index: {e}")
            raise

    
    # Split documents to respect Pinecone metadata limits and improve retrieval
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs_split = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} original docs into {len(docs_split)} chunks.")

    from langchain_pinecone import PineconeVectorStore

    print(f"Uploading {len(docs_split)} documents to Pinecone index '{index_name}'...")
    PineconeVectorStore.from_documents(
        documents=docs_split,
        embedding=embeddings,
        index_name=index_name
    )

    print(f"Built multilingual vector store: {collection_name}")
    print(f"Persisted at: {persist_dir_path}")
    print(f"Indexed documents: {len(documents)}")


if __name__ == "__main__":
    build_multilingual_vectordb()


