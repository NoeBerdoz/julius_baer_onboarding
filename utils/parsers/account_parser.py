import base64
from pdf2image import convert_from_bytes
import pytesseract


def process_account(account_b64: str) -> str:
    """
    Traite l'account :
    - Décodage du PDF encodé en base64.
    - Conversion de chaque page du PDF en image.
    - Application de l'OCR sur chaque image pour extraire le texte.

    :param account_b64: Chaîne base64 représentant le PDF.
    :return: Texte extrait de chaque page du PDF.
    """
    pdf_bytes = base64.b64decode(account_b64)
    images = convert_from_bytes(pdf_bytes)
    pages_text = []
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image, lang="eng")
        pages_text.append(f"--- Page {i + 1} ---\n{text}")
    return "\n".join(pages_text)