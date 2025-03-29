from config.r2 import s3_client
import os
from fastapi import HTTPException


class R2Service:
    def get_file(self, path):
        try:
            print(path)
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
                detail=f"Error while trying to get file to R2: {str(e)}",
            )

    def save_pdf_to_r2(self, pdf_data, pdf_filename, file_type):
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
