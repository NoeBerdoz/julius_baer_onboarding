import logging
import threading
import time
from typing import Literal, Dict, Any
import config
from dto.requests import GameStartRequestDTO, GameDecisionRequestDTO
from services.julius_baer_api_client import JuliusBaerApiClient


class Player:

    def __init__(self):
        self.client = JuliusBaerApiClient()
        self._thread = None

    def start(self):
        self.play()

    def play_on_separate_thread(self):
        if self._thread and self._thread.is_alive():
            logging.warning('Game loop already running.')
            return self._thread

        self._thread = threading.Thread(target=self.play, daemon=True)
        self._thread.start()
        return self._thread

    def play(self):
        print('playing')
        payload = GameStartRequestDTO(player_name=config.API_TEAM)
        start_response = self.client.start_game(payload)
        logging.info(start_response)

        status = ''
        decision = self.make_decision(start_response.client_data)
        while status not in ['gameover', 'complete']:

            payload = GameDecisionRequestDTO(
                decision=decision,
                session_id=start_response.session_id,
                client_id=start_response.client_id,
            )

            decision_response = self.client.send_decision(payload)
            print(decision_response.status, decision_response.score)
            status = decision_response.status
            decision = self.make_decision(decision_response.client_data)
            time.sleep(1.5)

    def make_decision(self, client_data: Dict[str, Any]) -> Literal["Accept", "Reject"]:
        # Do your magic!

        return 'Accept'

        # import random
        # return random.choice(["Accept", "Reject"])


if __name__ == '__main__':
    player = Player()
    player.start()





