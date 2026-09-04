import os
import hmac
import hashlib
import secrets
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=env_path)

SECRET_KEY = os.getenv("HMAC_SECRET_KEY")

def generate_unique_token() -> str:
    return secrets.token_urlsafe(32)

def sign_payload(product_id: int, unique_token: str) -> str:
    message = f"{product_id}:{unique_token}"
    signature = hmac.new(
        key=SECRET_KEY.encode(),
        msg=message.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
    return signature

def verify_signature(product_id: int, unique_token: str, signature: str) -> bool:
    expected = sign_payload(product_id, unique_token)
    return hmac.compare_digest(expected, signature)