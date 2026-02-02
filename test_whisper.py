from faster_whisper import WhisperModel
import sys

print("Starting Import Test...")
try:
    print("Initializing Model...")
    # forcing cpu/int8
    model = WhisperModel("base", device="cpu", compute_type="int8")
    print("Model Initialized Successfully!")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
