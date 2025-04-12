from flask import Flask

from dto.requests import GameStartRequestDTO
from services.julius_baer_api_client import JuliusBaerApiClient

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    jb_client = JuliusBaerApiClient()
    game_start_request = GameStartRequestDTO(player_name="Welch")
    res = jb_client.start_game(game_start_request)
    print(res)

    app.run()
