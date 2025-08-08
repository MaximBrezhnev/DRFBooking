"""
Скрипт для создания `.env` файла, содержащего
переменные окружения, необходимые для  `docker-compose`.
"""

import os
from pathlib import Path

from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=[
        os.path.join("..", "drf_booking", "settings.yaml"),
        os.path.join("..", "drf_booking", ".secrets.yaml"),
    ],
    environments=True,
)

env_lines = [
    f"POSTGRES_DB={settings.POSTGRES_DB}",
    f"POSTGRES_USER={settings.POSTGRES_USER}",
    f"POSTGRES_PASSWORD={settings.POSTGRES_PASSWORD}",
    f"POSTGRES_PORT={settings.POSTGRES_PORT}",
    f"APP_PORT={settings.APP_PORT}",
]

env_path = Path(".env")
env_path.write_text("\n".join(env_lines))
print("✅ .env файл успешно создан")
