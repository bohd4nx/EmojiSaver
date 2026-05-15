from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserSchema:
    user_id: int
    username: str | None
    created_at: datetime
    updated_at: datetime


@dataclass
class UserCreateSchema:
    user_id: int
    username: str | None = None
