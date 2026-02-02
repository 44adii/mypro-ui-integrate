from dotenv import load_dotenv
import os
import sys

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

try:
    print("1. Importing Crew...")
    from crew import advisory_crew
    print("2. Crew Imported.")

    inputs = {
        "user_input": "My neighbor is threatening me over a property dispute.",
        "language_preference": "English"
    }

    print("3. Starting Crew Execution...")
    # executing directly without retry handler first to see raw errors
    result = advisory_crew.kickoff(inputs=inputs)
    
    print("4. Execution Complete!")
    print("\n\nRESULT:")
    print(result)

except Exception as e:
    print(f"\nCRITICAL FAIL: {e}")
    import traceback
    traceback.print_exc()
