import base64
import os
import logging
import config
import json
from typing import Dict, Any
import csv
from pathlib import Path

from dto.responses import GameStartResponseDTO, GameDecisionResponseDTO

GAME_FILES_DIR = config.GAME_FILES_DIR

# Define padding for round numbers (e.g., 6 digits for up to 999,999 rounds)
FOLDER_ROUND_PADDING = 6


def store_decoded_files(client_data: Dict[str, Any] | None, directory: str):
    """
        Decodes and saves base64 encoded files from client_data into the specified round directory.
    """
    file_map = {
        "passport": ".png",
        "profile": ".docx",
        "description": ".txt",
        "account": ".pdf"
    }

    logging.info(f"[+] Storing failed game round data with decoded files in: {directory}")

    for key, extension in file_map.items():
        if key in client_data:
            base64_string = client_data[key]
            if isinstance(base64_string, str):
                file_path = os.path.join(directory, f"{key}{extension}")
                try:
                    decoded_bytes = base64.b64decode(base64_string)

                    with open(file_path, "wb") as file:
                        file.write(decoded_bytes)
                        logging.info(f"[+] Successfully stored game decoded file: {file_path}")

                except base64.binascii.Error as b64e:
                    logging.error(f"[!] Failed to decode base64 for key '{key}' in {directory}: {b64e}")
                except IOError as ioe:
                    logging.error(f"[!] Failed to write file {file_path}: {ioe}")
                except Exception as e:
                    logging.error(f"[!] Unexpected error saving file '{key}{extension}' in {directory}: {e}")


def store_game_round_data(decision: str, response: GameStartResponseDTO | GameDecisionResponseDTO, round_number: int,
                          session_id: str, status: str):
    """
        Logs structured response data and saves associated client files.
    """
    logging.info(f"[+] Storing game round data in {GAME_FILES_DIR}")

    try:
        padded_round = str(round_number).zfill(FOLDER_ROUND_PADDING)
        round_folder_name = f"{padded_round}_decision_{decision.lower()}_{status}"

        # Construct the directory path: base_dir / session_id / decision_XXXXXX
        round_dir = os.path.join(GAME_FILES_DIR, str(session_id), round_folder_name)
        os.makedirs(round_dir, exist_ok=True)  # Create the directory structure if it doesn't exist

        json_file_path = os.path.join(round_dir, f"{padded_round}_response.json")

        with open(json_file_path, "w") as json_file:
            json.dump(response.model_dump_json(), json_file)

        if status in ["gameover", "complete"]:
            logging.info(f"[+] Game status is '{status}'. Attempting to save decoded files.")
            store_decoded_files(response.client_data, round_dir)


        logging.info(f"[+] Successfully saved API response JSON to: {json_file_path}")
    except Exception as e:
        logging.error(f"[!] Failed to save API response JSON: {e}")


def store_decision(client_id: str, decision: str):
    path = Path('./resources/decision_log2.csv')  # TODO clean me!!

    path.parent.mkdir(parents=True, exist_ok=True)  # create dirs if needed

    exists = path.exists()
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(['client_id', 'decision'])  # header
        writer.writerow([client_id, decision])
