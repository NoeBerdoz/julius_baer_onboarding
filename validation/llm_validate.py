from pydantic import BaseModel
from typing import Literal, Optional

class AdvisorDecision(BaseModel):
    answer: Literal["Accept", "Reject"]
    reason: Optional[str] = None