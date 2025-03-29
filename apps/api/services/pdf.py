import requests
from fastapi import HTTPException
import pdfplumber
from services.scraper import ScraperService
from utils.get_abbreviation import get_abbreviation
import os
from typing import List, Tuple


class PDFService:
    def __init__(self, r2_service, zip_service, csv_service):
        self.r2_service = r2_service
        self.zip_service = zip_service
        self.csv_service = csv_service

    def process_pdf(self, target_url: str) -> bool:
        files_to_zip: List[Tuple[str, str]] = []
        zip_file_path = "/tmp/asn.zip"
        try:
            pdf_links = ScraperService.get_pdf_links(target_url)

            for pdf_link in pdf_links:
                file_response = requests.get(pdf_link)

                if file_response.status_code != 200:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Failed to download PDF from {pdf_link}. Status code: {file_response.status_code}",
                    )

                filename = pdf_link.split("/")[-1]
                file_path = f"/tmp/{filename}"

                with open(file_path, "wb") as f:
                    f.write(file_response.content)

                files_to_zip.append((file_path, filename))

            self.zip_service.compress_files_to_zip(files_to_zip, zip_file_path)

            with open(zip_file_path, "rb") as zip_file:
                self.r2_service.save_pdf_to_r2(zip_file.read(), "asn.zip", "zip")

            os.remove(zip_file_path)
            return True

        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error while processing PDF: {str(e)}"
            )

        finally:
            for file_path, _ in files_to_zip:
                if os.path.exists(file_path):
                    os.remove(file_path)

            if os.path.exists(zip_file_path):
                self.zip_service.cleanup_temp_files(None, zip_file_path)

    def extract_tables(self, target_file: str, extension: str) -> str:
        extract_dir = "/tmp/extracted_pdfs"
        zip_file_path = os.path.join(extract_dir, "asn.zip")
        csv_file_name = "/tmp/rol_table.csv"
        tmp_csv = ""

        try:
            zipped_file_url = self.r2_service.get_file("pdfs/asn.zip")
            response = requests.get(zipped_file_url)

            if response.status_code != 200:
                raise Exception(f"Failed to download the file: {response.status_code}")

            os.makedirs(extract_dir, exist_ok=True)

            with open(zip_file_path, "wb") as f:
                f.write(response.content)

            zipped_file = zip_file_path

            pdf_file = self.zip_service.unzip(
                extract_dir, zipped_file, target_file, extension
            )

            data = []
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    table = page.extract_table()
                    if table:
                        header = table[0]
                        self.replace_abbreviations_in_header(header)
                        data.extend(table)

            tmp_csv = self.csv_service.save_to_csv(data, csv_file_name)
            name = "Thiago"

            zip_file = self.zip_service.compress_to_zip(tmp_csv)

            path = f"csv/Teste_{name}.zip"
            res = self.r2_service.save_to_r2(zip_file, path, "zip")

            if not res:
                return ""

            file_from_r2 = self.r2_service.get_file(path)

            return file_from_r2

        finally:
            self.zip_service.cleanup_temp_files(extract_dir, zip_file_path)

            if csv_file_name and os.path.exists(csv_file_name):
                os.remove(csv_file_name)

    @staticmethod
    def replace_abbreviations_in_header(header: List[str]) -> None:
        for i, column in enumerate(header):
            abbreviation = get_abbreviation(header[i])
            if abbreviation != "Abbreviation not found":
                header[i] = abbreviation
