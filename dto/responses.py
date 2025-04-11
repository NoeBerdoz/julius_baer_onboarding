from dataclasses import dataclass
from typing import Dict, Optional, Any
from uuid import UUID


@dataclass
class GameStartResponse:
    """Response model for a new game started."""
    message: str
    session_id: UUID
    player_id: str
    client_id: UUID
    client_data: Dict[str, Any]
    score: int


@dataclass
class GameDecisionResponse:
    """Response model for a game decision result."""
    status: str
    score: int
    client_id: Optional[UUID] = None
    client_data: Optional[Dict[str, Any]] = None
