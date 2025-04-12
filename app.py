import logging

from flask import Flask

import config
from dto.requests import GameStartRequestDTO
from services.julius_baer_api_client import JuliusBaerApiClient

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(module)s] - %(message)s')
jb_client = JuliusBaerApiClient()


@app.route('/new-game', methods=['POST'])
def new_game():
    game_start_request = GameStartRequestDTO(player_name=config.API_TEAM)
    res = jb_client.start_game(game_start_request)

    return res.model_dump_json()


if __name__ == '__main__':
    app.run()
