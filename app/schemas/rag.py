from pydantic import BaseModel, field_validator, Field

class SearchDocsRequest(BaseModel):
    query: str = Field(description="Domanda o argomento da cercare nei documenti tecnici")
    top_k: int = Field(default=3, ge=1, le=10, description="Numero massimo di risultati ottenuti dalla ricerca")


    @field_validator("query")
    @classmethod
    def query_non_vuota(cls, v:str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("query non può essere vuota")
        return v