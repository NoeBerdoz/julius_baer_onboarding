import logging
import threading
import time
from typing import Literal, Dict, Any
import config
from dto.requests import GameStartRequestDTO, GameDecisionRequestDTO
from services.extractor import extract_profile, extract_passport, extract_description, extract_account
from services.julius_baer_api_client import JuliusBaerApiClient
from utils.storage.game_files_manager import store_game_round_data
from langchain_google_genai import ChatGoogleGenerativeAI
from validation.llm_validate import AssistantDecision
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser


log = logging.getLogger(__name__)


class Advisor:

    def __init__(self):
        self.client = JuliusBaerApiClient()
        self._thread = None

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
            client_id = decision_response.client_id

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
        # 1. Extraction des données
        profile = extract_profile(client_data)
        passport = extract_passport(client_data)
        description = extract_description(client_data)
        account = extract_account(client_data)

        # 2. Création du parser
        parser = PydanticOutputParser(pydantic_object=AssistantDecision)
        format_instructions = parser.get_format_instructions()

        # 3. Prompt enrichi
        prompt = ChatPromptTemplate.from_template(
            """You are a compliance analyst in a private bank.
    You are given structured data extracted from four different documents of a new client application.

    Your task is to accept or reject the client's application for private banking.

    Only reject the application if there is an inconsistency in the data provided.
    Inconsistencies include:
    - Incorrect data (e.g., mismatched or invalid information)
    - Incomplete data (e.g., missing required fields)
    - Implausible or suspicious details

    Use the extracted profile, description, and account details to cross-check the information in the passport and other documents.

    Be highly critical. Reject if there's any doubt or if anything feels wrong.

    Return only JSON matching this format:
    {format_instructions}

    ---

    **Document: Passport**
    {passport}

    ---

    **Document: Profile**
    {profile}

    ---

    **Document: Description**
    {description}

    ---

    **Document: Account**
    {account}"""
        )

        # 4. Chaîne LLM
        chain = prompt | ChatGoogleGenerativeAI(model="gemini-pro") | parser

        # 5. Invocation
        result: AssistantDecision = chain.invoke({
            "passport": passport.json(),
            "profile": profile.json(),
            "description": description.json(),
            "account": account.json(),
            "format_instructions": format_instructions,
        })

        # 6. Logs et retour
        if result.decision == "Reject":
            log.warning(f"Client rejected. Reason: {result.reason}")
        else:
            log.info("Client accepted.")

        return result.decision
