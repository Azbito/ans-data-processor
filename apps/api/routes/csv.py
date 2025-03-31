from fastapi import APIRouter
from controllers.csv import CSVController

router = APIRouter()
csv_controller = CSVController()

@router.get("/csv/extract-tables")
async def extract_tables(target_file: str):
    return csv_controller.extract_tables(target_file)

@router.get("/csv/download-table")
async def download_tables():
    return csv_controller.download_unzipped_table()