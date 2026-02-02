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

# Helper to clear session state
def reset_session():
    for key in list(st.session_state.keys()):
        del st.session_state[key]

    

# Initialize input in session state if not present
if 'input_text' not in st.session_state:
    st.session_state['input_text'] = ""

# --- Voice Input Section ---
st.markdown("### 🎙️ Voice Input")
from audio_recorder_streamlit import audio_recorder
import google.generativeai as genai
import os

audio_bytes = audio_recorder( text="", recording_color="#e8b62c", neutral_color="#6aa36f", icon_name="microphone", icon_size="2x")

if audio_bytes:
    # Check if this precise audio buffer has been processed to avoid re-transcribing same bytes on casual reruns
    # A simple hash or length check could be used, but for now we rely on the component behavior.
    
    st.info("🎧 Transcribing audio...")
    try:
        # Configure GenAI with the API Key
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        
        # Generate content from audio bytes
        response = model.generate_content([
            "Transcribe the following legal issue description exactly into English or Hindi as spoken.",
            {"mime_type": "audio/mp3", "data": audio_bytes}
        ])
        
        # Update session state with transcribed text
        st.session_state['input_text'] = response.text
        st.success("✅ Transcription Complete!")
    except Exception as e:
        st.error(f"❌ Transcription failed: {e}")

submitted = False
with st.form("legal_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        # Use value from session state to persist changes
        # Note: If user types manually, st.session_state['input_text'] will NOT auto-update unless we add a callback or key.
        # But text_area state is usually preserved by Streamlit if key is consistent. 
        # Here we use 'value' to force overwrite when voice input updates.
        user_input = st.text_area("📝 Describe your legal issue (Type or Speak):", value=st.session_state['input_text'], height=250)
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
    
    submitted_analyze = st.form_submit_button("🔍 Analyze Legal Issue")

if submitted_analyze:
    if not user_input.strip():
        st.warning("Please enter a legal issue to analyze.")
    else:
        with st.spinner("🛡️ Analyzing your case strategy..."):
            from crew import advisory_crew
            from utils.retry_handler import execute_crew_with_retry
            
            try:
                # Stage 1: Advisory
                advisory_result = execute_crew_with_retry(advisory_crew, inputs={
                    "user_input": user_input,
                    "language_preference": language_pref
                })
                
                # Store results in session state
                st.session_state['advisory_result'] = advisory_result
                st.session_state['user_input'] = user_input
                st.session_state['language_pref'] = language_pref
                st.session_state['lawyer_email'] = lawyer_email
                st.session_state['send_lawyer_email'] = send_lawyer_email
                st.session_state['stage'] = "advisory_done"
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {e}")
                st.stop()

# --- Post-Analysis Logic ---
if st.session_state.get('stage') == "advisory_done":
    result = st.session_state['advisory_result']
    
    # Display Advisory Output
    import json
    try:
        # Task 1 output is the Advisory JSON
        if hasattr(result, 'tasks_output') and len(result.tasks_output) > 1:
            advisory_output_raw = result.tasks_output[1].raw
            clean_json = advisory_output_raw.replace("```json", "").replace("```", "").strip()
            advisory_data = json.loads(clean_json)
            
            st.markdown("---")
            st.subheader("🛡️ Strategic Legal Advice")
            
            severity = advisory_data.get('severity', 'Unknown')
            legal_type = advisory_data.get('legal_type', 'General')
            action = advisory_data.get('recommended_action', 'Review Case')
            guidance = advisory_data.get('step_guidance', 'Please consult a lawyer.')

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.info(f"**Severity**: {severity}")
            with col_b:
                st.warning(f"**Type**: {legal_type}")
            with col_c:
                st.error(f"**Action**: {action}")
            
            st.markdown(f"**👉 Immediate Step Guidance:**\n> {guidance}")
            st.markdown("---")
            
            # Store structured data for Stage 2
            st.session_state['advisory_json'] = advisory_output_raw
            st.session_state['case_summary'] = result.tasks_output[0].raw # Intake summary
            
    except Exception as e:
        st.error(f"Could not parse advisory output: {e}")

    # Stage 2 Trigger
    st.info("💡 Would you like to generate the formal legal document recommended above?")
    if st.button("📄 Generate Legal Document"):
        with st.spinner("📝 Drafting document (Researching IPC & Precedents)..."):
            from crew import drafting_crew
            from utils.retry_handler import execute_crew_with_retry
            
            try:
                # Stage 2: Drafting
                draft_result = execute_crew_with_retry(drafting_crew, inputs={
                    "case_summary": st.session_state['case_summary'],
                    "advisory_analysis": st.session_state['advisory_json'],
                    "language_preference": st.session_state['language_pref']
                })
                st.session_state['final_result'] = draft_result
                st.session_state['stage'] = "complete"
                st.rerun() # Rerun to show final result
            except Exception as e:
                 st.error(f"❌ Drafting failed: {e}")

if st.session_state.get('stage') == "complete":
    final_result = st.session_state.get('final_result')
    st.subheader("📄 Final Legal Document")
    st.markdown(str(final_result))
    
    # Logic to send email if requested
    if st.session_state.get('send_lawyer_email'):
        lawyer_email = st.session_state.get('lawyer_email')
        if not lawyer_email or "@" not in lawyer_email:
            st.warning("⚠️ Could not send email: Invalid address provided.")
        else:
            from tools.email_tool import send_email_smtp
            subject = "Consultation Request — Legal Document"
            email_res = send_email_smtp(to_email=lawyer_email, subject=subject, body=str(final_result))
            if email_res.get("ok"):
                st.success(f"✅ Email sent to {lawyer_email}")
            else:
                st.error(f"❌ Email failed: {email_res.get('error', 'Unknown error')}")

    st.success("✅ Document Generation Complete!")
    if st.button("🔄 Start New Case"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
