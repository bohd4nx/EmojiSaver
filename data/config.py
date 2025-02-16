from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    BOT_TOKEN: str = "7242027636:AAEf8GufH_pslyJLHt1FPkdny9fUEk_nXZA"
    API_ID: str = "29414111"
    API_HASH: str = "e35fe225ebb9d7a457fd9e82efb90ec0"
    PHONE_NUMBER: str = "+380777770345"
    DOWNLOAD_DIR: str = "../temp"


config = Config()
