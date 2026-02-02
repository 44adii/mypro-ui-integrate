import sys
import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from faster_whisper import WhisperModel
import uuid

# Ensure we can import from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment
load_dotenv()

# Initialize FastAPI
app = FastAPI()

# Initialize Whisper Model (Global)
# usage="int8" is faster and uses less memory, "cpu" or "cuda" depending on hardware
print("Loading Whisper Model...")
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")
print("Whisper Model Loaded!")

# CORS Setup
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class AnalyzeRequest(BaseModel):
    user_input: str
    language_preference: str = "english"

class DraftRequest(BaseModel):
    case_summary: str
    advisory_analysis: str
    language_preference: str = "english"


# --- Endpoints ---

@app.get("/")
def read_root():
    return {"status": "NyayaGPT Backend Running"}



@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        # Save temp file
        temp_filename = f"temp_{file.filename}"
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"DEBUG: Transcribing {temp_filename}...")
        
        # Transcribe with auto-detection first
        segments, info = whisper_model.transcribe(
            temp_filename, 
            beam_size=5, 
            vad_filter=True,
            initial_prompt="नमस्ते, this is a legal discussion in Hindi and English."
        )

        detected_lang = info.language
        print(f"DEBUG: Detected language: {detected_lang} with probability {info.language_probability}")

        # Fallback: If it thinks it's Urdu (ur) or Arabic (ar), force Hindi (hi)
        # This handles the "Right Language, Wrong Script" issue common in Hinglish.
        if detected_lang not in ['en', 'hi']:
            print(f"DEBUG: Detected {detected_lang}, forcing 'hi' (Hindi)...")
            segments, info = whisper_model.transcribe(
                temp_filename, 
                beam_size=5, 
                vad_filter=True,
                language="hi",
                initial_prompt="नमस्ते, write this in Devanagari script."
            )

        transcribed_text = ""
        for segment in segments:
            transcribed_text += segment.text + " "
            
        print(f"DEBUG: Transcription result: {transcribed_text}")
        
        # Cleanup
        os.remove(temp_filename)
        
        return {"text": transcribed_text.strip()}
    
    except Exception as e:
        print(f"Transcription Error: {e}")
        # Clean up if failed
        if 'temp_filename' in locals() and os.path.exists(temp_filename):
            os.remove(temp_filename)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze")
async def analyze_case(request: AnalyzeRequest):
    try:
        from crew import advisory_crew
        from utils.retry_handler import execute_crew_with_retry
        
        # Run Advisory Crew
        result = execute_crew_with_retry(advisory_crew, inputs={
            "user_input": request.user_input,
            "language_preference": request.language_preference
        })
        
        # Extract Output
        # Task 0: Intake, Task 1: Advisory
        task_output = result.tasks_output[1].raw
        intake_output = result.tasks_output[0].raw
        
        # Basic JSON cleanup if needed (CrewAI sometimes wraps in markdown)
        clean_json = task_output.replace("```json", "").replace("```", "").strip()
        
        return {
            "advisory_json": clean_json,
            "case_summary": intake_output
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Analysis Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/draft")
async def draft_document(request: DraftRequest):
    try:
        from crew import drafting_crew
        from utils.retry_handler import execute_crew_with_retry
        
        # Run Drafting Crew
        result = execute_crew_with_retry(drafting_crew, inputs={
            "case_summary": request.case_summary,
            "advisory_analysis": request.advisory_analysis,
            "language_preference": request.language_preference
        })
        
        # Final result is the output of the whole crew (Drafter is last)
        final_doc = str(result)
        
        return {"document": final_doc}
        
    except Exception as e:
        print(f"Drafting Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run from parent directory context usually, but here we enable running directly
    uvicorn.run(app, host="0.0.0.0", port=8001)
