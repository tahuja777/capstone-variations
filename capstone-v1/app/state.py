from typing import Optional, List, Dict
from pydantic import BaseModel

class NovaState(BaseModel):
    query: str
    intent: Optional[str] = None

    # final synthesized answer to user
    answer: Optional[str] = ""

    # evidence collected from tools
    evidence: Optional[List[str]] = []

    # errors collected from tools or LLM
    errors: Optional[List[str]] = []

    # conversational history
    history: List[str] = []

    # Storing tools result
    tool_result: Optional[Dict] = None
