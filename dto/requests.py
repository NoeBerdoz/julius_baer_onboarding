from dataclasses import dataclass
from typing import Literal
from uuid import UUID


@dataclass
class GameStartRequest:
    """Request model for starting a new game."""
    player_name: str


@dataclass
class GameDecisionRequest:
    """Request model for making a game decision."""
    decision: Literal["Accept", "Reject"]
    session_id: UUID
    client_id: UUID
