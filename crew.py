# crew.py

from crewai import Crew
from dotenv import load_dotenv

# Ensure env is loaded even when this module is imported directly
load_dotenv()

from agents.case_intake_agent import case_intake_agent
from agents.advisory_agent import advisory_agent
from agents.ipc_section_agent import ipc_section_agent
from agents.legal_precedent_agent import legal_precedent_agent
from agents.legal_drafter_agent import legal_drafter_agent
from agents.lawyer_notifier_agent import lawyer_notifier_agent
from tasks.case_intake_task import case_intake_task
from tasks.advisory_task import advisory_task
from tasks.ipc_section_task import ipc_section_task
from tasks.legal_precedent_task import legal_precedent_task
from tasks.legal_drafter_task import legal_drafter_task
from tasks.lawyer_notifier_task import lawyer_notifier_task


# --- 1. Advisory Phase Crew ---
advisory_crew = Crew(
    agents=[case_intake_agent, advisory_agent],
    tasks=[case_intake_task, advisory_task],
    verbose=True
)

# --- 2. Drafting Phase Crew ---
# NOTE: Precedent Agent is temporarily disabled to save tokens/requests
drafting_crew = Crew(
    agents=[ipc_section_agent, legal_drafter_agent, lawyer_notifier_agent],
    tasks=[ipc_section_task, lawyer_notifier_task, legal_drafter_task],
    verbose=True
)