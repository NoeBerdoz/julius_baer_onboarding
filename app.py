import logging

from flask import Flask, request
from flask_cors import cross_origin

import config
from dto.requests import GameStartRequestDTO, GameDecisionRequestDTO
from dto.responses import GameStartResponseWithBotDecisionDTO
from services.julius_baer_api_client import JuliusBaerApiClient
from services.player import Player

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(module)s] - %(message)s')
jb_client = JuliusBaerApiClient()


@app.route('/new-game', methods=['POST'])
@cross_origin() # allow all origins all methods
def new_game():
    # game_start_request = GameStartRequestDTO(player_name=config.API_TEAM)
    # res = jb_client.start_game(game_start_request)
    player = Player()
    player.play_on_separate_thread()

    res_with_bot_decision = GameStartResponseWithBotDecisionDTO(
        message=res.message,
        session_id=res.session_id,
        player_id=res.player_id,
        client_id=res.client_id,
        client_data=res.client_data,
        score=res.score,
        bot_decision="Accept" # TODO: Get decision from bot
    )

    return res_with_bot_decision.model_dump_json()


@app.route('/next', methods=['POST'])
@cross_origin() # allow all origins all methods
def next_client():
    body = request.get_json()

    decision = body.get("decision")
    client_id = body.get("client_id")
    session_id = body.get("session_id")

    make_decision_request = GameDecisionRequestDTO(decision=decision, client_id=client_id, session_id=session_id)
    res = jb_client.send_decision(make_decision_request)

    return res.model_dump_json()

if __name__ == '__main__':
    app.run()
