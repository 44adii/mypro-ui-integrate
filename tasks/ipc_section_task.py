# ipc_section_task.py

from crewai import Task
from agents.ipc_section_agent import ipc_section_agent
from tasks.case_intake_task import case_intake_task

ipc_section_task = Task(
    agent=ipc_section_agent,
    context=[case_intake_task],
    async_execution=True,
    description=(
        "You are provided with the structured legal context generated from the previous task.\n\n"
        "Your job is to identify and retrieve the most relevant sections from the Indian Penal Code (IPC) "
        "that apply to this legal issue. Use your tool to search and extract the top 3-5 most relevant IPC sections.\n\n"
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
