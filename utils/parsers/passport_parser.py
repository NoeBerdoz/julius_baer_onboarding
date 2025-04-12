import base64
import io
from PIL import Image
import pytesseract


def process_passport(passport_b64: str) -> str:
    """
    Traite le passport :
    - Décodage de l'image en base64.
    - Application de l'OCR pour extraire le texte.

    :param passport_b64: Chaîne base64 représentant l'image du passport.
    :return: Texte extrait de l'image.
    """
    image_bytes = base64.b64decode(passport_b64)
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image, lang='eng')
    return text