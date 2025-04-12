from flask import Flask

from services.julius_baer_api_client import JuliusBaerApiClient

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    jb_client = JuliusBaerApiClient()
    # game_start_request = GameStartRequestDTO(player_name=config.API_TEAM)
    # res = jb_client.start_game(game_start_request)
    #
    # game_decision_request = GameDecisionRequestDTO(decision="Accept", client_id=res.client_id, session_id=res.session_id)
    # decision_response = jb_client.make_decision(game_decision_request)
    #
    # while decision_response.status == "active":
    #     game_decision_request = GameDecisionRequestDTO(decision="Accept", client_id=res.client_id, session_id=res.session_id)
    #     decision_response = jb_client.make_decision(game_decision_request)
    #
    #     if decision_response.status == "gameover":
    #         logging.info("Game over")

    app.run()
