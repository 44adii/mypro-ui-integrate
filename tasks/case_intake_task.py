# case_intake_task.py

from crewai import Task
from agents.case_intake_agent import case_intake_agent


case_intake_task = Task(
    agent=case_intake_agent,
    description=(
        "The user has submitted the following legal query:\n\n"
        "{user_input}\n\n"
        "Your job is to interpret it, identify the core legal issue, classify the legal domain "
        "(e.g., civil, criminal, labor), and return a structured JSON.\n\n"
        "IMPORTANT: The user's language preference is: {language_preference}\n"
        "You MUST provide your output in the user's preferred language:\n"
        "- If language_preference is 'hindi', return your response in Hindi\n"
        "- If language_preference is 'english', return your response in English\n"
        "- If language_preference is 'both', return in English with bilingual support\n\n"
        "Return a structured JSON with: "
        "`case_type`, `legal_domain`, `summary`, `relevant_entities`, and `jurisdiction` (if any)."
    ),
    expected_output=(
        "```json\n"
        "{\n"
        "  \"case_type\": \"Wrongful Termination\",\n"
        "  \"legal_domain\": \"Labor Law\",\n"
        "  \"summary\": \"The user reports being fired after refusing to work unpaid overtime.\",\n"
        "  \"relevant_entities\": [\"user\", \"employer\"],\n"
        "  \"jurisdiction\": \"India\"\n"
        "}\n"
        "```"
    ),
)