import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def load_env():
    env_path = Path(__file__).parent.parent.parent / '.env'
    load_dotenv(env_path)
    
    token = os.getenv('BOT_TOKEN', '').strip()
    if not token:
        logger.error("Missing BOT_TOKEN in environment variables!")
        sys.exit(1)
    
    return {"BOT_TOKEN": token}

config = load_env()
