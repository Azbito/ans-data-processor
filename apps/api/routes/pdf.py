from fastapi import APIRouter
from controllers.PDFController import PDFController

router = APIRouter()
pdf_controller = PDFController()

router.get("/pdf/ans")(pdf_controller.ans_pdf_scrapper)
router.get("/pdf/embed_ans_pdf")(pdf_controller.get_ans_pdf)
