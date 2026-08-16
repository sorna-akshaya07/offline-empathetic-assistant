import re
from datetime import datetime


# ---------------------------------------------------------
# Unsafe Content Detection Rules
# ---------------------------------------------------------

UNSAFE_PATTERNS = [
    r"\bhow to hack\b",
    r"\bhack into\b",
    r"\bsteal\b.*\bpassword\b",
    r"\bmake a bomb\b",
    r"\bkill myself\b",
    r"\bcommit suicide\b",
    r"\bself[- ]harm\b",
    r"\bhurt myself\b",
    r"\bhow to hurt\b.*\bmyself\b",
]

# ---------------------------------------------------------
# Safe Fallback Response
# ---------------------------------------------------------

SAFE_FALLBACK = (
    "I'm sorry, but I can't help with that. "
    "I'm here to listen and support you in a safe way."
)

# ---------------------------------------------------------
# Safety Event Logging
# ---------------------------------------------------------

def log_safety_event(event_type: str, text: str):
    """Record safety-related events separately."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("safety_events.log", "a", encoding="utf-8") as log_file:
        log_file.write(
            f"[{timestamp}] {event_type}: {text}\n"
        )

# ---------------------------------------------------------
# Check User Input for Unsafe Content
# ---------------------------------------------------------

def is_unsafe(text: str) -> bool:
    """Check whether the text contains unsafe content."""

    if not text or not text.strip():
        return True

    text = text.lower()

    for pattern in UNSAFE_PATTERNS:
        if re.search(pattern, text):
            return True

    return False

# ---------------------------------------------------------
# Validate and Sanitize LLM-Generated Response
# ---------------------------------------------------------

def validate_response(reply_text: str) -> str:
    """Validate model response and return a safe response."""

    if not reply_text or not reply_text.strip():
        log_safety_event("EMPTY_RESPONSE", "Model returned an empty response")
        return SAFE_FALLBACK

    if is_unsafe(reply_text):
        log_safety_event("UNSAFE_RESPONSE", reply_text)
        return SAFE_FALLBACK

    return reply_text.strip()