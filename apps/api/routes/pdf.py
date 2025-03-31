from fastapi import APIRouter
from controllers.pdf import PDFController

router = APIRouter()
pdf_controller = PDFController()

@router.get("/pdf/ans")
async def ans_pdf_scrapper(target_url: str):
    return pdf_controller.ans_pdf_scrapper(target_url)

@router.get("/pdf/scrap")
async def get_ans_pdf(target_url: str, target_file: str):
    return pdf_controller.get_ans_pdf(target_url, target_file)
