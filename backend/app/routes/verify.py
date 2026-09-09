from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database.db import get_db
from app.models.qr_code import QRCode
from app.models.verification_log import VerificationLog
from app.schemas.verify import VerifyRequest, VerifyResponse
from app.security.qr_security import verify_signature

router = APIRouter(prefix="/qr", tags=["qr"])

DUPLICATE_SCAN_THRESHOLD = 3
DUPLICATE_TIME_WINDOW_MINUTES = 10

@router.post("/verify", response_model=VerifyResponse)
def verify_qr(request: VerifyRequest, http_request: Request, db: Session = Depends(get_db)):
    client_ip = http_request.client.host

    is_valid_signature = verify_signature(request.product_id, request.token, request.sig)

    if not is_valid_signature:
        log = VerificationLog(qr_id=None, result="tampered", ip_address=client_ip)
        db.add(log)
        db.commit()
        return VerifyResponse(result="tampered", message="Signature does not match — data was altered")

    qr_record = db.query(QRCode).filter(QRCode.unique_token == request.token).first()

    if not qr_record:
        log = VerificationLog(qr_id=None, result="invalid", ip_address=client_ip)
        db.add(log)
        db.commit()
        return VerifyResponse(result="invalid", message="This QR code was never issued")

    window_start = datetime.utcnow() - timedelta(minutes=DUPLICATE_TIME_WINDOW_MINUTES)
    recent_logs = db.query(VerificationLog).filter(
        VerificationLog.qr_id == qr_record.id,
        VerificationLog.result.in_(["genuine", "possible_duplicate"]),
        VerificationLog.scanned_at >= window_start
    ).all()

    distinct_ips = set(log.ip_address for log in recent_logs if log.ip_address)
    distinct_ips.add(client_ip)

    if len(recent_logs) + 1 > DUPLICATE_SCAN_THRESHOLD or len(distinct_ips) > 1:
        log = VerificationLog(qr_id=qr_record.id, result="possible_duplicate", ip_address=client_ip)
        db.add(log)
        db.commit()
        return VerifyResponse(
            result="possible_duplicate",
            message="This QR has been verified an unusual number of times or from multiple sources recently — please review"
        )

    log = VerificationLog(qr_id=qr_record.id, result="genuine", ip_address=client_ip)
    db.add(log)
    db.commit()
    return VerifyResponse(result="genuine", message="QR code verified successfully")