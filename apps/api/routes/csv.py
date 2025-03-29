from fastapi import APIRouter
from controllers.CSVController import CSVController

router = APIRouter()
csv_controller = CSVController()

router.get("/csv/extract-tables")(csv_controller.extract_tables)
router.get("/csv/download-tables")(csv_controller.extract_and_download_tables)
