# advisory_agent.py

from crewai import Agent, LLM


llm = LLM(model="gemini/models/gemini-1.5-flash", temperature=0.2)

legal_advisory_agent = Agent(
    role="Legal Advisory Agent",
    goal=(
        "Provide clear, actionable legal advice and next steps based on the case intake, "
        "identified IPC sections, and relevant precedents in the user's preferred language."
    ),
    backstory=(
        "You are a client-facing advisor who explains legal implications plainly and proposes a practical plan. "
        "You synthesize upstream analysis into concise recommendations, potential risks, and immediate actions. "
        "You tailor tone and language (English/Hindi) to the user's preference and avoid legalese unless necessary."
    ),
    tools=[],
    llm=llm,
    verbose=True,
)



