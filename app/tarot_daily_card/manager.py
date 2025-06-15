import random
from typing import List, Optional

from config import TarotCard

class Card:
    name: str
    key_words: str
    meaning: str
    image_url: Optional[str] = None
    music_url: Optional[str] = None

def get_card(tarot_list: List[TarotCard]) -> Card:
    card = random.choice(tarot_list)

    result = Card()
    result.name = card.name
    result.key_words = card.key_words
    result.image_url = random.choice(card.image_urls) if card.image_urls else None
    result.music_url = random.choice(card.music_urls) if card.music_urls else None
    result.meaning = card.meaning

    if card.alter_meaning:
            alter_meaning = random.choice(card.alter_meaning)
            result.meaning += f"{alter_meaning}\n\n"

    return result


from abc import ABC, abstractmethod

class ITarotDailyCardGenerator(ABC):
    @abstractmethod
    async def generate_meaning_from_name_async(self, name_card: str) -> str:
        pass