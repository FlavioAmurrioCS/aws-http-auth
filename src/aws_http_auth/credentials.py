from __future__ import annotations

from typing import NamedTuple


class AWSCredentials(NamedTuple):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{k}=***' for k in self._asdict())})"
