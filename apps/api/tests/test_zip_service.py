import pytest
import os
from io import BytesIO
from zipfile import ZipFile
from services.zip import ZIPService
from unittest.mock import patch, mock_open, MagicMock


@pytest.fixture
def zip_service():
    return ZIPService()


def test_compress_to_zip(zip_service, tmp_path):

    test_content = b"Test file content"
    test_file = tmp_path / "test.txt"
    test_file.write_bytes(test_content)

    buffer = zip_service.compress_to_zip(str(test_file))

    assert isinstance(buffer, BytesIO)

    with ZipFile(buffer) as zipf:

        assert "test.txt" in zipf.namelist()

        extracted_content = zipf.read("test.txt")
        assert extracted_content == test_content

    assert not os.path.exists(str(test_file))


def test_compress_files_to_zip(zip_service, tmp_path):

    test_files = []
    file_contents = {"file1.txt": b"Content 1", "file2.txt": b"Content 2"}

    for filename, content in file_contents.items():
        file_path = tmp_path / filename
        file_path.write_bytes(content)
        test_files.append((str(file_path), filename))

    zip_path = str(tmp_path / "test.zip")

    zip_service.compress_files_to_zip(test_files, zip_path)

    assert os.path.exists(zip_path)

    with ZipFile(zip_path, "r") as zipf:
        for filename in file_contents.keys():

            assert filename in zipf.namelist()

            assert zipf.read(filename) == file_contents[filename]

            assert not os.path.exists(str(tmp_path / filename))


def test_unzip_success(zip_service, tmp_path):

    test_content = b"PDF content"
    zip_path = tmp_path / "test.zip"
    extract_dir = str(tmp_path / "extract")
    target_file = "document"
    extension = "pdf"

    with ZipFile(zip_path, "w") as zipf:
        zipf.writestr("document.pdf", test_content)

    result = zip_service.unzip(extract_dir, str(zip_path), target_file, extension)

    assert os.path.exists(result)
    assert os.path.basename(result) == "document.pdf"
    with open(result, "rb") as f:
        assert f.read() == test_content


def test_unzip_file_not_found(zip_service, tmp_path):

    zip_path = tmp_path / "test.zip"
    extract_dir = str(tmp_path / "extract")

    with ZipFile(zip_path, "w") as zipf:
        zipf.writestr("other.txt", b"Some content")

    with pytest.raises(FileNotFoundError) as exc_info:
        zip_service.unzip(extract_dir, str(zip_path), "document", "pdf")
    assert "No file with document found in the ZIP archive" in str(exc_info.value)


@patch("services.zip.requests.get")
def test_download_and_extract_success(mock_get, zip_service, tmp_path):

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"ZIP content"
    mock_get.return_value = mock_response

    test_url = "http://example.com/test.zip"
    target_file = "document"
    extension = "pdf"

    extract_dir = "/tmp/extracted_data"
    temp_zip_path = "/tmp/downloaded_data.zip"
    test_extracted_file = "/tmp/extracted_data/document.pdf"

    with patch.object(ZIPService, "unzip", return_value=test_extracted_file):

        extracted_file, result_dir, result_zip = zip_service.download_and_extract(
            test_url, target_file, extension
        )

        mock_get.assert_called_once_with(test_url)
        assert extracted_file == test_extracted_file
        assert result_dir == extract_dir
        assert result_zip == temp_zip_path


@patch("services.zip.requests.get")
def test_download_and_extract_http_error(mock_get, zip_service):

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    test_url = "http://example.com/test.zip"
    target_file = "document"
    extension = "pdf"

    with pytest.raises(Exception) as exc_info:
        zip_service.download_and_extract(test_url, target_file, extension)

    assert "Failed to download the file: 404" in str(exc_info.value)


@patch("services.zip.os.path.exists")
@patch("services.zip.os.remove")
@patch("services.zip.shutil.rmtree")
def test_cleanup_temp_files(mock_rmtree, mock_remove, mock_exists, zip_service):

    mock_exists.return_value = True

    extract_dir = "/tmp/extract"
    zip_path = "/tmp/test.zip"
    zip_service.cleanup_temp_files(extract_dir, zip_path)

    mock_remove.assert_called_once_with(zip_path)
    mock_rmtree.assert_called_once_with(extract_dir)


@patch("services.zip.os.path.exists")
@patch("services.zip.os.remove")
@patch("services.zip.shutil.rmtree")
def test_cleanup_temp_files_none_paths(
    mock_rmtree, mock_remove, mock_exists, zip_service
):

    mock_exists.return_value = True

    zip_service.cleanup_temp_files(None, None)

    mock_remove.assert_not_called()
    mock_rmtree.assert_not_called()
