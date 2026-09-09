import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from fastapi.testclient import TestClient
from app.main import app
from app.security.qr_security import sign_payload

client = TestClient(app)

def test_genuine_qr_verified():
    response = client.post("/qr/generate", json={"product_id": 1})
    assert response.status_code == 200
    qr_data = response.json()

    import json
    from app.security.qr_image import OUTPUT_DIR
    qr_file = OUTPUT_DIR / f"qr_{qr_data['id']}.png"
    assert qr_file.exists()

    verify_response = client.post("/qr/verify", json={
        "product_id": qr_data["product_id"],
        "token": qr_data["unique_token"],
        "sig": qr_data["signature"]
    })
    assert verify_response.status_code == 200
    assert verify_response.json()["result"] == "genuine"

def test_tampered_product_id_detected():
    response = client.post("/qr/generate", json={"product_id": 1})
    qr_data = response.json()

    verify_response = client.post("/qr/verify", json={
        "product_id": 999,
        "token": qr_data["unique_token"],
        "sig": qr_data["signature"]
    })
    assert verify_response.json()["result"] == "tampered"

def test_tampered_signature_detected():
    response = client.post("/qr/generate", json={"product_id": 1})
    qr_data = response.json()

    verify_response = client.post("/qr/verify", json={
        "product_id": qr_data["product_id"],
        "token": qr_data["unique_token"],
        "sig": "0000000000000000000000000000000000000000000000000000000000000000"
    })
    assert verify_response.json()["result"] == "tampered"

def test_never_issued_token_is_invalid():
    fake_token = "definitely_never_issued_abc"
    fake_sig = sign_payload(1, fake_token)

    verify_response = client.post("/qr/verify", json={
        "product_id": 1,
        "token": fake_token,
        "sig": fake_sig
    })
    assert verify_response.json()["result"] == "invalid"

def test_nonexistent_product_qr_generation_fails():
    response = client.post("/qr/generate", json={"product_id": 999999})
    assert response.status_code == 404