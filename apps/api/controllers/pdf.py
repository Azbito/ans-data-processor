from fastapi.responses import JSONResponse
from services.pdf import PDFService
from services.r2 import R2Service
from services.zip import ZIPService
from services.csv import CSVService
from fastapi import HTTPException
import os
import requests


class PDFController:
    def __init__(self):
        self.r2_service = R2Service()
        self.zip_service = ZIPService()
        self.csv_service = CSVService()
        self.pdf_service = PDFService(
            self.r2_service, self.zip_service, self.csv_service
        )

    def get_ans_pdf(self, target_url: str, target_file: str) -> JSONResponse:
        res = self.pdf_service.process_pdf(target_url)

        if not res:
            return JSONResponse(
                status_code=404,
                content={"detail": "No data found for the provided URL."},
            )

        extract_dir = "/tmp/extracted_pdfs"
        os.makedirs(extract_dir, exist_ok=True)

        zip_url = self.r2_service.get_file("pdfs/ans.zip")

        response = requests.get(zip_url)
        if response.status_code != 200:
            return JSONResponse(
                status_code=500,
                content={
                    "detail": f"Failed to download the zip file: {response.status_code}"
                },
            )

        zip_file_path = os.path.join(extract_dir, "ans.zip")
        with open(zip_file_path, "wb") as f:
            f.write(response.content)

        try:
            extension = (
                os.path.splitext(target_file)[1][1:] if "." in target_file else "pdf"
            )
            file_path = self.zip_service.unzip(
                extract_dir, zip_file_path, target_file.split(".")[0], extension
            )

            with open(file_path, "rb") as file:
                file_content = file.read()

            extracted_file_path = f"pdfs/raw/{target_file}"
            self.r2_service.save_to_r2(file_content, extracted_file_path, extension)

            download_url = self.r2_service.get_file(extracted_file_path)

            return JSONResponse(status_code=200, content={"url": download_url})

        except FileNotFoundError as e:
            return JSONResponse(
                status_code=404,
                content={"detail": str(e)},
            )
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"detail": f"Error extracting file: {str(e)}"},
            )
        finally:
            self.zip_service.cleanup_temp_files(extract_dir, zip_file_path)

    def ans_pdf_scrapper(self, target_url: str) -> JSONResponse:
        try:
            res = self.pdf_service.process_pdf(target_url)

            if not res:
                return JSONResponse(
                    status_code=404,
                    content={"detail": "No data found for the provided URL."},
                )

            r2_download_url = self.r2_service.get_file("pdfs/ans.zip")

            return JSONResponse(status_code=200, content={"url": r2_download_url})

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"ANS PDF Scrapper: {str(e)}")

    def extract_tables(self, target_file: str) -> JSONResponse:
        try:
            data = self.pdf_service.extract_tables(target_file)

            return JSONResponse(status_code=200, content={"url": data})

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error while extracting tables: {str(e)}"
            )
