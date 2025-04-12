from pydantic import BaseModel
from typing import Literal, Optional

class AssistantDecision(BaseModel):
    decision: Literal["Accept", "Reject"]
    reason: Optional[str] = None