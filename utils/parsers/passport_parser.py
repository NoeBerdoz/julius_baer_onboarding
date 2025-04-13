import os
from mistralai import Mistral

api_key = "XEOc110BYE4PMj8FQBauxxGZTitRTs2w"
client = Mistral(api_key=api_key)


def process_passport(passport_b64: str) -> str:
    mistral_image_url = f"data:image/png;base64,{passport_b64}"

    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "image_url",
            "image_url": mistral_image_url
        }
    )

    # Extraire le markdown de toutes les pages
    markdown_text = "\n\n".join(page.markdown for page in ocr_response.pages)

    return markdown_text  # Tu peux aussi retourner juste le chemin si tu préfères