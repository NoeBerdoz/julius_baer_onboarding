import logging

from flask import Flask

import config
from dto.requests import GameStartRequestDTO, GameDecisionRequestDTO
from services.player import Player

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':

    player = Player()
    player.play_on_separate_thread()

    app.run()
