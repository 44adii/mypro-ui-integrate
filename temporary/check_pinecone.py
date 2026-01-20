import os
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

api_key = os.getenv("PINECONE_API_KEY")
if not api_key:
    print("❌ PINECONE_API_KEY not found in .env")
    exit(1)

try:
    pc = Pinecone(api_key=api_key)
    indexes = pc.list_indexes()
    print("✅ Pinecone Connection Successful!")
    print(f"Available Indexes: {[i.name for i in indexes]}")
    
    target_index = os.getenv("PINECONE_INDEX_NAME")
    print(f"Target Index from .env: {target_index}")
    
    if any(i.name == target_index for i in indexes):
        print("✅ Target index found.")
    else:
        print("❌ Target index NOT found in the list.")

except Exception as e:
    print(f"❌ Error connecting to Pinecone: {e}")
