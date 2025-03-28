from config.r2 import s3_client
import os


class R2Service:
    def save_pdf_to_r2(pdf_data, pdf_filename):
        try:
            s3_client.put_object(
                Bucket=os.getenv("R2_BUCKET_NAME"),
                Key=pdf_filename,
                Body=pdf_data,
                ContentType="application/pdf",
            )
            print(f"Arquivo {pdf_filename} enviado para o R2 com sucesso!")
        except Exception as e:
            print(f"Erro ao enviar o arquivo {pdf_filename} para o R2: {e}")
