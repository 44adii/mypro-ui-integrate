print("Start Import")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    print("Import Success")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
    print("Init Success")
except Exception as e:
    print(f"Error: {e}")
