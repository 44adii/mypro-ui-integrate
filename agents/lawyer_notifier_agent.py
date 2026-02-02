# lawyer_notifier_agent.py

from crewai import Agent, LLM
import os
from tools.lawyer_email_tool import send_lawyer_email_tool


llm = LLM(
    model="gemini/gemini-2.5-flash-lite", 
    temperature=0.2,
    api_key=os.environ.get("GOOGLE_API_KEY")
)

lawyer_notifier_agent = Agent(
    role="Lawyer Notifier Agent",
    goal=(
        "Draft a concise, professional outreach email to a nearby lawyer using the user's case summary and IPC sections, "
        "in the user's preferred language."
    ),
    backstory=(
        "You prepare outreach emails that summarize the issue, applicable IPC sections, and requested assistance, "
        "including contact details and preferred timelines."
    ),
    tools=[send_lawyer_email_tool],
    llm=llm,
    verbose=True,
    max_iter=5,
    max_rpm=60,
)




