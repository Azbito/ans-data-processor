import pytest
import os
from io import BytesIO
from zipfile import ZipFile
from services.zip import ZIPService
from unittest.mock import patch, mock_open


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
