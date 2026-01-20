import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ GROQ_API_KEY not found.")
    exit(1)

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    response = requests.get("https://api.groq.com/openai/v1/models", headers=headers)
    if response.status_code == 200:
        models = response.json().get("data", [])
        print(f"✅ Found {len(models)} models:")
        for m in models:
            print(f" - {m['id']}")
    else:
        print(f"❌ Error fetching models: {response.status_code} - {response.text}")

except Exception as e:
    print(f"❌ Exception: {e}")
