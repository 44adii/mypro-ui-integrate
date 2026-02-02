from crewai import Task
from agents.advisory_agent import advisory_agent

advisory_task = Task(
    description=(
        "Analyze the user's legal issue listed freely below:\n"
        "{user_input}\n\n"
        "Your job is to apply the following decision logic:\n"
        "1. **Severity Assessment**: Is it High (Violence, Major Theft, Immediate Danger) or Low (Nuisance, Refund, Minor Dispute)?\n"
        "2. **Classification**: \n"
        "   - **Criminal** (Theft, Assault, Fraud) -> Requires Police/FIR.\n"
        "   - **Civil** (Property, Contract, Family) -> Requires Lawyer/Notice.\n"
        "   - **Consumer/Other** (Defective Product, Service Issue) -> Requires Consumer Forum/RWA.\n"
        "4. **Action Path**: Recommend ONE immediate step: 'File FIR', 'Send Legal Notice', or 'File Complaint near Authority'.\n\n"
        "You MUST return the output as a Valid JSON string with these keys: 'severity', 'legal_type', 'recommended_action', 'step_guidance'.\n"
        "IMPORTANT: 'step_guidance' must be a detailed, numbered list (Markdown format) explaining exactly what the user should do next."
    ),
    expected_output=(
        "A valid JSON string. Example:\n"
        "{\n"
        "  \"severity\": \"High\",\n"
        "  \"legal_type\": \"Criminal\",\n"
        "  \"recommended_action\": \"File FIR\",\n"
        "  \"step_guidance\": \"Go to the nearest Police Station and meet the Station House Officer (SHO).\"\n"
        "}"
    ),
    agent=advisory_agent
)
