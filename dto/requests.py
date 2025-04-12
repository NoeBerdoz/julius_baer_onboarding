from pydantic import BaseModel
from typing import Literal
from uuid import UUID


class GameStartRequestDTO(BaseModel):
    """Request model for starting a new game."""
    player_name: str


class GameDecisionRequestDTO(BaseModel):
    """Request model for making a game decision."""
    decision: Literal["Accept", "Reject"]
    session_id: UUID
    client_id: UUID
