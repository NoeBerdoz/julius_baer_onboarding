import base64
import binascii
from typing import Callable, Type
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI


def run_extraction_chain(
    *,
    raw_file_data: str,
    file_processor: Callable[[str], str],
    pydantic_model: Type,
    prompt_template: str,
    model_name: str = "gemini-2.0-flash"
):
    """
    Traite un fichier encodé en base64, applique un parser OCR, génère un prompt, envoie à un modèle LLM, et retourne le résultat parsé.

    Args:
        raw_file_data (str): Données base64 du fichier à traiter.
        file_processor (Callable): Fonction qui transforme les données en texte brut.
        pydantic_model (Type): Classe Pydantic pour le parsing du résultat.
        prompt_template (str): Prompt à envoyer au LLM avec {format_instructions} et {processed_text}.
        model_name (str): Nom du modèle LLM à utiliser.

    Returns:
        Instance du modèle Pydantic parsé avec les résultats du LLM.
    """
    try:
        base64.b64decode(raw_file_data, validate=True)
    except binascii.Error as e:
        raise ValueError(f"Invalid base64 data: {e}")

    processed_text = file_processor(raw_file_data)

    parser = PydanticOutputParser(pydantic_object=pydantic_model)
    format_instructions = parser.get_format_instructions()

    prompt = ChatPromptTemplate.from_template(prompt_template)

    chain: Runnable = prompt | ChatGoogleGenerativeAI(model=model_name) | parser

    result = chain.invoke({
        "processed_text": processed_text,
        "format_instructions": format_instructions,
    })

    return result