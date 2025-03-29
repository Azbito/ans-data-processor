import pytest
import os
from unittest.mock import patch, mock_open
from models.file import File


def test_file_init():

    test_filename = "test.txt"
    test_content = b"test content"

    file = File(test_filename, test_content)

    assert file.filename == test_filename
    assert file.content == test_content


@patch("builtins.open", new_callable=mock_open)
def test_file_save(mock_file):

    test_filename = "test.txt"
    test_content = b"test content"
    test_path = "/tmp/test.txt"

    file = File(test_filename, test_content)
    file.save(test_path)

    mock_file.assert_called_once_with(test_path, "wb")

    file_handle = mock_file()

    file_handle.write.assert_called_once_with(test_content)


def test_file_save_integration(tmp_path):

    test_filename = "test.txt"
    test_content = b"test content"
    test_path = os.path.join(tmp_path, test_filename)

    file = File(test_filename, test_content)
    file.save(test_path)

    assert os.path.exists(test_path)
    with open(test_path, "rb") as f:
        saved_content = f.read()
    assert saved_content == test_content
