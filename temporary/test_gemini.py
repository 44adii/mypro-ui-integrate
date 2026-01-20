import os
from dotenv import load_dotenv, find_dotenv
from crewai import Agent, Task, Crew, LLM

# Force reload of .env
load_dotenv(find_dotenv(), override=True)

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key loaded: {'Yes' if api_key else 'No'} (starts with {api_key[:4] if api_key else 'None'})")

try:
    print("Initializing LLM with gemini/gemini-2.0-flash...")
    llm = LLM(model="gemini/gemini-2.0-flash")
    
    agent = Agent(
        role="Test Agent",
        goal="Say hello",
        backstory="You are a test agent",
        llm=llm
    )
    
    task = Task(
        description="Say hello world",
        expected_output="Hello world",
        agent=agent
    )
    
    crew = Crew(agents=[agent], tasks=[task])
    print("Kicking off crew...")
    result = crew.kickoff()
    print("Success! Output:", result)
    
except Exception as e:
    print("\nERROR DETECTED:")
    print(e)
