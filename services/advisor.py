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
            """You are an experienced compliance analyst at a prestigious private bank. Your role is to carefully examine client applications by cross-checking data from four provided documents: Passport, Profile, Description, and Account.

        Your task:
        Determine whether to ACCEPT or REJECT the client’s private banking application based on data consistency.

        CRITICAL RULES for rejection (any single issue means rejection):
        - Mismatch in personal details: names, surnames must match exactly across all documents.
        - Typos or spelling errors in critical information.
        - Expired or incorrect validity dates on passports or other documents.
        - Non-existent or incorrect addresses, including city, street, zip code, and country.
        - Conflicting information regarding country of domicile.
        - Suspicious or implausible personal details.
        - Financial discrepancies between Profile and Description documents.
        - Mismatching nationality between Passport and Account documents.

        ADDITIONAL INSTRUCTIONS:
        - Cross-check the Profile, Description, and Account information meticulously against the Passport.
        - Historical occupation details may legitimately differ from current data—this alone does not imply inconsistency.
        - Always verify currency consistency when evaluating monetary amounts.
        - Be extremely cautious—reject immediately if there's any uncertainty or if any detail appears suspicious.
        - NEVER fabricate or assume information; rely strictly on provided data.

        RESPOND STRICTLY IN THE FOLLOWING JSON FORMAT:
        {format_instructions}

        ---

        **Passport Document:**
        {passport}

        **Profile Document:**
        {profile}

        **Description Document:**
        {description}

        **Account Document:**
        {account}
        """
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
