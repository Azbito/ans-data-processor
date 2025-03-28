import requests
from io import BytesIO
from zipfile import ZipFile
from models.file import File
from utils.http_utils import get_pdf_links


class PDFService:
    def __init__(self, r2_service):
        self.r2_service = r2_service

    def process_pdf(self, target_url):

        pdf_links = get_pdf_links(target_url)

        zip_buffer = BytesIO()
        with ZipFile(zip_buffer, "w") as zip_file:
            for pdf_link in pdf_links:
                file_response = requests.get(pdf_link)
                file = File(pdf_link.split("/")[-1], file_response.content)

                self.r2_service.save_pdf_to_r2(file.data, file.filename)

                zip_file.writestr(file.filename, file.data)

        zip_buffer.seek(0)
        return zip_buffer
