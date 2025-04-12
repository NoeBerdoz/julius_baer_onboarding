from dto.requests import GameStartRequestDTO
from services.extractor import run_extraction_chain
from services.julius_baer_api_client import JuliusBaerApiClient
from validation.from_passport import FromPassport

from services.player import Player
from utils.parsers import process_passport
from flask import Flask
import config

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
