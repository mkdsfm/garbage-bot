import json
from typing import Optional
from pydantic_settings import BaseSettings
from typing import Optional, List, Dict
from pydantic import Field, SecretStr, BaseModel, field_validator
import logging
from pathlib import Path

class TarotCard(BaseModel):
    name: str
    key_words: str
    meaning: str
    image_url: Optional[str] = None
    description: Optional[str] = None

class Settings(BaseSettings):
    
    TELEGRAM_BOT_TOKEN: SecretStr = Field(None, env="TELEGRAM_BOT_TOKEN")
    
    GIGACHAT_CREDENTIALS: SecretStr = Field(None, env="GIGACHAT_CREDENTIALS")

    TAROT_DECK: List[TarotCard] = Field(
        default=[
            {
                "name": "0. Шут �",
                "key_words": "Новые начинания, спонтанность, невинность",
                "meaning": "Вот ты стоишь на краю обрыва. Ну чо, прыгаем? 🤪"
            }
        ],
        description="Колода карт Таро с их значениями"
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