import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from services.r2 import R2Service
import os


@pytest.fixture
def r2_service():
    return R2Service()


@pytest.fixture
def mock_s3_client():
    with patch("services.r2.s3_client") as mock_client:
        yield mock_client


def test_get_file_success(r2_service, mock_s3_client):

    test_path = "test/file.pdf"
    expected_url = "https://example.com/test.pdf"
    mock_s3_client.generate_presigned_url.return_value = expected_url

    result = r2_service.get_file(test_path)

    assert result == expected_url
    mock_s3_client.generate_presigned_url.assert_called_once_with(
        "get_object",
        Params={
            "Bucket": os.getenv("R2_BUCKET_NAME"),
            "Key": test_path,
        },
        ExpiresIn=3600,
    )


def test_get_file_failure(r2_service, mock_s3_client):

    mock_s3_client.generate_presigned_url.side_effect = Exception("Connection error")

    with pytest.raises(HTTPException) as exc_info:
        r2_service.get_file("test/file.pdf")
    assert exc_info.value.status_code == 500
    assert "Error while trying to get file from R2" in str(exc_info.value.detail)


def test_save_to_r2_success(r2_service, mock_s3_client):

    test_content = "test content"
    test_path = "test/file.txt"
    test_type = "txt"

    result = r2_service.save_to_r2(test_content, test_path, test_type)

    assert result is True
    mock_s3_client.put_object.assert_called_once_with(
        Bucket=os.getenv("R2_BUCKET_NAME"),
        Key=test_path,
        Body=test_content,
        ContentType="application/txt",
    )


def test_save_to_r2_failure(r2_service, mock_s3_client):

    mock_s3_client.put_object.side_effect = Exception("Upload failed")

    with pytest.raises(HTTPException) as exc_info:
        r2_service.save_to_r2("content", "test.txt", "txt")
    assert exc_info.value.status_code == 500
    assert "Error while trying to save file to R2" in str(exc_info.value.detail)


def test_save_pdf_to_r2_success(r2_service, mock_s3_client):

    test_pdf_data = b"PDF content"
    test_filename = "test.pdf"
    test_type = "pdf"

    r2_service.save_pdf_to_r2(test_pdf_data, test_filename, test_type)

    mock_s3_client.put_object.assert_called_once_with(
        Bucket=os.getenv("R2_BUCKET_NAME"),
        Key="pdfs/test.pdf",
        Body=test_pdf_data,
        ContentType="application/pdf",
    )


def test_save_pdf_to_r2_failure(r2_service, mock_s3_client):

    mock_s3_client.put_object.side_effect = Exception("Upload failed")

    with pytest.raises(HTTPException) as exc_info:
        r2_service.save_pdf_to_r2(b"PDF content", "test.pdf", "pdf")
    assert exc_info.value.status_code == 500
    assert "Error while trying to save file to R2" in str(exc_info.value.detail)
