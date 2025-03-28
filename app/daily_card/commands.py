from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.filters import Command
from config import settings
import logging
import random

logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("daily_card"))
async def cmd_daily_card(message: Message):
    try:
        if not settings.TAROT_DECK:
            logger.error("Колода карт пуста!")
            await message.answer("Извините, колода карт недоступна.")
            return
        
        card = random.choice(settings.TAROT_DECK)
        
        content = (
            f"✨ Карта дня: {card.name} \n\n"
            f"Ключевые слова: {card.key_words} \n\n"
            f"Значение: {card.meaning} \n\n"
        )

        if card.music_urls:
            music_url = random.choice(card.music_urls)
            content += f"{music_url}"

        builder = MediaGroupBuilder(
            caption=content
        )

        image_urls = card.image_urls or settings.BASE_IMAGE_URLS
        image_url = random.choice(image_urls)

        builder.add_photo(image_url)

        await message.answer_media_group(builder.build())
        
            
    except Exception as e:
        logger.error(f"Ошибка в tarot_card: {e}")
        await message.answer("Произошла ошибка при выборе карты.")


def register_card_day_handlers(dp):
    dp.include_router(router)