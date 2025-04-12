from pydantic import BaseModel
from typing import Dict, Optional, Any, Literal
from uuid import UUID


class GameStartResponseDTO(BaseModel):
    """Response model for a new game started."""
    message: str
    session_id: UUID
    player_id: str
    client_id: UUID
    client_data: Dict[str, Any]
    score: int

class GameStartResponseWithBotDecisionDTO(BaseModel):
    """Response model to send to frontend after a new game started."""
    message: str
    session_id: UUID
    player_id: str
    client_id: UUID
    client_data: Dict[str, Any]
    score: int
    bot_decision: Literal["Accept", "Reject"]
    bot_reason: str


class GameDecisionResponseDTO(BaseModel):
    """Response model for a game decision result."""
    status: str
    score: int
    client_id: Optional[UUID] = None
    client_data: Optional[Dict[str, Any]] = None

class GameDecisionResponseWithBotDecisionDTO(BaseModel):
    """Response model to send to frontend after a game decision has been sent."""
    status: str
    score: int
    client_id: Optional[UUID] = None
    client_data: Optional[Dict[str, Any]] = None
    bot_decision: Literal["Accept", "Reject"]
    bot_reason: str