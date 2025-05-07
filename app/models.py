from typing import Optional

from pydantic import BaseModel, Field


class Item(BaseModel):
    id: int
    name: str
    price: float


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=3, description="Name must have at least 3 characters")
    price: float


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
