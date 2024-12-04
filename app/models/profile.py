from pydantic import BaseModel, Field
from typing import Optional

class CreateProfileModel(BaseModel):
    img: str
    description: Optional[str] = None
    age: int = Field(..., gt=0)  # La edad debe ser mayor a 0
    gender: str = Field(..., pattern="^(male|female)$")
    target_gender: str = Field(..., pattern="^(male|female)$")
    zodiac_symbol: str = Field(..., pattern="^(aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|capricorn|aquarius|pisces)$")
    imgs: list[str]

class GetProfileModel(BaseModel):
    id: int
    img: str
    description: Optional[str]
    age: int
    gender: str
    target_gender: str
    zodiac_symbol: str
    imgs: list[str]
