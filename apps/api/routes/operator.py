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

@router.get("/operators/{registro_ans}")
async def get_operator(registro_ans: int):
    return operator_controller.get_operator(registro_ans)

@router.post("/operators/import")
async def import_operators(file: UploadFile):
    return await operator_controller.import_operators(file)
