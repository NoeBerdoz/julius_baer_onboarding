import base64

def process_description(desc_b64: str) -> str:
    """
            Décode une chaîne base64 et retourne le texte UTF-8 correspondant.

            :param base64_text: Donnée encodée en base64.
            :return: Chaîne de caractères décodée.
            """
    try:
        decoded_bytes = base64.b64decode(desc_b64)
        decoded_text = decoded_bytes.decode('utf-8')
        return decoded_text
    except Exception as e:
        return f"[Erreur de décodage] {str(e)}"