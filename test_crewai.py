print("Start Import CrewAI")
try:
    from crewai import LLM
    print("CrewAI Import Success")
    llm = LLM(model="gemini/gemini-2.5-flash-lite", temperature=0)
    print("CrewAI Init Success")
except Exception as e:
    print(f"Error: {e}")
