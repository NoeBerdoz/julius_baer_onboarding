from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field


# Step 1: Define the structured output
class CountryAnswer(BaseModel):
    answer: str = Field(..., description="La réponse à la question")
    country: str = Field(..., description="Le pays concerné")

# Step 2: Create the output parser
parser = PydanticOutputParser(pydantic_object=CountryAnswer)

# Step 3: Create the prompt
prompt = ChatPromptTemplate.from_template(
    "Tu es un assistant utile. Réponds à la question : {question}\n"
    "Réponds uniquement en JSON avec ce format :\n{format_instructions}"
)

# Step 4: LLM configuration
llm = ChatGroq(model_name="llama3-70b-8192", temperature=0.7)

# Step 5: Combine everything
chain: Runnable = prompt | llm | parser

# Step 6: Run the chain
response = chain.invoke({
    "question": "Quelle est la capitale de la Suisse ?",
    "format_instructions": parser.get_format_instructions()
})

# Result
print(response)