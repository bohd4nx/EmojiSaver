import logging
import random
import string
from datetime import datetime, UTC
from typing import Optional, List, Dict, Any

from motor.motor_asyncio import AsyncIOMotorClient

from data.config import config

logger = logging.getLogger(__name__)


class MongoDB:
    def __init__(self):
        self.client = AsyncIOMotorClient(config.MONGO_URL)
        self.db = self.client.jsons
        self.animations = self.db.animations

    @staticmethod
    def _generate_unique_code(length: int = 15) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    async def save_animations(self,
                              user_id: int,
                              message_id: int,
                              animations: List[Dict[str, Any]]) -> bool:
        try:
            doc = {
                'user_id': user_id,
                'message_id': message_id,
                'code': self._generate_unique_code(),
                'created_at': datetime.now(UTC),
                'animations': animations
            }
            await self.animations.insert_one(doc)
            return True
        except Exception as e:
            logger.error(f"Failed to save animations batch to MongoDB: {e}")
            return False

    async def get_user_code(self, user_id: int) -> Optional[str]:
        doc = await self.animations.find_one({'user_id': user_id})
        return doc.get('code') if doc else None

    async def get_animation_by_code(self, code: str) -> Optional[Dict]:
        return await self.animations.find_one({'code': code})

    async def get_animations_code(self, user_id: int, message_id: int) -> Optional[str]:
        doc = await self.animations.find_one({
            'user_id': user_id,
            'message_id': message_id
        })
        return doc.get('code') if doc else None


db = MongoDB()
