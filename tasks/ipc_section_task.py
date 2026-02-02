# ipc_section_task.py

from crewai import Task
from agents.ipc_section_agent import ipc_section_agent
from tasks.case_intake_task import case_intake_task
from tasks.advisory_task import advisory_task

ipc_section_task = Task(
    agent=ipc_section_agent,
    async_execution=True,
    description=(
        "You are provided with the following Case Summary and Advisory Analysis:\n"
        "CASE SUMMARY: {case_summary}\n"
        "ADVISORY ANALYSIS: {advisory_analysis}\n\n"
        "1. **Analyze Strategy**: Use the 'legal_type' (Criminal vs Civil) from the Advisory Analysis to guide your search.\n"
        "2. **Search Strategy**: \n"
        "   - If Criminal: Focus on IPC sections related to offenses, penalties, and FIRs.\n"
        "   - If Civil: Focus on property, contract, or specific civil codes (if applicable) or relevant IPC sections for negligence/nuisance.\n"
        "3. **Retrieve**: Identify and retrieve the top 3-5 most relevant IPC sections.\n\n"
        "IMPORTANT: The user's language preference is: {language_preference}\n"
        "- If the preference is 'hindi', append '[hindi]' to your search query AND present your response in Hindi\n"
        "- If 'english', append '[english]' to your search query AND present your response in English\n"
        "- If 'both', append '[all]' to your search query AND present your response showing both languages\n\n"
        "Example: If searching for theft in Hindi, your query should be: 'theft laws [hindi]' and your response should be in Hindi.\n\n"
        "Return the results in the user's preferred language in clean JSON format with the following fields:\n"
        "- `section` or `page` (depending on source)\n"
        "- `language` (english/hindi)\n"
        "- `content`\n"
        "- `granularity` (section/page)"
    ),
    expected_output=(
        "```json\n"
        "[\n"
        "  {\n"
        "    \"section\": \"73\",\n"
        "    \"language\": \"english\",\n"
        "    \"granularity\": \"section\",\n"
        "    \"content\": \"Section 73: When a contract has been broken...\"\n"
        "  },\n"
        "  { ... },\n"
        "  { ... }\n"
        "]\n"
        "```"
    )
)
