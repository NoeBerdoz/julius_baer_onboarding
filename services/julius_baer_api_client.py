import requests
import config
import logging
from dto.requests import GameStartRequestDTO, GameDecisionRequestDTO
from dto.responses import GameStartResponseDTO, GameDecisionResponseDTO


class JuliusBaerApiClient:
    """
    Client for interacting with the Julius Baer API service.

    Provides methods to start a game and make game decisions.
    """

    def __init__(self):
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
        logging.debug("[+] Starting new game session")
        start_uri = f"{self.api_uri}/game/start"
        payload = game_start_request.model_dump_json()

        try:
            response = requests.post(start_uri, data=payload, headers=self.headers)
            response.raise_for_status()

            response_json = response.json()
            validated_response = GameStartResponseDTO.model_validate(response_json)
            logging.debug(f"Game started successfully. Session: {validated_response.session_id}, Client: {validated_response.client_id}")

            return validated_response
        except Exception as e:
            logging.error(f"[!] Failed to start game session: {e}")
            raise

    def send_decision(self, game_decision_request: GameDecisionRequestDTO) -> GameDecisionResponseDTO:
        """
        Make a game decision (Accept or Reject).
        """
        logging.debug("[+] Sending decision")
        decision_uri = f"{self.api_uri}/game/decision"

        payload = game_decision_request.model_dump_json()

        try:
            response = requests.post(decision_uri, data=payload, headers=self.headers)
            response.raise_for_status()

            response_json = response.json()
            validated_response = GameDecisionResponseDTO.model_validate(response_json)
            logging.debug("[+] Decision sent successfully")

            return validated_response
        except Exception as e:
            logging.error(f"[!] Failed to send a decision: {e}")
            raise
