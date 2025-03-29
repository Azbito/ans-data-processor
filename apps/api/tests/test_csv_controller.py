import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from controllers.CSVController import CSVController
from fastapi.responses import JSONResponse
import os


@pytest.fixture
def controller():
    with patch("controllers.CSVController.R2Service") as mock_r2, patch(
        "controllers.CSVController.ZIPService"
    ) as mock_zip, patch("controllers.CSVController.CSVService") as mock_csv, patch(
        "controllers.CSVController.PDFService"
    ) as mock_pdf:

        controller = CSVController()
        controller.r2_service = mock_r2.return_value
        controller.zip_service = mock_zip.return_value
        controller.csv_service = mock_csv.return_value
        controller.pdf_service = mock_pdf.return_value
        yield controller


def test_extract_tables_success(controller):
    test_file = "test.pdf"
    test_extension = "pdf"
    result_url = "http://r2.example.com/tables.csv"
    controller.pdf_service.extract_tables.return_value = result_url

    response = controller.extract_tables(test_file, test_extension)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 200
    assert response.body.decode() == f'{{"url":"{result_url}"}}'
    controller.pdf_service.extract_tables.assert_called_once_with(
        test_file, test_extension
    )


def test_extract_tables_error(controller):
    test_file = "test.pdf"
    test_extension = "pdf"
    controller.pdf_service.extract_tables.side_effect = Exception("Extraction failed")

    with pytest.raises(HTTPException) as exc_info:
        controller.extract_tables(test_file, test_extension)
    assert exc_info.value.status_code == 500
    assert "Error while extracting tables" in str(exc_info.value.detail)


def test_extract_and_download_tables_success(controller):
    test_file = "test.pdf"
    test_extension = "pdf"
    download_url = "http://example.com/tables.zip"
    extracted_file = "/tmp/extracted_data/test.pdf"
    extract_dir = "/tmp/extracted_data"
    temp_zip_path = "/tmp/downloaded_data.zip"
    r2_path = "csv/extracted/test.pdf"
    final_download_url = "http://r2.example.com/test.pdf"

    controller.pdf_service.extract_tables.return_value = download_url
    controller.zip_service.download_and_extract.return_value = (
        extracted_file,
        extract_dir,
        temp_zip_path,
    )
    controller.r2_service.get_file.return_value = final_download_url

    mock_file_content = b"file content"
    mock_file = MagicMock()
    mock_file.__enter__.return_value.read.return_value = mock_file_content

    with patch("builtins.open", return_value=mock_file):
        response = controller.extract_and_download_tables(test_file, test_extension)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 200
    assert response.body.decode() == f'{{"url":"{final_download_url}"}}'

    controller.pdf_service.extract_tables.assert_called_once_with(
        test_file, test_extension
    )
    controller.zip_service.download_and_extract.assert_called_once_with(
        download_url, test_file, test_extension
    )
    controller.r2_service.save_to_r2.assert_called_once_with(
        mock_file_content, r2_path, test_extension
    )
    controller.r2_service.get_file.assert_called_once_with(r2_path)
    controller.zip_service.cleanup_temp_files.assert_called_once_with(
        extract_dir, temp_zip_path
    )


def test_extract_and_download_tables_extraction_error(controller):
    test_file = "test.pdf"
    test_extension = "pdf"

    controller.pdf_service.extract_tables.side_effect = Exception("Extraction failed")

    with pytest.raises(HTTPException) as exc_info:
        controller.extract_and_download_tables(test_file, test_extension)

    assert exc_info.value.status_code == 500
    assert "Error while extracting and downloading tables" in str(exc_info.value.detail)

    controller.zip_service.download_and_extract.assert_not_called()
    controller.r2_service.save_to_r2.assert_not_called()
    controller.r2_service.get_file.assert_not_called()


def test_extract_and_download_tables_download_error(controller):
    test_file = "test.pdf"
    test_extension = "pdf"
    download_url = "http://example.com/tables.zip"

    controller.pdf_service.extract_tables.return_value = download_url
    controller.zip_service.download_and_extract.side_effect = Exception(
        "Download failed"
    )

    with pytest.raises(HTTPException) as exc_info:
        controller.extract_and_download_tables(test_file, test_extension)

    assert exc_info.value.status_code == 500
    assert "Error while extracting and downloading tables" in str(exc_info.value.detail)

    controller.pdf_service.extract_tables.assert_called_once_with(
        test_file, test_extension
    )
    controller.zip_service.download_and_extract.assert_called_once_with(
        download_url, test_file, test_extension
    )
