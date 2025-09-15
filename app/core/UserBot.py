import logging

from pyrogram import Client

from .config import config

logging.getLogger('pyrogram').setLevel(logging.ERROR)


class UserBot:
    def __init__(self) -> None:
        self.client = Client(
            name="account",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            phone_number=config.PHONE_NUMBER,
            device_model="Telegram Desktop",
            system_version="Windows 11 x64 (24H2)",
            app_version="8.9.2",
            lang_code="en",
            sleep_threshold=30,
            max_concurrent_transmissions=10,
            no_updates=True
        )
        self.username = None
        self.user_id = None

    async def start(self) -> None:
        await self.client.start()
        me = await self.client.get_me()
        self.username = me.username
        self.user_id = me.id

    async def stop(self) -> None:
        await self.client.stop()
