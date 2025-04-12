import base64
import pymupdf

def process_account(account_b64: str) -> str:
    """
    Traite l'account :
    - Décodage du PDF encodé en base64.
    - Extraction du texte et des champs de formulaire directement depuis le PDF.

    :param account_b64: Chaîne base64 représentant le PDF.
    :return: Texte extrait de chaque page du PDF, incluant les champs du formulaire.
    """
    # Décodage du PDF en base64
    pdf_bytes = base64.b64decode(account_b64)

    # Ouverture du PDF avec PyMuPDF
    pdf_document = pymupdf.open(stream=pdf_bytes, filetype="pdf")

    # Traitement de chaque page
    for i in range(len(pdf_document)):
        page = pdf_document[i]

        # Extraction des champs de formulaire
        fields = page.widgets()
        form_fields_text = []

        for field in fields:
            field_name = field.field_name
            field_value = field.field_value
            form_fields_text.append(f"Field: {field_name}, Value: {field_value}")

        combined_text = ""

        if form_fields_text:
            combined_text += "\n\nForm Fields:\n" + "\n".join(form_fields_text)

    pdf_document.close()
    return "\n".join(combined_text)