from fastapi import FastAPI
from routes import pdf, csv

app = FastAPI()

app.include_router(pdf.router)
app.include_router(csv.router)


@app.get("/ping")
def read_root():
    return {"message": "ping"}
