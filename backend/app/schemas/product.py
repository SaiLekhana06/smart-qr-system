from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: Optional[str] = None

class ProductOut(BaseModel):
    id: int
    name: str
    sku: str
    description: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True