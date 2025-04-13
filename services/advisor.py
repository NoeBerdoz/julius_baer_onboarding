import logging
import threading
import time
from typing import Literal, Dict, Any
import config
from dto.requests import GameStartRequestDTO, GameDecisionRequestDTO
from services.extractor import extract_profile, extract_passport, extract_description, extract_account
from services.julius_baer_api_client import JuliusBaerApiClient
from utils.storage.game_files_manager import store_game_round_data
from langchain_openai.chat_models import ChatOpenAI
from validation.llm_validate import AdvisorDecision
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
                decision=decision.answer,
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
                store_game_round_data(decision.answer, start_response, decision_counter, str(start_response.session_id) ,status)
            else:
                # store ongoing decision response
                store_game_round_data(decision.answer, decision_response, decision_counter, str(start_response.session_id), status)

            decision_counter += 1
            time.sleep(1)

    def make_decision(self, client_data: Dict[str, Any]) -> AdvisorDecision:
        # 1. Extraction des données
        profile = extract_profile(client_data)
        passport = extract_passport(client_data)
        description = extract_description(client_data)
        account = extract_account(client_data)

        # 2. Création du parser
        parser = PydanticOutputParser(pydantic_object=AdvisorDecision)
        format_instructions = parser.get_format_instructions()

        # 3. Prompt enrichi
        prompt = ChatPromptTemplate.from_template(
            """You are a compliance analyst in a private bank.
    You are given structured data extracted from four different documents of a new client application.

    Your task is to accept or reject the client's application for private banking.

    Only reject the application if there is an inconsistency in the data provided.
    
    Inconsistencies include:
    - Incorrect names used accros all docs, what is stated in one of the doc should be true on other documents.
    - Check for typos
    - Incorrect validity date passport or documents
    - Wrong address, city, street name, zip code and country
    - Only one domicile
    - Implausible or suspicious details
    - Amounts in profile and the description file
    - Incorrect nationality regarding the passport data

    Use the extracted profile, description, and account details to cross-check the information in the passport and other documents.
    Take into consideration that occupation history might be in the past not match the actual situation.
    Pay attention to the currency when dealing with amounts.
    Be highly critical. Reject if there's any doubt or if anything feels wrong.
    DO NOT HALLUCINATE at any point ! 

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
        chain = prompt | ChatOpenAI(model="gpt-4o-mini") | parser

        # 5. Invocation
        result: AdvisorDecision = chain.invoke({
            "passport": passport,
            "profile": profile,
            "description": description,
            "account": account,
            "format_instructions": format_instructions,
        })

        # 6. Logs et retour
        if result.answer == "Reject":
            log.warning(f"Client rejected. Reason: {result.reason}")
        else:
            log.info("Client accepted.")

        return result
