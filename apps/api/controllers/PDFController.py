from fastapi.responses import JSONResponse
from services.pdf import PDFService
from services.r2 import R2Service
from services.zip import ZIPService
from services.csv import CSVService
from fastapi import HTTPException


class ANSPDFController:
    def __init__(self):
        self.r2_service = R2Service()
        self.zip_service = ZIPService()
        self.csv_service = CSVService()
        self.pdf_service = PDFService(
            self.r2_service, self.zip_service, self.csv_service
        )

    def ans_pdf_scrapper(self, target_url: str) -> JSONResponse:
        try:
            res = self.pdf_service.process_pdf(target_url)

            if not res:
                return JSONResponse(
                    status_code=404,
                    content={"detail": "No data found for the provided URL."},
                )

            r2_download_url = self.r2_service.get_file("pdfs/asn.zip")

            return JSONResponse(status_code=200, content={"url": r2_download_url})

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ANS PDF Scrapper: {str(e)}")

    def extract_tables(self, target_file: str, extension: str) -> JSONResponse:
        try:
            data = self.pdf_service.extract_tables(target_file, extension)

            return JSONResponse(status_code=200, content={"url": data})

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error while extracting tables: {str(e)}"
            )
