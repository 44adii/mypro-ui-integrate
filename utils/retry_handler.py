
import time
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Try to import the specific exception. If not available, we can use a broader one or search litellm
try:
    from litellm.exceptions import RateLimitError
except ImportError:
    # If using crewai's internal handling, sometimes we just catch generic Exception but check message
    # For now, let's catch generic Exception and check string in decorator or handle inside
    RateLimitError = Exception 

def log_retry_attempt(retry_state):
    """Callback to log retry attempts"""
    print(f"⚠️ Rate Limit Hit! Retrying in {retry_state.next_action.sleep} seconds... (Attempt {retry_state.attempt_number})")

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=2, max=60),
    retry=retry_if_exception_type((Exception,)), # Catching broad exception to filter msg
    before_sleep=log_retry_attempt
)
def execute_crew_with_retry(crew, inputs):
    """
    Executes a CrewAI crew with auto-retry logic for RateLimitErrors.
    """
    try:
        return crew.kickoff(inputs=inputs)
    except Exception as e:
        error_msg = str(e).lower()
        if "rate limit" in error_msg or "429" in error_msg:
             # Re-raise to let tenacity handle it
             raise e
        else:
            # Explicitly raise the original exception context
            import traceback
            traceback.print_exc()
            raise e
