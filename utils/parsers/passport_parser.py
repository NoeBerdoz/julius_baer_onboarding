import base64
import io
from tempfile import NamedTemporaryFile
from PIL import Image, ImageEnhance
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
    with NamedTemporaryFile(mode="wb") as tmp_img:
        tmp_img.write(image_bytes)
        with open(tmp_img.name, "rb") as read_img:
            mrz_obj = read_mrz(read_img)

    image = Image.open(io.BytesIO(image_bytes))
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)  # 2.0 = double le contraste (1.0 = inchangé)
    tesseract_text = pytesseract.image_to_string(image, lang='eng')
    out_dict = {}
    if not mrz_obj is None:
        number_raw = str(mrz_obj.number)
        # It's not called a 'Hack'athon for nothing...
        number = number_raw.replace("B", "8")
        out_dict = {
            "country": mrz_obj.country,
            "names": mrz_obj.names,
            "number": number,
            "surname": mrz_obj.surname,
            "mrz": mrz_obj.aux["text"],
        }
    out_dict["raw"] = tesseract_text
    out = json.dumps(out_dict)
    return out