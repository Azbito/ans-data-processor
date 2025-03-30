from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import pdf, csv, operator, accounting, analytics
from repositories.operator import OperatorRepository
from repositories.accounting import AccountingRepository

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")

async def startup_event():
    OperatorRepository.create_table()
    AccountingRepository.create_table()

app.include_router(pdf.router)
app.include_router(csv.router)
app.include_router(operator.router)
app.include_router(accounting.router)
app.include_router(analytics.router)

@app.get("/ping")
def read_root():
    return {"message": "pong"}
