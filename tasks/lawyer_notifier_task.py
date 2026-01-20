# lawyer_notifier_task.py

from crewai import Task

from agents.lawyer_notifier_agent import lawyer_notifier_agent
from tasks.case_intake_task import case_intake_task
from tasks.ipc_section_task import ipc_section_task
from tools.email_tool import send_email_smtp


def _send_lawyer_email(to_email: str, subject: str, body: str) -> dict:
    return send_email_smtp(to_email=to_email, subject=subject, body=body)


lawyer_notifier_task = Task(
    agent=lawyer_notifier_agent,
    context=[case_intake_task, ipc_section_task],
    description=(
        "Draft a concise, professional outreach email to a local lawyer summarizing the user's issue and the most relevant IPC sections, and requesting a consultation.\n\n"
        "CRITICAL: The user's language preference is: {language_preference}\n"
        "Use the user's language_preference for the entire email ('hindi' | 'english' | 'both'). For 'both', write in English and append a short Hindi translation right after each item.\n\n"
        "STRICT FORMAT: Return ONLY valid JSON with keys {\"subject\": string, \"body\": string}. Do not include code fences or extra text.\n\n"
        "BODY TEMPLATE (use simple bullet points with clear labels):\n"
        "- Greeting: [e.g., Dear [Lawyer Name],]\n"
        "- Purpose: [one line stating consultation request]\n"
        "- Case Summary: [1-2 lines]\n"
        "- Key Facts:\n"
        "  - [fact 1]\n"
        "  - [fact 2]\n"
        "  - [fact 3]\n"
        "- Relevant IPC Sections:\n"
        "  - [Section Number]: [Short title] — [Why applicable]\n"
        "  - [Section Number]: [Short title] — [Why applicable]\n"
        "- Request: [proposed next step, preferred timeline]\n"
        "- Contact: [user name or placeholder], [phone/email if available]\n"
        "- Sign-off: [Sincerely/Regards], [User]"
    ),
    expected_output=(
        '{"subject": "Consultation Request — [Short Issue Title]", "body": "- Greeting: ...\n- Purpose: ...\n- Case Summary: ...\n- Key Facts:\n  - ...\n  - ...\n- Relevant IPC Sections:\n  - 380: Theft in dwelling house — ...\n- Request: ...\n- Contact: ...\n- Sign-off: ..."}'
    ),
    async_execution=False,
)




