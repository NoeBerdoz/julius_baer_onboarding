import zipfile
import requests
import base64
from PIL import Image
import pytesseract
import io
import xml.etree.ElementTree as ET
from pathlib import Path

# === Configuration API ===
api_url = "https://hackathon-api.mlo.sehlat.io/game/start"
api_key = "OwogAztgWRdPfT2wWe7Xevdw98tdJelatlk82K6bozw"
team_name = "Welch"

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

# === Traitement du profil DOCX ===
profile_b64 = response_data["client_data"]["profile"]
profile_bytes = base64.b64decode(profile_b64)
zip_file = zipfile.ZipFile(io.BytesIO(profile_bytes))

document_path = "word/document.xml"
styles_path = "word/styles.xml"

# Charger la carte des styles pour retrouver les titres
style_map = {}
if styles_path in zip_file.namelist():
    styles_xml = zip_file.read(styles_path)
    styles_tree = ET.fromstring(styles_xml)

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    for style in styles_tree.findall(".//w:style", ns):
        style_id = style.attrib.get(f"{{{ns['w']}}}styleId")
        name_elem = style.find("w:name", ns)
        if name_elem is not None:
            style_name = name_elem.attrib.get(f"{{{ns['w']}}}val", "")
            style_map[style_id] = style_name

# Parse du document principal
if document_path in zip_file.namelist():
    document_xml = zip_file.read(document_path)
    tree = ET.fromstring(document_xml)

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    print("\n=== Texte structuré extrait depuis le profil ===\n")

    for para in tree.findall(".//w:p", ns):
        texts = [node.text for node in para.findall(".//w:t", ns) if node.text]
        if not texts:
            continue
        full_text = " ".join(texts).strip()

        # Détecter le style (Heading1, Heading2, etc.)
        p_style = para.find(".//w:pStyle", ns)
        if p_style is not None:
            style_id = p_style.attrib.get(f"{{{ns['w']}}}val")
            style_name = style_map.get(style_id, "")
            if "Heading1" in style_name:
                print(f"\n# {full_text}\n")
            elif "Heading2" in style_name:
                print(f"\n## {full_text}\n")
            elif "Heading3" in style_name:
                print(f"\n### {full_text}\n")
            else:
                print(full_text)
        else:
            print(full_text)
else:
    print("Le fichier 'word/document.xml' est introuvable dans le profil.")