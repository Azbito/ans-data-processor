from fastapi import APIRouter, Query, UploadFile
from typing import Optional
from controllers.operator import OperatorController

router = APIRouter()
operator_controller = OperatorController()

@router.get("/operators")
async def get_all_operators(
    limit: int = Query(50, ge=1, le=1000, description="Number of items to return"),
    cursor: Optional[str] = Query(None, description="Cursor for pagination")
):
    return operator_controller.get_all_operators(limit, cursor)

@router.get("/operators/id/{registro_ans}")
async def get_operator(registro_ans: int):
    return operator_controller.get_operator(registro_ans)

@router.get("/operators/search")
async def search_operators(
    name: Optional[str] = Query(None, description="Search by razao_social or nome_fantasia"),
    city: Optional[str] = Query(None, description="Search by cidade"),
    state: Optional[str] = Query(None, description="Search by UF"),
    modality: Optional[str] = Query(None, description="Search by modalidade")
):
    return await operator_controller.search_operators(name, city, state, modality)

@router.post("/operators/import")
async def import_operators(file: UploadFile):
    return await operator_controller.import_operators(file)
