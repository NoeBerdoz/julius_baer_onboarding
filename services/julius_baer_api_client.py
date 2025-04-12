from typing import Dict, Any

import requests

import config
from dto.requests import GameStartRequest, GameDecisionRequest


class JuliusBaerApiClient:
    """
    Client for interacting with the Julius Baer API service.

    Provides methods to start a game and make game decisions.
    """

    def __init__(self):
        self.api_uri = config.API_URI
        self.api_key = config.API_KEY
        self.api_team = config.API_TEAM

    def start_game(self, game_start_request: GameStartRequest) -> Dict[str, Any]:
        """
        Start a new game session.

        Args:
            player_name: Name of the player.

        Returns:
            Dict containing the game start response with session_id, player_id, etc.
        """
        url = f"{self.api_uri}/game/start"
        payload = {"player_name": game_start_request.player_name}

        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors

        data = response.json()

        # Store session_id and client_id for convenience in future calls
        self.session_id = data.get("session_id")
        self.client_id = data.get("client_id")

        return data

    def make_decision(self, game_decision_request: GameDecisionRequest) -> Dict[str, Any]:
        """
        Make a game decision (Accept or Reject).

        Args:
            decision: Either "Accept" or "Reject".
            session_id: Unique session ID for the game. If None, uses the stored session_id.
            client_id: Unique client ID for the game. If None, uses the stored client_id.

        Returns:
            Dict containing the game decision response with status, score, etc.

        Raises:
            ValueError: If decision is not "Accept" or "Reject".
            ValueError: If session_id and client_id are not provided or stored from a previous start_game call.
        """
        if game_decision_request.decision not in ["Accept", "Reject"]:
            raise ValueError('Decision must be either "Accept" or "Reject"')

        # Use stored values if not provided
        session_id = game_decision_request.session_id or self.session_id
        client_id = game_decision_request.client_id or self.client_id

        if not session_id or not client_id:
            raise ValueError(
                "Session ID and Client ID are required. Either provide them explicitly or call start_game first.")

        url = f"{self.base_url}/game/decision"
        payload = {
            "decision": game_decision_request.decision,
            "session_id": session_id,
            "client_id": client_id
        }

        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors

        return response.json()
