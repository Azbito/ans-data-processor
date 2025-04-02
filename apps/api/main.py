from fastapi import FastAPI
from contextlib import asynccontextmanager

from middleware import add_cors_middleware
from routes import pdf, csv, operator, accounting, analytics
from repositories.operator import OperatorRepository
from repositories.accounting import AccountingRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    OperatorRepository.create_table()
    AccountingRepository.create_table()
    yield


app = FastAPI(lifespan=lifespan)

add_cors_middleware(app)

app.include_router(pdf.router)
app.include_router(csv.router)
app.include_router(operator.router)
app.include_router(accounting.router)
app.include_router(analytics.router)


@app.get("/ping")
def read_root():
    return {"message": "pong"}
