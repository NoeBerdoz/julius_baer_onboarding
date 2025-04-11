import zipfile
import requests
import base64
from PIL import Image
import pytesseract
import io
import re
from pathlib import Path

# === Configuration API ===
api_url = "https://hackathon-api.mlo.sehlat.io/game/start"
api_key = "OwogAztgWRdPfT2wWe7Xevdw98tdJelatlk82K6bozw"
team_name = "Welch"

# === Requête API ===
headers = {
    "x-api-key": api_key,
    "Content-Type": "application/json"
}
payload = {
    "player_name": team_name
}

response = requests.post(api_url, headers=headers, json=payload)
response_data = response.json()

# === Traitement du passeport ===
passport_b64 = response_data["client_data"]["passport"]
image_bytes = base64.b64decode(passport_b64)
image = Image.open(io.BytesIO(image_bytes))
extracted_text = pytesseract.image_to_string(image, lang='eng')

print("=== Texte extrait depuis le passeport ===\n")
print(extracted_text)

# === Traitement du profil ===
profile_b64 = response_data["client_data"]["profile"]
profile_bytes = base64.b64decode(profile_b64)
zip_file = zipfile.ZipFile(io.BytesIO(profile_bytes))

# Vérifie la présence du fichier principal du Word
document_path = "word/document.xml"
if document_path in zip_file.namelist():
    with zip_file.open(document_path) as doc_file:
        xml_content = doc_file.read().decode("utf-8", errors="ignore")

    # Extraction naïve du texte (on peut améliorer avec XML parser si besoin)
    text_only = re.sub(r"<[^>]+>", "", xml_content)

    print("\n=== Texte extrait depuis le profil (document Word) ===\n")
    print(text_only.strip())
else:
    print("Le fichier 'word/document.xml' est introuvable dans l'archive du profil.")