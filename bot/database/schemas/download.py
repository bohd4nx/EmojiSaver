from dataclasses import dataclass
from datetime import datetime


@dataclass
class DownloadSchema:
    id: int
    user_id: int
    content_type: str
    content_id: str | None
    created_at: datetime


@dataclass
class DownloadCreateSchema:
    user_id: int
    content_type: str
    content_id: str | None = None
