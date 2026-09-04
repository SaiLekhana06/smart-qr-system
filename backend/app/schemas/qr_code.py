from pydantic import BaseModel
from datetime import datetime

class QRGenerateRequest(BaseModel):
    product_id: int

class QRCodeOut(BaseModel):
    id: int
    product_id: int
    unique_token: str
    signature: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True