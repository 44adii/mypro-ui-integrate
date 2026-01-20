# app.py

import streamlit as st
from dotenv import load_dotenv

# Load environment BEFORE importing anything that constructs LLMs
load_dotenv()

# Imports moved to lazy loading functions to speed up app startup
# from crew import legal_assistant_crew
# from tools.email_tool import send_email_smtp

st.set_page_config(page_title="AI Legal Assistant", page_icon="🧠", layout="wide")

st.title("⚖️ Personal AI Legal Assistant")
st.markdown(
    "Enter a legal problem in plain English or Hindi. This assistant will help you:\n"
    "- Understand the legal issue\n"
    "- Find applicable IPC sections\n"
    "- Retrieve matching precedent cases\n"
    "- Generate a formal legal document"
)

@st.cache_resource
def load_crew():
    """Lazy load the crew to avoid app startup delay."""
    from crew import legal_assistant_crew
    return legal_assistant_crew

with st.form("legal_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        user_input = st.text_area("📝 Describe your legal issue:", height=250)
    with col2:
        language_pref = st.selectbox(
            "🌐 Response Language",
            options=["english", "hindi", "both"],
            index=0,
            help="Choose your preferred language for the legal response"
        )
        lawyer_email = st.text_input(
            "📧 Lawyer Email (optional)",
            help="Provide a nearby lawyer's email to send the final document"
        )
        send_lawyer_email = st.checkbox("Send final document to lawyer", value=False)
    
    submitted = st.form_submit_button("🔍 Run Legal Assistant")

if submitted:
    if not user_input.strip():
        st.warning("Please enter a legal issue to analyze.")
    else:
        with st.spinner("🔎 Analyzing your case and preparing legal output..."):
            legal_crew = load_crew()
            
            from utils.retry_handler import execute_crew_with_retry
            
            try:
                result = execute_crew_with_retry(legal_crew, inputs={
                    "user_input": user_input,
                    "language_preference": language_pref
                })
            except Exception as e:
                st.error(f"❌ Execution failed: {e}")
                st.stop()

        st.success("✅ Legal Assistant completed the workflow!")

        # Display all task outputs
        st.subheader("📄 Final Legal Document")
        final_result = str(result)
        st.markdown(final_result)

        # Optionally send the final document via email
        if send_lawyer_email:
            if not lawyer_email or "@" not in lawyer_email:
                st.warning("Please enter a valid lawyer email address to send the document.")
            else:
                subject = "Consultation Request — Legal Document"
                body = final_result
                from tools.email_tool import send_email_smtp
                email_res = send_email_smtp(to_email=lawyer_email, subject=subject, body=body)
                if email_res.get("ok"):
                    st.success(f"✅ Email sent to {lawyer_email}")
                else:
                    st.error(f"❌ Email failed: {email_res.get('error', 'Unknown error')}")
        
        # Show all intermediate outputs if available
        if hasattr(result, 'tasks_output'):
            with st.expander("📊 View All Task Outputs", expanded=False):
                for i, task_output in enumerate(result.tasks_output, 1):
                    st.markdown(f"### Task {i} Output")
                    st.text(task_output.raw)
                    st.markdown("---")
        elif hasattr(result, 'tasks'):
            with st.expander("📊 View All Task Outputs", expanded=False):
                for i, task in enumerate(result.tasks, 1):
                    if hasattr(task, 'output'):
                        st.markdown(f"### Task {i} Output")
                        st.text(str(task.output))
                        st.markdown("---")
