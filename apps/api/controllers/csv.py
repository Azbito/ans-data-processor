from fastapi.responses import JSONResponse
from services.pdf import PDFService
from services.r2 import R2Service
from services.zip import ZIPService
from services.csv import CSVService
from fastapi import HTTPException
import os


class CSVController:
    def __init__(self):
        self.r2_service = R2Service()
        self.zip_service = ZIPService()
        self.csv_service = CSVService()
        self.pdf_service = PDFService(
            self.r2_service, self.zip_service, self.csv_service
        )

    def extract_tables(self, target_file: str) -> JSONResponse:
        try:
            data = self.pdf_service.extract_tables(target_file)

            return JSONResponse(status_code=200, content={"url": data})

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error while extracting tables: {str(e)}"
            )

    def download_unzipped_table(self) -> JSONResponse:
        try:
            download_url = self.pdf_service.extract_tables(target_file="Anexo_I")

            extracted_file, extract_dir, temp_zip_path = (
                self.zip_service.download_and_extract(
                    download_url, target_file="rol_table", extension="csv"
                )
            )

            file_name = os.path.basename(extracted_file)
            r2_path = f"csv/raw/{file_name}"

            with open(extracted_file, "rb") as file:
                content = file.read()
                self.r2_service.save_to_r2(content, r2_path, "csv")

            download_url = self.r2_service.get_file(r2_path)

            self.zip_service.cleanup_temp_files(extract_dir, temp_zip_path)

            return JSONResponse(status_code=200, content={"url": download_url})

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error while extracting and downloading tables: {str(e)}",
            )
