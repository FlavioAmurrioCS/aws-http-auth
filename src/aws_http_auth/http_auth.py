from __future__ import annotations

import sys

if sys.platform == "emscripten":
    try:
        import pyodide_http

        pyodide_http.patch_all()

    except ImportError:
        msg = (
            "pyodide_http is required for AWSV4SignerAuth to work in Pyodide. "
            "Please install it using 'micropip.install(\"pyodide-http\")'."
        )
        raise ImportError(msg) from None


from typing import TYPE_CHECKING

from aws_http_auth.signer import sign_requests

if TYPE_CHECKING:
    from collections.abc import Generator

    import httpx
    import requests

    from aws_http_auth.credentials import AWSCredentials


try:
    from httpx import Auth
except ImportError:
    Auth = object  # type: ignore[misc,assignment,unused-ignore]

try:
    from requests.auth import AuthBase
except ImportError:
    AuthBase = object  # type: ignore[misc,assignment]


class AWSV4SignerAuth(Auth, AuthBase):  # pyright: ignore[reportGeneralTypeIssues] # pyrefly: ignore[invalid-inheritance]
    def __init__(self, credentials: AWSCredentials) -> None:
        self.credentials = credentials

    def auth_flow(self, request: httpx.Request) -> Generator[httpx.Request, httpx.Response, None]:
        signed_headers = sign_requests(
            creds=self.credentials,
            method=request.method,
            url=str(request.url),
            body=request.content,
            headers=request.headers,
        )

        for key, value in signed_headers.items():
            request.headers[key] = value

        yield request

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        signed_headers = sign_requests(
            creds=self.credentials,
            method=r.method or "GET",
            url=str(r.url),
            body=r.body,  # type: ignore[arg-type]
            headers=r.headers or {},
        )

        for key, value in signed_headers.items():
            r.headers[key] = value  # pyrefly: ignore[missing-attribute]

        return r
