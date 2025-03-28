from services.pdf import PDFService
from services.r2 import R2Service
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

router = APIRouter()

r2_service = R2Service()

pdf_service = PDFService(r2_service)


@router.get("/ans-pdf")
def ans_pdf_scrapper(target_url: str):
    try:
        zip_buffer = pdf_service.process_pdf(target_url)

        return StreamingResponse(
            zip_buffer,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=attachments.zip"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar o PDF: {str(e)}"
        )
