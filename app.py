from dto.requests import GameStartRequestDTO
from services.extractor import run_extraction_chain
from services.julius_baer_api_client import JuliusBaerApiClient
from validation.from_passport import FromPassport

from services.player import Player
from utils.parsers import process_passport
from flask import Flask
import config

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    jb_client = JuliusBaerApiClient()
    game_start_request = GameStartRequestDTO(player_name=config.API_TEAM)
    res = jb_client.start_game(game_start_request)


    passport_data = res.client_data.get("passport")

    prompt_template = (
        "Extract the following information from the provided passport text.\n"
        "Return only JSON matching this format:\n{format_instructions}\n\n"
        "Pay special attention to the passport number and signature.\n"
        "Passport text:\n{processed_text}"
    )

    result = run_extraction_chain(
        raw_file_data=passport_data,
        file_processor=process_passport,
        pydantic_model=FromPassport,
        prompt_template=prompt_template,
    )

    print(result)

    player = Player()
    player.play_on_separate_thread()

    app.run()

    # res.session_id
    # UUID('fde19363-a3d5-432e-8b87-54a6dd54f0dd')
    # second test UUID('e3d58302-400a-4bc6-9772-ae50de43c9f4')
    # UUID('f8b2a0a6-d4e0-45e6-900f-8ecb3c28f993')
    # UUID('f8b2a0a6-d4e0-45e6-900f-8ecb3c28f993')