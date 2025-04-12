import logging

from flask import Flask

import config
from dto.requests import GameStartRequestDTO
from services.extractor import extract_profile
from services.julius_baer_api_client import JuliusBaerApiClient
from services.player import Player

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - [%(module)s] - %(message)s')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    jb_client = JuliusBaerApiClient()
    game_start_request = GameStartRequestDTO(player_name=config.API_TEAM)
    res = jb_client.start_game(game_start_request)

    result = extract_profile(res.client_data)

    player = Player()
    player.play_on_separate_thread()

    app.run()
