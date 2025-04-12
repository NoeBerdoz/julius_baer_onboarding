import logging
import threading
import time
from typing import Literal, Dict, Any
import config
from dto.requests import GameStartRequestDTO, GameDecisionRequestDTO
from services.extractor import extract_profile, extract_passport
from services.julius_baer_api_client import JuliusBaerApiClient
from utils.storage.game_files_manager import store_game_round_data, store_decision, load_decisions
import json
import hashlib


log = logging.getLogger(__name__)


class Player:

    def __init__(self, use_cache = True):
        self.client = JuliusBaerApiClient()
        self._thread = None
        self.cached_decisions = None
        if use_cache:
            self.cached_decisions = self.load_cached_decisions()
            print(self.cached_decisions)

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

        client_id = start_response.client_id
        client_hash = self.hash_obj(start_response.client_data)
        decision = self.make_decision(start_response.client_data)

        decision_counter = 0

        is_game_running = True
        while is_game_running:
            payload = GameDecisionRequestDTO(
                decision=decision,
                session_id=start_response.session_id,
                client_id=client_id,
            )

            log.info('client id: %s', client_id)
            decision_response = self.client.send_decision(payload)
            log.info(f'decision: {decision}, response status: {decision_response.status}, score: {decision_response.score}')

            status = decision_response.status
            is_game_running = status not in ['gameover', 'complete']
            if is_game_running:
                store_decision(client_hash, decision)
            client_id = decision_response.client_id

            client_hash = self.hash_obj(decision_response.client_data)
            decision = self.make_decision(decision_response.client_data)

            # Handle first response from game initialization logic
            if decision_counter == 0:
                # Store start response
                store_game_round_data(decision, start_response, decision_counter, str(start_response.session_id) ,status)
            else:
                # store ongoing decision response
                store_game_round_data(decision, decision_response, decision_counter, str(start_response.session_id), status)

            decision_counter += 1
            time.sleep(1)

    def make_decision(self, client_data: Dict[str, Any]) -> Literal["Accept", "Reject"]:
        # Verify cached data (avoid duplicated call to the LLM)
        client_hash = self.hash_obj(client_data)
        if self.cached_decisions is not None and client_hash in self.cached_decisions.keys():
            print('DECISION TAKE FROM CACHE --------------------------- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            return self.cached_decisions[client_hash]

        # Data extraction

        # profile = extract_profile(client_data)
        # passport = extract_passport(client_data)

        # Do your magic!

        return 'Accept'  # Replace me!!

    def load_cached_decisions(self) -> Dict[str, Literal["Accept", "Reject"]]:
        decisions = load_decisions()
        mapping = {}
        for item in decisions:
            mapping[item['client_hash']] = item['decision']

        return mapping

    @staticmethod
    def hash_obj(obj) -> str:
        obj_str = json.dumps(obj, sort_keys=True)  # make dict order consistent
        return hashlib.sha256(obj_str.encode()).hexdigest()


