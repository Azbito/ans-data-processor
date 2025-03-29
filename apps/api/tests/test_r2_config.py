import pytest
from unittest.mock import patch, MagicMock


@patch("boto3.client")
@patch("config.r2.os.getenv")
def test_r2_client_configuration(mock_getenv, mock_boto3_client):
    mock_getenv.side_effect = lambda key: {
        "R2_ACCESS_KEY": "test_access_key",
        "R2_SECRET_KEY": "test_secret_key",
        "R2_BUCKET_NAME": "test_bucket",
        "R2_ENDPOINT_URL": "https://test.r2.com",
    }.get(key)

    mock_client = MagicMock()
    mock_boto3_client.return_value = mock_client

    from importlib import reload
    import config.r2

    reload(config.r2)
    from config.r2 import s3_client

    mock_boto3_client.assert_called_once()
    args, kwargs = mock_boto3_client.call_args

    assert args[0] == "s3"
    assert kwargs["aws_access_key_id"] == "test_access_key"
    assert kwargs["aws_secret_access_key"] == "test_secret_key"
    assert kwargs["endpoint_url"] == "https://test.r2.com"
    assert "config" in kwargs

    assert s3_client == mock_client


def test_r2_client_exists():
    from config.r2 import s3_client

    assert s3_client is not None
