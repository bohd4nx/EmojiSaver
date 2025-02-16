from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    BOT_TOKEN: str = ""
    API_ID: str = ""
    API_HASH: str = ""
    PHONE_NUMBER: str = "+"
    DOWNLOAD_DIR: str = "../temp"
    MONGO_URL: str = ""


config = Config()
