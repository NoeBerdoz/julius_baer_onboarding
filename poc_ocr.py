import requests
import base64
from PIL import Image
import pytesseract
import io
from pathlib import Path

# Définir les informations de l'API (à personnaliser)
api_url = "https://hackathon-api.mlo.sehlat.io/game/start"
api_key = "OwogAztgWRdPfT2wWe7Xevdw98tdJelatlk82K6bozw"
team_name = "Welch"

# Requête POST pour obtenir les données du jeu
headers = {
    "x-api-key": api_key,
    "Content-Type": "application/json"
}
payload = {
    "player_name": team_name
}

# Simulation de la requête (à activer quand tu veux l’exécuter pour de vrai)
response = requests.post(api_url, headers=headers, json=payload)
response_data = response.json()
print(response_data["client_data"]["passport"])


# === Extraction du champ "passport" depuis ta réponse API ===
passport_b64 = response_data["client_data"]["passport"]

# === Décodage de l’image (Base64 → image binaire) ===
image_bytes = base64.b64decode(passport_b64)
image = Image.open(io.BytesIO(image_bytes))

# === OCR avec pytesseract ===
# (Tu peux changer 'eng' par 'fra', 'deu', etc. selon la langue du passeport)
extracted_text = pytesseract.image_to_string(image, lang='eng')

# === Affichage du résultat ===
print("Texte extrait depuis le passeport :\n")
print(extracted_text)