from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.qr_code import QRCode
from app.models.verification_log import VerificationLog
from app.schemas.verify import VerifyRequest, VerifyResponse
from app.security.qr_security import verify_signature

router = APIRouter(prefix="/qr", tags=["qr"])

@router.post("/verify", response_model=VerifyResponse)
def verify_qr(request: VerifyRequest, db: Session = Depends(get_db)):
    is_valid_signature = verify_signature(request.product_id, request.token, request.sig)

    if not is_valid_signature:
        log = VerificationLog(qr_id=None, result="tampered")
        db.add(log)
        db.commit()
        return VerifyResponse(result="tampered", message="Signature does not match — data was altered")

    qr_record = db.query(QRCode).filter(QRCode.unique_token == request.token).first()

    if not qr_record:
        log = VerificationLog(qr_id=None, result="invalid")
        db.add(log)
        db.commit()
        return VerifyResponse(result="invalid", message="This QR code was never issued")

    log = VerificationLog(qr_id=qr_record.id, result="genuine")
    db.add(log)
    db.commit()
    return VerifyResponse(result="genuine", message="QR code verified successfully")