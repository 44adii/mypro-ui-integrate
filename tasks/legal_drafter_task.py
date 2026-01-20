# legal_drafter_task.py

from crewai import Task

from agents.legal_drafter_agent import legal_drafter_agent
from tasks.case_intake_task import case_intake_task
from tasks.ipc_section_task import ipc_section_task
from tasks.legal_precedent_task import legal_precedent_task

legal_drafter_task = Task(
    agent=legal_drafter_agent,
    description=(
        "Based on the legal case summary, IPC sections, and precedents retrieved from the previous tasks, draft a formal legal document (e.g., FIR or legal notice) that the user can submit.\n\n"
        "CRITICAL LANGUAGE RULES: The user's language preference is: {language_preference}\n"
        "- If 'hindi': write the whole document in natural, formal Hindi.\n"
        "- If 'english': write the whole document in English.\n"
        "- If 'both': write in English with short Hindi translation lines immediately after each bullet/section.\n\n"
        "STRICT FORMAT: Output should be clean Markdown with headings and bullet points (no code fences). Use the following structure and keep it concise and clear:\n"
        "# [ALL CAPS TITLE]\n"
        "- **Date**: [Current Date]\n"
        "- **Parties**: [Complainant] vs [Respondent]\n\n"
        "## Factual Summary\n"
        "- [1–3 short bullets]\n\n"
        "## Applicable IPC Sections\n"
        "- [Section Number]: [Short Title] — [Why applicable]\n"
        "- [Section Number]: [Short Title] — [Why applicable]\n\n"
        "## Demand / Request\n"
        "- [What action is requested and preferred timeline]\n\n"
        "## Sender Details\n"
        "- [Name], [Address], [Contact]\n"
    ),
    expected_output=(
        "Markdown document with headings and bullet points matching the structure above, fully in the chosen language."
    ),
    context=[case_intake_task, ipc_section_task, legal_precedent_task]
)
