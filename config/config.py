import json
from typing import Optional, Type
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict
from pydantic import Field, SecretStr, field_validator
import logging
from pathlib import Path

from app.tarot_daily_card.manager import ITarotDailyCardGenerator
from config.models import TarotCard
from implementations.gigachat_daily_card_generator import GigaChatTarotDailyCardGenerator

class Settings(BaseSettings):
    
    TELEGRAM_BOT_TOKEN: SecretStr = Field(None, env="TELEGRAM_BOT_TOKEN")
    
    GIGACHAT_CREDENTIALS: SecretStr = Field(None, env="GIGACHAT_CREDENTIALS")
    GIGACHAT_MODEL: str = Field("GigaChat", env="GIGACHAT_MODEL")
    GIGACHAT_SCOPE: str = Field("GIGACHAT_API_PERS", env="GIGACHAT_SCOPE")
    GIGACHAT_CA_BUNDLE_FILE: str = Field("russian_trusted_root_ca.cer", env="GIGACHAT_CA_BUNDLE_FILE")

    BASE_IMAGE_URLS: List[str] = [
        "https://i.pinimg.com/736x/07/04/4b/07044befeccfd9edc04a63ab924a3a5d.jpg",
        "https://i.pinimg.com/736x/8e/bb/f7/8ebbf7ed755453625485e4609a8cc9b2.jpg",
        "https://i.pinimg.com/736x/73/d9/d6/73d9d6a105169cebf2a02d4c71e70734.jpg",
        "https://i.pinimg.com/736x/d0/0e/f3/d00ef3f724db899e934a79084ada3bd3.jpg",
        "https://i.pinimg.com/736x/a9/52/62/a95262fe6371ae72577bb603d870a3f1.jpg"
    ]

    TAROT_DECK: List[TarotCard] = Field(None, description="Колода карт Таро с их значениями")

    TAROT_DAILY_CARD_GENERATOR_CLASS: Optional[ITarotDailyCardGenerator] = Field(default=None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Создаем экземпляр генератора **после** загрузки значений из env
        self.TAROT_DAILY_CARD_GENERATOR_CLASS = GigaChatTarotDailyCardGenerator(
            credentials=self.GIGACHAT_CREDENTIALS.get_secret_value() if self.GIGACHAT_CREDENTIALS else None,
            scope=self.GIGACHAT_SCOPE,
            model=self.GIGACHAT_MODEL,
            ca_bundle_file=self.GIGACHAT_CA_BUNDLE_FILE
        )
        
    @field_validator('TAROT_DECK', mode='before')
    @classmethod
    def load_tarot_from_json(cls, v, info):
        json_path = Path('config/tarot_cards.json')
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    cards = json.load(f)
                    if isinstance(cards, list):
                        return cards
                    logging.warning("JSON файл с картами должен содержать массив")
            except Exception as e:
                logging.error(f"Ошибка загрузки tarot_cards.json: {e}")
        
        # Если JSON не загрузился, возвращаем дефолтное значение
        return v


logging.basicConfig(
    level=logging.INFO,  # Минимальный уровень логирования
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()         # Вывод в консоль
    ]
)

# Создаем экземпляр настроек
settings = Settings()