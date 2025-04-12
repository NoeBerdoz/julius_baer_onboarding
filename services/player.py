import logging
import threading
import time
from typing import Literal, Dict, Any
import config
from dto.requests import GameStartRequestDTO, GameDecisionRequestDTO
from services.julius_baer_api_client import JuliusBaerApiClient
from utils.storage.game_files_manager import store_game_round_data

log = logging.getLogger(__name__)


class Player:

    def __init__(self):
        self.client = JuliusBaerApiClient()
        self._thread = None

    def start(self):
        self.play()

    def play_on_separate_thread(self):
        if self._thread and self._thread.is_alive():
            log.warning('Game loop already running.')
            return self._thread

        self._thread = threading.Thread(target=self.play, daemon=True)
        self._thread.start()
        return self._thread

    def play(self):
        log.info('playing')
        payload = GameStartRequestDTO(player_name=config.API_TEAM)
        start_response = self.client.start_game(payload)
        log.info('game started, session id: %s', start_response.session_id)

        status = ''
        decision = self.make_decision(start_response.client_data)

        decision_counter = 0

        while status not in ['gameover', 'complete']:
            payload = GameDecisionRequestDTO(
                decision=decision,
                session_id=start_response.session_id,
                client_id=start_response.client_id,
            )

            decision_response = self.client.send_decision(payload)
            log.info(f'decision: {decision}, response status: {decision_response.status}, score: {decision_response.score}')
            status = decision_response.status
            decision = self.make_decision(decision_response.client_data)

            # Handle first response from game initialization logic
            if decision_counter == 0:
                # Store start response
                store_game_round_data(decision, start_response, decision_counter, str(start_response.session_id) ,status)
            else:
                # store ongoing decision response
                store_game_round_data(decision, decision_response, decision_counter, str(start_response.session_id), status)

            decision_counter += 1
            time.sleep(1.5)



    def make_decision(self, client_data: Dict[str, Any]) -> Literal["Accept", "Reject"]:
        # Do your magic!

        return 'Accept'

        # import random
        # return random.choice(["Accept", "Reject"])


if __name__ == '__main__':
    player = Player()
    player.start()





