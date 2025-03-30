from fastapi import APIRouter
from controllers.csv import CSVController

router = APIRouter()
csv_controller = CSVController()

@router.get("/csv/extract-tables")
async def extract_tables(target_file: str, extension: str):
    return csv_controller.extract_tables(target_file, extension)

@router.get("/csv/download-tables")
async def download_tables(target_file: str, extension: str):
    return csv_controller.extract_and_download_tables(target_file, extension)