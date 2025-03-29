import pytest
from unittest.mock import patch, MagicMock
from services.scraper import ScraperService


def test_get_pdf_links_success():
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

    pdf_links = ScraperService.get_pdf_links(url)

    assert isinstance(pdf_links, list)
    assert len(pdf_links) > 0
    assert all(link.endswith(".pdf") for link in pdf_links)
    assert all("Anexo" in link for link in pdf_links)


@patch("services.scraper.requests.get")
def test_get_pdf_links_http_error(mock_get):

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    url = "https://example.com/nonexistent"

    with pytest.raises(Exception) as exc_info:
        ScraperService.get_pdf_links(url)

    assert f"Error while accessing: {url}" in str(exc_info.value)
    mock_get.assert_called_once_with(url)


@patch("services.scraper.requests.get")
def test_get_pdf_links_no_pdfs_found(mock_get):

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '<html><body><a href="file.doc">Document</a></body></html>'
    mock_get.return_value = mock_response

    url = "https://example.com/no-pdfs"

    with pytest.raises(Exception) as exc_info:
        ScraperService.get_pdf_links(url)

    assert f"There's no PDF URL for: {url}" in str(exc_info.value)
    mock_get.assert_called_once_with(url)
