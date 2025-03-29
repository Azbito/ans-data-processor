from zipfile import ZipFile, ZIP_DEFLATED
import os
from io import BytesIO
from typing import List, Tuple


class ZIPService:
    @staticmethod
    def compress_to_zip(file: str) -> BytesIO:
        buffer = BytesIO()

        with ZipFile(buffer, "w", ZIP_DEFLATED) as zipf:
            zipf.write(file, arcname=os.path.basename(file))

        buffer.seek(0)
        os.remove(file)

        return buffer

    @staticmethod
    def compress_files_to_zip(files: List[Tuple[str, str]], zip_file_path: str) -> None:
        with ZipFile(zip_file_path, "w", ZIP_DEFLATED) as zipf:
            for file_path, file_name in files:
                zipf.write(file_path, file_name)
                os.remove(file_path)

    @staticmethod
    def unzip(extract_dir: str, zipped_file: str, target_file: str, extension: str) -> str:
        os.makedirs(extract_dir, exist_ok=True)

        with ZipFile(zipped_file, "r") as zip_ref:
            for file_name in zip_ref.namelist():
                if target_file in file_name and file_name.endswith(extension):
                    zip_ref.extract(file_name, extract_dir)
                    pdf_file = os.path.join(extract_dir, file_name)

                    return pdf_file
            else:
                raise FileNotFoundError(
                    "No file with " + target_file + " found in the ZIP archive."
                )
