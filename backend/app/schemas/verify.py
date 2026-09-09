from pydantic import BaseModel

class VerifyRequest(BaseModel):
    product_id: int
    token: str
    sig: str

class VerifyResponse(BaseModel):
    result: str
    message: str