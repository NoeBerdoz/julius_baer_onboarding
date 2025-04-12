import os
import logging
import config
import json

from dto.responses import GameStartResponseDTO, GameDecisionResponseDTO

GAME_FILES_DIR = config.GAME_FILES_DIR

# Define padding for round numbers (e.g., 6 digits for up to 999,999 rounds)
FOLDER_ROUND_PADDING = 6

def store_game_round_data(response: GameStartResponseDTO | GameDecisionResponseDTO, round_number: int, session_id: str):
    """
        Logs structured response data and saves associated client files.
    """
    logging.info(f"[+] Storing game round data in {GAME_FILES_DIR}")

    try:
        padded_round = str(round_number).zfill(FOLDER_ROUND_PADDING)
        round_folder_name = f"{padded_round}_decision"

        # Construct the directory path: base_dir / session_id / decision_XXXXXX
        round_dir = os.path.join(GAME_FILES_DIR, str(session_id), round_folder_name)
        os.makedirs(round_dir, exist_ok=True) # Create the directory structure if it doesn't exist

        json_file_path = os.path.join(round_dir, f"{padded_round}_response.json")

        with open(json_file_path, "w") as json_file:
            json.dump(response.model_dump_json(), json_file)

        logging.info(f"[+] Successfully saved API response JSON to: {json_file_path}")
    except Exception as e:
        logging.error(f"[!] Failed to save API response JSON: {e}")

