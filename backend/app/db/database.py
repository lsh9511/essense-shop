from tortoise import Tortoise
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgres://localhost/essence")

# Tortoise ORM 설정
TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.brand",
                "app.models.product",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "Asia/Seoul",
}


async def init_db() -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()
