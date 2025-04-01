import pytest
from datetime import datetime
from utils.get_last_period_range import get_last_period_range


@pytest.fixture
def mock_datetime_now(mocker):
    return mocker.patch("datetime.datetime")


def test_get_last_period_range_quarterly_in_q1(mock_datetime_now):
    mock_datetime_now.now.return_value = datetime(2025, 2, 15)
    start_date, end_date = get_last_period_range(
        "quarterly", mock_datetime_now.now.return_value
    )
    print(start_date, end_date)
    assert start_date == datetime(2024, 10, 1)
    assert end_date == datetime(2024, 12, 31)


def test_get_last_period_range_yearly(mock_datetime_now):
    mock_datetime_now.now.return_value = datetime(2025, 2, 15)
    start_date, end_date = get_last_period_range("yearly")
    assert start_date == datetime(2024, 1, 1)
    assert end_date == datetime(2024, 12, 31, 23, 59, 59, 999999)


def test_get_last_period_range_quarterly_in_q2(mock_datetime_now):
    start_date, end_date = get_last_period_range("quarterly", datetime(2025, 8, 15))
    assert start_date == datetime(2025, 4, 1)
    assert end_date == datetime(2025, 6, 30)


def test_get_last_period_range_quarterly_in_q3(mock_datetime_now):
    start_date, end_date = get_last_period_range("quarterly", datetime(2025, 4, 15))
    assert start_date == datetime(2025, 1, 1)
    assert end_date == datetime(2025, 3, 31)


def test_get_last_period_range_quarterly_in_q4(mock_datetime_now):
    start_date, end_date = get_last_period_range("quarterly", datetime(2025, 11, 15))
    assert start_date == datetime(2025, 7, 1)
    assert end_date == datetime(2025, 9, 30)
