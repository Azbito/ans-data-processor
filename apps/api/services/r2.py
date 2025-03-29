from config.r2 import s3_client
import os
from fastapi import HTTPException
from typing import Union


class R2Service:
    def get_file(self, path: str) -> str:
        try:
            url = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": os.getenv("R2_BUCKET_NAME"),
                    "Key": path,
                },
                ExpiresIn=3600,
            )
            return url
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error while trying to get file from R2: {str(e)}",
            )

    def save_to_r2(self, content: Union[str, bytes], path: str, file_type: str) -> bool:
        try:
            content_type = f"application/{file_type}"

            s3_client.put_object(
                Bucket=os.getenv("R2_BUCKET_NAME"),
                Key=path,
                Body=content,
                ContentType=content_type,
            )

            return True
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error while trying to save file to R2: {str(e)}",
            )

    def save_pdf_to_r2(
        self, pdf_data: bytes, pdf_filename: str, file_type: str
    ) -> None:
        try:
            files_path = "pdfs/" + pdf_filename
            content_type = "application/" + file_type

            s3_client.put_object(
                Bucket=os.getenv("R2_BUCKET_NAME"),
                Key=files_path,
                Body=pdf_data,
                ContentType=content_type,
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error while trying to save file to R2: {str(e)}",
            )
