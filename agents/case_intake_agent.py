# case_intake_agent.py

from crewai import Agent, LLM


# agent specific LLM - can also be configured din .env file
llm = LLM(
    model="gemini/gemini-1.5-flash-latest",
    temperature=0
)

case_intake_agent = Agent(
    role="Case Intake Agent",
    goal=(
        "Understand the user's legal issue and classify it into a"
        " structured format for further legal processing in the user's preferred language."
    ),
    backstory=(
        "You're a highly skilled legal intake assistant trained to analyze"
        " legal concerns in both English and Hindi. "
        "You identify the type of legal issue, categorize it under a domain of law,"
        " and extract relevant context "
        "to pass along to legal researchers, drafters, or compliance teams. "
        "You're fluent in both English and Hindi and can respond in either language based on user preference."
    ),
    llm=llm,
    tools=[],
    verbose=True,
    max_iter=5,
    max_rpm=60,
)

