from fastapi import APIRouter, UploadFile, Query
from controllers.accounting import AccountingController
from typing import Optional

router = APIRouter()
accounting_controller = AccountingController()

@router.get("/accounting")
async def get_all_accounting(
    limit: int = Query(50, ge=1, le=1000, description="Number of items to return"),
    cursor: Optional[str] = Query(None, description="Cursor for pagination")
):
    return accounting_controller.get_all_accounting(limit, cursor)

@router.get("/accounting/{reg_ans}")
async def get_operator_accounting(reg_ans: int):
    return accounting_controller.get_accounting(reg_ans)

@router.post("/accounting/import")
async def import_accounting(file: UploadFile):
    return await accounting_controller.import_accounting(file)
