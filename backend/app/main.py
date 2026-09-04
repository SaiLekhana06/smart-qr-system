from fastapi import FastAPI
from app.database.db import engine, Base
from app.models import product
from app.routes import product as product_routes

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product_routes.router)

@app.get("/")
def read_root():
    return {"message": "Smart QR System backend is running"}