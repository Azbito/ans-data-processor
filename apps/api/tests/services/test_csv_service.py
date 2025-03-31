import pytest
from unittest.mock import mock_open, patch, call
from services.csv import CSVService


def test_save_to_csv_success():
    data = [
        ["Header1", "Header2"],
        ["Data1", "Data2"],
    ]
    csv_file = "/tmp/test_file.csv"

    with patch("builtins.open", mock_open()) as mock_file:
        result = CSVService.save_to_csv(data, csv_file)

        assert result == csv_file

        mock_file.assert_called_once_with(csv_file, "w", newline="", encoding="utf-8")

        mock_writer = mock_file().write
        calls = [call("Header1,Header2\r\n"), call("Data1,Data2\r\n")]
        mock_writer.assert_has_calls(calls, any_order=True)


def test_save_to_csv_empty_data():
    data = []
    csv_file = "/tmp/test_file.csv"

    with patch("builtins.open", mock_open()) as mock_file:
        result = CSVService.save_to_csv(data, csv_file)

        assert result == ""

        mock_file.assert_not_called()


def test_save_to_csv_no_file_creation_on_empty_data():
    data = []
    csv_file = "/tmp/test_file.csv"

    with patch("builtins.open", mock_open()) as mock_file:
        result = CSVService.save_to_csv(data, csv_file)

        mock_file.assert_not_called()
