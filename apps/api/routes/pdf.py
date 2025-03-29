from fastapi import APIRouter
from controllers.PDFController import ANSPDFController

router = APIRouter()
ans_pdf_controller = ANSPDFController()

router.get("/pdf/ans")(ans_pdf_controller.ans_pdf_scrapper)
router.get("/pdf/extract-tables")(ans_pdf_controller.extract_tables)
