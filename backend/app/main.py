from fastapi import FastAPI
from app.database.db import engine, Base
from app.models import product

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Smart QR System backend is running"}