from typing import Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int
    name: str = Field(..., min_length=3)
    price: float = Field(..., gt=0)


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=3)
    price: float


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
