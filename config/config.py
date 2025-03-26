from typing import Optional
from pydantic_settings import BaseSettings  # Измененный импорт
from pydantic import Field, SecretStr
import logging


class Settings(BaseSettings):
    
    TELEGRAM_BOT_TOKEN: SecretStr = Field(None, env="TELEGRAM_BOT_TOKEN")
    
    GIGACHAT_CREDENTIALS: SecretStr = Field(None, env="GIGACHAT_CREDENTIALS")


logging.basicConfig(
    level=logging.INFO,  # Минимальный уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()         # Вывод в консоль
    ]
)

# Создаем экземпляр настроек
settings = Settings()