import os
from crewai import Agent, Task, Crew, LLM
from dotenv import load_dotenv

load_dotenv()

# List of model names to try
model_names = [
    "gemini/gemini-1.5-flash-001",
    "gemini/gemini-1.5-flash-latest",
    "gemini/gemini-pro"
]

for model_name in model_names:
    print(f"\n\nTesting model: {model_name}")
    try:
        llm = LLM(model=model_name, temperature=0.7)
        agent = Agent(role="Test", goal="Reply 'OK'", backstory="Test", llm=llm)
        task = Task(description="Say OK", expected_output="OK", agent=agent)
        crew = Crew(agents=[agent], tasks=[task])
        result = crew.kickoff()
        print(f"SUCCESS with {model_name}! Output: {result}")
        break 
    except Exception as e:
        print(f"FAILED with {model_name}: {e}")
