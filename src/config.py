import os
from pathlib import Path

import dotenv

PROJECT_ROOT: Path = Path(__file__).parent.parent
dotenv.load_dotenv(PROJECT_ROOT / ".env", verbose=True)

APP_DB_DSN = os.environ.get(
    "APP_DB_DSN", "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "fill_me")
