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

    # res.session_id
    # UUID('fde19363-a3d5-432e-8b87-54a6dd54f0dd')
    # second test UUID('e3d58302-400a-4bc6-9772-ae50de43c9f4')
    # UUID('f8b2a0a6-d4e0-45e6-900f-8ecb3c28f993')
    # UUID('f8b2a0a6-d4e0-45e6-900f-8ecb3c28f993')