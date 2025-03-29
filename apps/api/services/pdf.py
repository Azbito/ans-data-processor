import requests
from io import BytesIO
from zipfile import ZipFile
from models.file import File
from utils.http_utils import get_pdf_links
from fastapi import HTTPException


class PDFService:
    def __init__(self, r2_service):
        self.r2_service = r2_service

    def process_pdf(self, target_url):
        try:
            pdf_links = get_pdf_links(target_url)

            zip_buffer = BytesIO()

            with ZipFile(zip_buffer, "w") as zip_file:
                for pdf_link in pdf_links:
                    file_response = requests.get(pdf_link)

                    if file_response.status_code != 200:
                        raise HTTPException(
                            status_code=500,
                            detail=f"Failed to download PDF from {pdf_link}. Status code: {file_response.status_code}",
                        )

                    filename = pdf_link.split("/")[-1]

                    zip_file.writestr(filename, file_response.content)

            zip_buffer.seek(0)

            self.r2_service.save_pdf_to_r2(zip_buffer.read(), "asn.zip", "zip")

            return True
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error while processing PDF: {str(e)}"
            )
