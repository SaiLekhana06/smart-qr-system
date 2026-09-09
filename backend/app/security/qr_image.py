import json
import qrcode
from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parents[3] / "generated_qr"
OUTPUT_DIR.mkdir(exist_ok=True)

def generate_qr_image(product_id: int, token: str, signature: str, qr_id: int) -> str:
    payload = {
        "product_id": product_id,
        "token": token,
        "sig": signature
    }
    data = json.dumps(payload)

    img = qrcode.make(data)

    filename = f"qr_{qr_id}.png"
    filepath = OUTPUT_DIR / filename
    img.save(filepath)

    return str(filepath)