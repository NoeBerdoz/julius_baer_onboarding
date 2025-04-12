import base64
import io
from tempfile import NamedTemporaryFile
from PIL import Image
import pytesseract
from passporteye import read_mrz
import json

def process_passport(passport_b64: str) -> str:
    """
    Traite le passport :
    - Décodage de l'image en base64.
    - Application de l'OCR pour extraire le texte.

    :param passport_b64: Chaîne base64 représentant l'image du passport.
    :return: Texte extrait de l'image.
    """
    image_bytes = base64.b64decode(passport_b64)
    # image = Image.open(io.BytesIO(image_bytes))
    # text = pytesseract.image_to_string(image, lang='eng')
    with NamedTemporaryFile(mode="wb") as tmp_img:
        tmp_img.write(image_bytes)
        with open(tmp_img.name, "rb") as read_img:
            text = read_mrz(read_img)
    # text = json.dumps(text)
    # TODO CONTINUE
    return text