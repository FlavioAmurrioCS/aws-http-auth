# flake8: noqa: S106

import datetime
from unittest.mock import patch


def test_request_signing() -> None:
    from aws_http_auth.credentials import AWSCredentials
    from aws_http_auth.signer import sign_requests

    creds = AWSCredentials(
        aws_access_key_id="aws_access_key_id",
        aws_secret_access_key="aws_secret_access",
        aws_session_token="aws_session_token",
    )

    fixed_time = datetime.datetime(2023, 10, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)

    with patch("datetime.datetime") as mock_datetime:
        mock_datetime.now.return_value = fixed_time
        mock_datetime.utcnow.return_value = fixed_time

        method = "GET"
        url = "https://secretsmanager.us-east-1.amazonaws.com/"
        body = b'{"key": "value"}'
        headers = {
            "Content-Type": "application/json",
            "X-Amz-Target": "X-Amz-Target",
        }

        actual = sign_requests(creds=creds, method=method, url=url, body=body, headers=headers)
        print("*" * 100)
        print(actual)
        print("*" * 100)

        expected = {
            "Content-Type": "application/json",
            "X-Amz-Date": "20231001T120000Z",
            "X-Amz-Target": "X-Amz-Target",
            "Authorization": "AWS4-HMAC-SHA256 Credential=aws_access_key_id/20231001/us-east-1/secretsmanager/aws4_request, SignedHeaders=content-type;host;x-amz-date;x-amz-target, Signature=78377ced44802809578beb2c9a9d5658175dbc866e7389aa6d3c263982e852b7",  # noqa: E501
            "X-Amz-Security-Token": "aws_session_token",
        }

        assert actual == expected
