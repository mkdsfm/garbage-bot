from pydantic import BaseModel


from typing import List, Optional


class TarotCard(BaseModel):
    name: str
    key_words: str
    meaning: str
    image_urls: Optional[List[str]] = None
    alter_meaning: Optional[List[str]] = None
    music_urls: Optional[List[str]] = None