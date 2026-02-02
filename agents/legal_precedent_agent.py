# legal_precedent_agent.py

from crewai import Agent, LLM
import os
from tools.legal_precedent_search_tool import search_legal_precedents

llm = LLM(
    model="gemini/gemini-2.5-flash-lite", 
    temperature=0,
    api_key=os.environ.get("GOOGLE_API_KEY")
)

legal_precedent_agent = Agent(
    role="Legal Precedent Agent",
    goal="Find relevant legal precedent cases based on the user's legal issue and present them in the user's preferred language.",
    backstory=(
        "You're an expert legal researcher who specializes in finding case law and precedent judgments in both English and Hindi. "
        "You are skilled in identifying relevant case summaries based on natural language descriptions of legal issues. "
        "Your task is to search trusted legal databases to support legal analysis with past judgments. "
        "You can present findings in the user's preferred language (English or Hindi)."
    ),
    tools=[search_legal_precedents],
    llm=llm,
    verbose=True,
    max_iter=5,
    max_rpm=60,
)
