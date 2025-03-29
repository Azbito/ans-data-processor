from services.pdf import PDFService
from services.r2 import R2Service
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

r2_service = R2Service()
pdf_service = PDFService(r2_service)


@router.get("/ans-pdf")
def ans_pdf_scrapper(target_url: str):
    try:
        res = pdf_service.process_pdf(target_url)

        if not res:
            return JSONResponse(
                status_code=404,
                content={"detail": "No data found for the provided URL."},
            )

        r2_download_url = r2_service.get_file("pdfs/asn.zip")

        return JSONResponse(status_code=200, content={"url": r2_download_url})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ANS PDF Scrapper: {str(e)}")
