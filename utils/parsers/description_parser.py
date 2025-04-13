import base64
import re
from typing import Dict

def process_description(desc_b64: str) -> Dict[str, str]:
    """
    Décode une chaîne Base64, puis découpe le texte en sections à partir des titres suivis de ':'.

    :param desc_b64: Donnée encodée en base64 représentant un fichier .txt
    :return: Dictionnaire avec titres comme clés et contenu comme valeurs
    """
    try:
        # Décodage
        decoded_bytes = base64.b64decode(desc_b64)
        decoded_text = decoded_bytes.decode('utf-8')

        # Expression régulière pour matcher les titres suivis de ':'
        pattern = r'(?P<title>[\w\s]+):\s*'

        # Split tout en gardant les titres
        parts = re.split(pattern, decoded_text)

        # Le premier élément de `parts` est ce qui précède le 1er titre (souvent vide)
        chunks = {}
        for i in range(1, len(parts), 2):
            title = parts[i].strip()
            content = parts[i+1].strip() if (i + 1) < len(parts) else ""
            chunks[title] = content

        return chunks
    except Exception as e:
        return {"Erreur": f"[Erreur de décodage ou de parsing] {str(e)}"}