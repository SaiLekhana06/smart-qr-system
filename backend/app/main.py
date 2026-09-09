from fastapi import FastAPI

from app.database.db import engine, Base
from app.models import product, qr_code , verification_log
from app.routes import product as product_routes
from app.routes import qr_code as qr_routes
from app.routes import verify as verify_routes

app = FastAPI()


Base.metadata.create_all(bind=engine)


app.include_router(product_routes.router)
app.include_router(qr_routes.router)
app.include_router(verify_routes.router)

@app.get("/")
def read_root():
    return {"message": "Smart QR System backend is running"}