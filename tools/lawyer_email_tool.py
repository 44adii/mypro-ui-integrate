# lawyer_email_tool.py

from crewai.tools import tool
from tools.email_tool import send_email_smtp


@tool("Send Lawyer Email")
def send_lawyer_email_tool(to_email: str, subject: str, body: str) -> str:
    """Sends an email to a lawyer with case summary and IPC sections.
    
    Args:
        to_email: The email address to send to
        subject: The email subject line
        body: The email body content
        
    Returns:
        Success or error message
    """
    result = send_email_smtp(to_email=to_email, subject=subject, body=body)
    
    if result.get("ok"):
        return "Email sent successfully"
    else:
        return f"Failed to send email: {result.get('error', 'Unknown error')}"



