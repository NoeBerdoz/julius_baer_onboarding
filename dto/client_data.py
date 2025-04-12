from pydantic import BaseModel

class ClientData(BaseModel):
    """
    Model for the client data attributes which need to be validated and compared for correspondence between
    the data sources ()
    """
    name: str

    # TODO CONTINUE