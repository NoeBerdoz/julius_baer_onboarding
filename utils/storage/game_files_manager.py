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


def _get_previous_round_folder(current_round: int, session_id: str) -> str | None:
    """
    Finds the directory path for the previous round by searching within the session directory
    for a folder starting with the previous round's padded number.
    """
    # TODO fix this technical debt, I'm so sorry for this, just rushing

    previous_round_num = current_round - 1
    if previous_round_num < 0:
        logging.warning(f"[+] Cannot get previous folder for round 0 (current_round was {current_round}).")
        return None

    session_dir = os.path.join(GAME_FILES_DIR, str(session_id))

    # Calculate the prefix to search for (e.g., "000008_decision_")
    prev_padded = str(previous_round_num).zfill(FOLDER_ROUND_PADDING)
    # Match the start of the folder name format we established
    prefix_to_find = f"{prev_padded}_decision_"

    found_folder = None

    # List contents of the session directory
    for item_name in os.listdir(session_dir):
        item_path = os.path.join(session_dir, item_name)
        # Check if it's a directory and starts with the correct prefix
        if os.path.isdir(item_path) and item_name.startswith(prefix_to_find):
            found_folder = item_path
            # We assume only one match is possible, we can break here
            logging.info(f"Found previous round folder: {found_folder}")
            break

    return found_folder


def store_decoded_files(response: Dict[str, Any] | None, directory: str):
    """
        Decodes and saves base64 encoded files from response into the specified round directory.
    """
    file_map = {
        "passport": ".png",
        "profile": ".docx",
        "description": ".txt",
        "account": ".pdf"
    }

    logging.info(f"[+] Storing failed game round data with decoded files in: {directory}")

    client_data = response["client_data"]

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
        # The response client_data is not present on gameover, in this case we decode the files for further investigation
        if status in ["gameover", "complete"]:
            logging.info(f"[+] Game status is '{status}'. Attempting to save decoded files.")
            previous_round_folder = _get_previous_round_folder(round_number, session_id)
            if previous_round_folder:
                previous_round_num = round_number - 1
                prev_padded = str(previous_round_num).zfill(FOLDER_ROUND_PADDING)
                previous_json_filename = f"{prev_padded}_response.json"  # Use previous round number in filename
                previous_json_path = os.path.join(previous_round_folder, previous_json_filename)
                with open(previous_json_path, 'r') as f:
                    prev_response_data = json.load(f)
                store_decoded_files(prev_response_data, previous_round_folder)
                previous_folder_path_instance = Path(previous_round_folder)
                parts = previous_folder_path_instance.name.rsplit("_", maxsplit=1)
                gameover_folder_name = f"{parts[0]}_gameover"
                new_gameover_path = previous_folder_path_instance.parent / gameover_folder_name
                previous_folder_path_instance.rename(new_gameover_path)
                logging.info(f"[+] Renamed gameover folder: {new_gameover_path}")
        else:
            padded_round = str(round_number).zfill(FOLDER_ROUND_PADDING)
            round_folder_name = f"{padded_round}_decision_{decision.lower()}_{status}"

            # Construct the directory path: base_dir / session_id / decision_XXXXXX
            round_dir = os.path.join(GAME_FILES_DIR, str(session_id), round_folder_name)
            os.makedirs(round_dir, exist_ok=True)  # Create the directory structure if it doesn't exist

            json_file_path = os.path.join(round_dir, f"{padded_round}_response.json")

            with open(json_file_path, "w") as json_file:
                json_file.write(response.model_dump_json())

            logging.info(f"[+] Successfully saved API response JSON to: {json_file_path}")
            store_decoded_files(response.model_dump(mode="json"), round_dir)


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
