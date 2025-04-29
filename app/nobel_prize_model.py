from pydantic import BaseModel, Field
from typing import List, Optional, Annotated


class Laureate(BaseModel):
    firstname: str
    surname: str
    motivation: Optional[str] = ""


class Prize(BaseModel):
    year: Annotated[
        str,
        Field(pattern=r"^\d{4}$", description="Year must be in YYYY format")
    ]  # only 4 digits are allowed on entry
    category: str
    laureates: List[Laureate]
