import pytest
from unittest.mock import MagicMock, call
from services.pdf import PDFService
from fastapi import HTTPException
import itertools


@pytest.fixture
def mock_services(mocker):
    r2_service_mock = mocker.MagicMock()
    csv_service_mock = mocker.MagicMock()
    zip_service_mock = mocker.MagicMock()
    scraper_service_mock = mocker.MagicMock()

    pdf_service = PDFService(r2_service_mock, zip_service_mock, csv_service_mock)

    pdf_service.r2_service = r2_service_mock
    pdf_service.zip_service = zip_service_mock
    pdf_service.scraper_service = scraper_service_mock

    return pdf_service, r2_service_mock, zip_service_mock, scraper_service_mock


def test_process_pdf_success(mock_services, mocker):
    pdf_service, r2_service_mock, zip_service_mock, _ = mock_services

    mocker.patch(
        "services.scraper.ScraperService.get_pdf_links",
        return_value=["http://example.com/file1.pdf"],
    )

    mocker.patch(
        "requests.get", return_value=MagicMock(status_code=200, content=b"PDF content")
    )

    mocker.patch("os.path.exists", return_value=True)

    mock_open = mocker.mock_open()
    mock_open.side_effect = itertools.cycle(
        [
            MagicMock(read=lambda: b"PDF content"),
            MagicMock(read=lambda: b"zip content"),
        ]
    )
    mocker.patch("builtins.open", mock_open)

    mocker.patch("os.remove")
    zip_service_mock.compress_files_to_zip.return_value = None
    r2_service_mock.save_pdf_to_r2.return_value = True

    result = pdf_service.process_pdf(
        "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    )

    assert result is True


def test_process_pdf_failure(mock_services, mocker):
    pdf_service, _, _, _ = mock_services

    mocker.patch(
        "services.scraper.ScraperService.get_pdf_links",
        return_value=["http://example.com/file1.pdf"],
    )

    mocker.patch("requests.get", return_value=MagicMock(status_code=404))

    with pytest.raises(HTTPException):
        pdf_service.process_pdf("http://example.com")


def test_extract_tables_success(mock_services, mocker):
    pdf_service, r2_service_mock, zip_service_mock, csv_service_mock = mock_services

    r2_service_mock.get_file.return_value = "http://example.com/ans.zip"

    mocker.patch(
        "requests.get", return_value=MagicMock(status_code=200, content=b"zip content")
    )

    mock_open = mocker.patch(
        "builtins.open", mocker.mock_open(read_data=b"zip content")
    )
    mocker.patch("os.path.exists", return_value=True)
    mocker.patch("os.makedirs")
    mocker.patch("os.remove")
    mocker.patch("os.walk", return_value=[("/tmp", [], ["file1"])])
    mocker.patch("os.rmdir")

    zip_service_mock.unzip.return_value = "/tmp/sample.pdf"

    mocker.patch(
        "pdfplumber.open",
        return_value=MagicMock(
            pages=[
                MagicMock(
                    extract_table=lambda: [["Header1", "Header2"], ["Data1", "Data2"]]
                )
            ]
        ),
    )

    csv_service_mock.save_to_csv.return_value = "/tmp/sample.csv"

    zip_service_mock.compress_to_zip.return_value = b"zip content"

    r2_service_mock.save_to_r2.return_value = True
    r2_service_mock.get_file.return_value = "/tmp/sample.zip"

    result = pdf_service.extract_tables("sample.pdf")
    assert result == "/tmp/sample.zip"

    zip_service_mock.unzip.assert_called_once()
    zip_service_mock.compress_to_zip.assert_called_once()
    r2_service_mock.save_to_r2.assert_called_once()


def test_replace_abbreviations_in_header():
    header = ["OD", "AMB", "HCO", "HSO", "REF", "PAC", "DUT"]
    PDFService.replace_abbreviations_in_header(header)
    assert header == [
        "Seg. Odontológica",
        "Seg. Ambulatorial",
        "Seg. Hospitalar Com Obstetrícia",
        "Seg. Hospitalar Sem Obstetrícia",
        "Plano Referência",
        "Procedimento de Alta Complexidade",
        "Diretriz de Utilização",
    ]


def test_replace_abbreviations_in_header_no_abbr():
    header = ["XYZ", "ABC"]
    PDFService.replace_abbreviations_in_header(header)
    assert header == ["XYZ", "ABC"]
