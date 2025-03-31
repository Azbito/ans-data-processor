import pytest
from unittest.mock import patch, MagicMock
from controllers.csv import CSVController
from fastapi import HTTPException
from fastapi.responses import JSONResponse
import os
from services.r2 import R2Service
from services.zip import ZIPService
from services.csv import CSVService
from services.pdf import PDFService

@pytest.fixture
def controller():
    mock_r2 = MagicMock(spec=R2Service)
    mock_zip = MagicMock(spec=ZIPService)
    mock_csv = MagicMock(spec=CSVService)
    mock_pdf = MagicMock(spec=PDFService)
    
    with patch('controllers.csv.R2Service', return_value=mock_r2), \
         patch('controllers.csv.ZIPService', return_value=mock_zip), \
         patch('controllers.csv.CSVService', return_value=mock_csv), \
         patch('controllers.csv.PDFService', return_value=mock_pdf):
        controller = CSVController()
        yield controller

def test_extract_tables_success(controller):
    expected_url = "https://example.com/tables.csv"
    controller.pdf_service.extract_tables.return_value = expected_url
    
    result = controller.extract_tables("file.pdf")
    
    assert isinstance(result, JSONResponse)
    assert result.status_code == 200
    assert result.body == b'{"url":"https://example.com/tables.csv"}'
    controller.pdf_service.extract_tables.assert_called_once_with("file.pdf")

def test_extract_tables_error(controller):
    error_msg = "Extraction failed"
    controller.pdf_service.extract_tables.side_effect = Exception(error_msg)
    
    with pytest.raises(HTTPException) as exc_info:
        controller.extract_tables("file.pdf")
    
    assert exc_info.value.status_code == 500
    assert error_msg in str(exc_info.value.detail)

def test_download_unzipped_table_success(controller):
    download_url = "https://example.com/tables.zip"
    extracted_file = "/tmp/extracted/tables.csv"
    extract_dir = "/tmp/extracted"
    temp_zip_path = "/tmp/tables.zip"
    r2_path = "csv/extracted/tables.csv"
    final_url = "https://r2.example.com/csv/extracted/tables.csv"

    controller.pdf_service.extract_tables.return_value = download_url
    controller.zip_service.download_and_extract.return_value = (
        extracted_file,
        extract_dir,
        temp_zip_path
    )
    controller.r2_service.get_file.return_value = final_url

    mock_file = MagicMock()
    mock_file.__enter__.return_value.read.return_value = b"csv,data,here"

    with patch("builtins.open", return_value=mock_file):
        result = controller.download_unzipped_table()

    assert isinstance(result, JSONResponse)
    assert result.status_code == 200
    assert result.body == b'{"url":"https://r2.example.com/csv/extracted/tables.csv"}'

    controller.pdf_service.extract_tables.assert_called_once()
    extract_tables_args, extract_tables_kwargs = controller.pdf_service.extract_tables.call_args

    assert "target_file" in extract_tables_kwargs
    assert extract_tables_kwargs["target_file"] == "Anexo_I"

    controller.zip_service.download_and_extract.assert_called_once_with(
        download_url, 
        target_file="rol_table", 
        extension="csv"
    )

    controller.r2_service.save_to_r2.assert_called_once()
    args, kwargs = controller.r2_service.save_to_r2.call_args

    assert isinstance(args[0], bytes)
    assert args[1] == "csv/extracted/tables.csv"
    assert args[2] == "csv"

    controller.r2_service.get_file.assert_called_once_with("csv/extracted/tables.csv")
    controller.zip_service.cleanup_temp_files.assert_called_once_with(extract_dir, temp_zip_path)

def test_download_unzipped_table_extraction_error(controller):
    error_msg = "Extraction failed"
    controller.pdf_service.extract_tables.side_effect = Exception(error_msg)
    
    with pytest.raises(HTTPException) as exc_info:
        controller.download_unzipped_table()
    
    assert exc_info.value.status_code == 500
    assert error_msg in str(exc_info.value.detail)

def test_download_unzipped_table_download_error(controller):
    download_url = "https://example.com/tables.zip"
    error_msg = "Download failed"
    
    controller.pdf_service.extract_tables.return_value = download_url
    controller.zip_service.download_and_extract.side_effect = Exception(error_msg)
    
    with pytest.raises(HTTPException) as exc_info:
        controller.download_unzipped_table()
    
    assert exc_info.value.status_code == 500
    assert error_msg in str(exc_info.value.detail)