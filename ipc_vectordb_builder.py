# ipc_vectordb_builder.py

import json
import os

from dotenv import load_dotenv
from langchain_community.docstore.document import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def load_ipc_data(file_path: str) -> list[dict]:
    """
    Load IPC data from a JSON file.

    Args:
        file_path (str): Path to the IPC JSON file.

    Returns:
        list[dict]: List of IPC sections as dictionaries.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except OSError as e:
        raise OSError(f"Failed to open IPC JSON file at '{file_path}': {e}") from e
    except json.JSONDecodeError as e:
        raise ValueError(f"IPC JSON at '{file_path}' is invalid JSON: {e}") from e


def sanitize_env_path(path: str | None) -> str | None:
    """
    Remove common wrapping characters (like <...> or quotes) and trim whitespace.
    """
    if path is None:
        return None
    p = path.strip()
    # Remove surrounding angle brackets if present
    if p.startswith("<") and p.endswith(">"):
        p = p[1:-1].strip()
    # Remove surrounding quotes if present
    if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
        p = p[1:-1]
    return p


def prepare_documents(ipc_data: list[dict]) -> list[Document]:
    """
    Convert IPC JSON entries to LangChain Document objects.

    Args:
        ipc_data (list[dict]): IPC data loaded from JSON.

    Returns:
        list[Document]: LangChain-compatible documents.
    """
    return [
        Document(
            page_content=f"Section {entry['Section']}: {entry['section_title']}\n\n{entry['section_desc']}",
            metadata={
                "chapter": entry["chapter"],
                "chapter_title": entry["chapter_title"],
                "section": entry["Section"],
                "section_title": entry["section_title"]
            }
        )
        for entry in ipc_data
    ]


def build_ipc_vectordb():
    """
    Build and persist a Chroma vectorstore for IPC sections.
    """
    # Load environment variables
    load_dotenv()
    ipc_json_path = os.getenv("IPC_JSON_PATH")
    persist_dir_path = os.getenv("PERSIST_DIRECTORY_PATH")
    collection_name = os.getenv("IPC_COLLECTION_NAME")

    # Sanitize values loaded from environment (handles cases like <"path">)
    ipc_json_path = sanitize_env_path(ipc_json_path)
    persist_dir_path = sanitize_env_path(persist_dir_path)
    collection_name = sanitize_env_path(collection_name)

    if not all([ipc_json_path, persist_dir_path, collection_name]):
        raise EnvironmentError("❌ Missing one or more required environment variables (after sanitization).")

    # Normalize and validate paths
    ipc_json_path = os.path.expanduser(os.path.normpath(ipc_json_path))
    persist_dir_path = os.path.expanduser(os.path.normpath(persist_dir_path))

    if not os.path.isfile(ipc_json_path):
        raise FileNotFoundError(f"IPC JSON file not found at: '{ipc_json_path}'")

    try:
        os.makedirs(persist_dir_path, exist_ok=True)
    except OSError as e:
        raise OSError(f"Failed to create or access persist directory '{persist_dir_path}': {e}") from e

    # Load and process data
    ipc_data = load_ipc_data(ipc_json_path)
    documents = prepare_documents(ipc_data)

    # Initialize embeddings and vectorstore
    embeddings = HuggingFaceEmbeddings()
    Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=persist_dir_path,
        collection_name=collection_name
    )

    print(f"✅ Vectorstore successfully created in collection '{collection_name}' at '{persist_dir_path}'")


if __name__ == "__main__":
    build_ipc_vectordb()
