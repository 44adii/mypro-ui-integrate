from crewai import Agent, LLM
import os

# Using the Lite model as per project standard
llm = LLM(
    model="gemini/gemini-2.5-flash-lite", 
    temperature=0.1,
    api_key=os.environ.get("GOOGLE_API_KEY")
)

advisory_agent = Agent(
    role="Legal Advisor & Strategist",
    goal="Analyze the user's situation to determine severity, legal classification, and the immediate best course of action (Police vs Lawyer vs Self-Help).",
    backstory=(
        "You are an expert Senior Legal Consultant who creates the initial roadmap for any legal issue. "
        "Your job is NOT to draft documents immediately, but to tell the user WHERE to go first. "
        "You strictly distinguish between Criminal matters (Police/FIR needed), Civil matters (Lawyer/Notice needed), "
        "and Consumer/Minor issues (Self-help/Forum needed). "
        "You always assess the SEVERITY of the situation (High/Low) to prioritize emergencies."
    ),
    llm=llm,
    verbose=True,
    max_iter=3,
    max_rpm=60,
)
