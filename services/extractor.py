import base64
import binascii
from typing import Callable, Type, Any, TypeVar
from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai.chat_models import ChatOpenAI
from pydantic import BaseModel

from utils.parsers import process_profile, process_passport, process_account, process_description
from validation.from_account import FromAccount
from validation.from_passport import FromPassport
from validation.from_profile import FromProfile
from validation.from_description import FromDescription

def extract_description(client_data: dict[str, Any]) -> FromDescription:
    passport_data = client_data.get("description")

    prompt_template = (
        "Extract the following information from the provided passport text.\n"
        "Return only JSON matching this format:\n{format_instructions}\n\n"
        "Pay special attention to the passport number\n"
        "Passport text:\n{processed_text}"
    )


    result = __run_extraction_chain(
        raw_file_data=passport_data,
        file_processor=process_description,
        pydantic_model=FromDescription,
        prompt_template=prompt_template,
    )

    return result

def extract_account(client_data: dict[str, Any])-> FromAccount:
    account_data = client_data.get("account")

    prompt_template = (
        "Extract the following information from the provided text.\n"
        "Return only JSON matching this format:\n{format_instructions}\n\n"
        "Trim email if needed\n"
        "Passport text:\n{processed_text}"
    )

    result = __run_extraction_chain(
        raw_file_data=account_data,
        file_processor=process_account,
        pydantic_model=FromAccount,
        prompt_template=prompt_template,
    )

    return result


def extract_passport(client_data: dict[str, Any]) -> FromPassport:
    passport_data = client_data.get("passport")

    prompt_template = (
        "Extract the following information from the provided passport text.\n"
        "Return only JSON matching this format:\n{format_instructions}\n\n"
        "Pay special attention to the passport number\n"
        "Passport text:\n{processed_text}"
    )

    result = __run_extraction_chain(
        raw_file_data=passport_data,
        file_processor=process_passport,
        pydantic_model=FromPassport,
        prompt_template=prompt_template,
    )

    return result


def extract_profile(client_data: dict[str, Any]) -> FromProfile:
    profile_data = client_data.get("profile")

    prompt_template = (
        "Extract the following information from the provided text.\n"
        "Return only JSON matching this format:\n{format_instructions}\n\n"
        "Pay special attention to the passport number and signature.\n"
        "Passport text:\n{processed_text}"
    )

    result = __run_extraction_chain(
        raw_file_data=profile_data,
        file_processor=process_profile,
        pydantic_model=FromProfile,
        prompt_template=prompt_template,
    )

    return result

ModelType = TypeVar("ModelType", bound=BaseModel)
def __run_extraction_chain(
    *,
    raw_file_data: str,
    file_processor: Callable[[str], str],
    pydantic_model: type[ModelType],
    prompt_template: str,
    model_name: str = "gemini-2.0-flash"
) -> ModelType:
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

    chain: Runnable = prompt | ChatOpenAI(model="gpt-4o") | parser

    result = chain.invoke({
        "processed_text": processed_text,
        "format_instructions": format_instructions,
    })

    return result