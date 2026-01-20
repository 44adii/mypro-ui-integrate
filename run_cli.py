# run_cli.py
import os
import sys
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Import the crew (using the lazy loading pattern if applicable, or direct import)
# We can import directly since this is a script
try:
    from crew import legal_assistant_crew
except ImportError as e:
    print(f"Error importing crew: {e}")
    sys.exit(1)

def main():
    print("\n⚖️  AI Legal Assistant - CLI Mode")
    print("--------------------------------")
    
    # Get input
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        user_input = input("\nEnter your legal issue: ")

    if not user_input.strip():
        print("❌ Error: No input provided.")
        return

    language_pref = input("Language (english/hindi/both) [default: english]: ").strip().lower() or "english"

    print(f"\n🚀 Running Crew with input: '{user_input}' (Lang: {language_pref})...")
    print("   (This may take a minute...)")

    try:
        from utils.retry_handler import execute_crew_with_retry
        
        # Wrapped call with retry logic
        result = execute_crew_with_retry(legal_assistant_crew, inputs={
            "user_input": user_input,
            "language_preference": language_pref
        })
        
        print("\n\n✅ FINAL RESULT\n==============")
        print(result)
        print("\n==============")

    except Exception as e:
        print(f"\n❌ Error running crew (after retries): {e}")

if __name__ == "__main__":
    main()
