import base64
import io
from PIL import Image
from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from validation.from_passport import FromPassport

def process_passport(passport_b64: str) -> str:
    """
    Traite le passport :
    - Décodage de l'image en base64.
    - Envoi à GPT-4o avec un prompt d'extraction structuré.
    - Parsing structuré avec un modèle Pydantic.
    """
    image_bytes = base64.b64decode(passport_b64)
    image = Image.open(io.BytesIO(image_bytes))

    # Parser structuré basé sur le modèle FromPassport
    parser = PydanticOutputParser(pydantic_object=FromPassport)

    # Prompt + Instructions pour extraction
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un assistant d'extraction de données de passeport."),
        ("human", "Voici l'image d'un passeport. Extrais les informations dans ce format :\n\n{format_instructions}"),
    ])

    # LLM avec vision (GPT-4o)
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    chain = prompt | llm.with_structured_output(parser=parser)

    # Appel du LLM avec l'image en contexte
    result = chain.invoke({
        "format_instructions": parser.get_format_instructions(),
        "image": image,
    })

    return result.json()