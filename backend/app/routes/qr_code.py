from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.product import Product
from app.models.qr_code import QRCode
from app.schemas.qr_code import QRGenerateRequest, QRCodeOut
from app.security.qr_security import generate_unique_token, sign_payload
from app.security.qr_image import generate_qr_image
router = APIRouter(prefix="/qr", tags=["qr"])

@router.post("/generate", response_model=QRCodeOut)
def generate_qr(request: QRGenerateRequest, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    token = generate_unique_token()
    signature = sign_payload(product.id, token)

    new_qr = QRCode(
        product_id=product.id,
        unique_token=token,
        signature=signature,
        status="active"
    )
    db.add(new_qr)
    db.commit()
    db.refresh(new_qr)

    generate_qr_image(product.id, token, signature, new_qr.id)

    return new_qr