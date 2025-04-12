import logging
from typing import Literal, Dict, Any
import config
from dto.requests import GameStartRequestDTO, GameDecisionRequestDTO
from services.julius_baer_api_client import JuliusBaerApiClient


class Player:

    def __init__(self):
        self.client = JuliusBaerApiClient()

    def start(self):
        self.play()

    def play(self):
        payload = GameStartRequestDTO(player_name=config.API_TEAM)
        start_response = self.client.start_game(payload)
        logging.info(start_response)

        status = ''
        decision = self.make_decision(start_response.client_data)
        while status != 'gameover':

            payload = GameDecisionRequestDTO(
                decision=decision,
                session_id=start_response.session_id,
                client_id=start_response.client_id,
            )

            decision_response = self.client.send_decision(payload)
            logging.info(decision_response)
            status = decision_response.status
            decision = self.make_decision(decision_response.client_data)


    def make_decision(self, client_data: Dict[str, Any]) -> Literal["Accept", "Reject"]:
        # Do your magic!

        return 'Accept'

        # import random
        # return random.choice(["Accept", "Reject"])


if __name__ == '__main__':
    player = Player()
    player.start()





