import requests
import config
import logging
from typing import Dict, Any
from dto.requests import GameStartRequestDTO, GameDecisionRequestDTO
from dto.responses import GameStartResponseDTO


class JuliusBaerApiClient:
    """
    Client for interacting with the Julius Baer API service.

    Provides methods to start a game and make game decisions.
    """

    def __init__(self):
        self.client_id = None
        self.session_id = None
        self.api_uri = config.API_URI
        self.api_key = config.API_KEY
        self.api_team = config.API_TEAM

        if not self.api_uri or not self.api_key or not self.api_team:
            logging.error("[!] API credentials are not configured, edit .env file")

        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def start_game(self, game_start_request: GameStartRequestDTO) -> GameStartResponseDTO:
        """
        Start a new game session.
        """
        logging.info("[+] Starting new game session")
        start_url = f"{self.api_uri}/game/start"
        payload = game_start_request.model_dump()  # Convert GameStartRequestDTO to dict for JSON

        try:
            response = requests.post(start_url, json=payload, headers=self.headers)
            response.raise_for_status()  # Raise exception for HTTP errors

            response_data = response.json()
            validated_response = GameStartResponseDTO.model_validate(response_data)
            logging.info(f"Game started successfully. Session: {validated_response.session_id}, Client: {validated_response.client_id}")


            # Store session_id and client_id for future calls
            self.session_id = validated_response.session_id
            self.client_id = validated_response.client_id

            return validated_response

        except Exception as e:
            logging.error(f"[!] Failed to start game session: {e}")
            raise

    def make_decision(self, game_decision_request: GameDecisionRequestDTO) -> Dict[str, Any]:
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
