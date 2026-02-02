# legal_drafter_task.py

from crewai import Task

from agents.legal_drafter_agent import legal_drafter_agent
from tasks.case_intake_task import case_intake_task
from tasks.ipc_section_task import ipc_section_task
from tasks.legal_precedent_task import legal_precedent_task
from tasks.advisory_task import advisory_task

legal_drafter_task = Task(
    agent=legal_drafter_agent,
    description=(
        "Review the following Case Summary and Advisory Analysis:\n"
        "CASE SUMMARY: {case_summary}\n"
        "ADVISORY ANALYSIS: {advisory_analysis}\n\n"
        "Draft the EXACT document requested (e.g., if 'File FIR' -> Draft an FIR application; if 'Legal Notice' -> Draft a Legal Notice).\n"
        "Incorporate the identified IPC sections and Precedents.\n\n"
        "CRITICAL LANGUAGE RULES: The user's language preference is: {language_preference}\n"
        "- If 'hindi': write the whole document in natural, formal Hindi.\n"
        "- If 'english': write the whole document in English.\n"
        "- If 'both': write in English with short Hindi translation lines immediately after each bullet/section.\n\n"
        "STRICT FORMAT: Output should be a Formal Legal Document (No Markdown titles like # Title).\n"
        "Follow this exact structure:\n\n"
        "To,\n"
        "The Station House Officer (SHO),\n"
        "[Police Station Name/Area],\n"
        "[City, State, Zip Code]\n\n"
        "Subject: [Formal Subject Line, e.g., Application for Registration of FIR under Section ...]\n\n"
        "Respected Sir/Madam,\n\n"
        "[Paragraph 1: Introduction - I, [Name], resident of [Address], wish to report a cognizable offence committed against me on [Date/Time].]\n\n"
        "[Paragraph 2: Brief Facts - Narrative form, no bullets. Describe incident clearly.]\n\n"
        "[Paragraph 3: Legal Basis - It is submitted that the accused's actions constitute offences under Section [X] (Title), Section [Y] (Title)...]\n\n"
        "[Paragraph 4: Prayer/Demand - I request you to register an FIR and take strict legal action.]\n\n"
        "Yours Faithfully,\n\n"
        "[Name]\n"
        "[Contact Info]\n"
        "Date: [Current Date]"
    ),
    expected_output=(
        "Markdown document with headings and bullet points matching the structure above, fully in the chosen language."
    ),
    context=[ipc_section_task, legal_precedent_task]
)
