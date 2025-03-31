import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from controllers.pdf import PDFController
from fastapi.responses import JSONResponse
from services.r2 import R2Service
from services.zip import ZIPService
from services.csv import CSVService
from services.pdf import PDFService

@pytest.fixture
def controller():
    with patch("controllers.pdf.R2Service") as mock_r2, patch(
        "controllers.pdf.ZIPService"
    ) as mock_zip, patch("controllers.pdf.CSVService") as mock_csv, patch(
        "controllers.pdf.PDFService"
    ) as mock_pdf:

        controller = PDFController()
        controller.r2_service = mock_r2.return_value
        controller.zip_service = mock_zip.return_value
        controller.csv_service = mock_csv.return_value
        controller.pdf_service = mock_pdf.return_value
        yield controller


def test_ans_pdf_scrapper_success(controller):

    test_url = "http://example.com"
    download_url = "http://r2.example.com/pdfs/asn.zip"
    controller.pdf_service.process_pdf.return_value = True
    controller.r2_service.get_file.return_value = download_url

    response = controller.ans_pdf_scrapper(test_url)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 200
    assert response.body.decode() == f'{{"url":"{download_url}"}}'
    controller.pdf_service.process_pdf.assert_called_once_with(test_url)
    controller.r2_service.get_file.assert_called_once_with("pdfs/asn.zip")


def test_ans_pdf_scrapper_no_data(controller):

    test_url = "http://example.com"
    controller.pdf_service.process_pdf.return_value = False

    response = controller.ans_pdf_scrapper(test_url)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    assert "No data found" in response.body.decode()
    controller.pdf_service.process_pdf.assert_called_once_with(test_url)
    controller.r2_service.get_file.assert_not_called()


def test_ans_pdf_scrapper_error(controller):

    test_url = "http://example.com"
    controller.pdf_service.process_pdf.side_effect = Exception("Processing failed")

    with pytest.raises(HTTPException) as exc_info:
        controller.ans_pdf_scrapper(test_url)
    assert exc_info.value.status_code == 500
    assert "ANS PDF Scrapper" in str(exc_info.value.detail)


def test_extract_tables_success(controller):

    test_file = "test.pdf"
    result_url = "http://r2.example.com/tables.csv"
    controller.pdf_service.extract_tables.return_value = result_url

    response = controller.extract_tables(test_file)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 200
    assert response.body.decode() == f'{{"url":"{result_url}"}}'
    controller.pdf_service.extract_tables.assert_called_once_with(
        test_file
    )


def test_extract_tables_error(controller):

    test_file = "test.pdf"
    controller.pdf_service.extract_tables.side_effect = Exception("Extraction failed")

    with pytest.raises(HTTPException) as exc_info:
        controller.extract_tables(test_file)
    assert exc_info.value.status_code == 500
    assert "Error while extracting tables" in str(exc_info.value.detail)