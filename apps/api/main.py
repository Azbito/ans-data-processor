from fastapi import FastAPI
from endpoints import pdf

app = FastAPI()

app.include_router(pdf.router)


@app.get("/ping")
def read_root():
    return {"message": "pong"}
