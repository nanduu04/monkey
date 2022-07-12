from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping


@dataclass
class UserCredentials:
    username: str
    password_hash: str

    def __bool__(self) -> bool:
        return bool(self.username and self.password_hash)

    def to_mapping(self) -> Mapping:
        return asdict(self)
