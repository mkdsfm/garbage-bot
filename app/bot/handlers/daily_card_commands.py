from typing import List
from aiogram import Router, F
from aiogram.types import Message, FSInputFile  
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.filters import Command
from app.tarot_daily_card.manager import get_card
from config import settings
import logging
import random

logger = logging.getLogger(__name__)

router = Router()

@router.message(Command("daily_card"))
async def cmd_daily_card(message: Message):
    if not settings.TAROT_DECK:
            logger.error("Колода карт пуста!")
            await message.answer("Извините, колода карт недоступна.")
            return
    
    card = get_card(settings.TAROT_DECK)

    generator = settings.TAROT_DAILY_CARD_GENERATOR_CLASS
    meaning = await generator.generate_meaning_from_name_async(card.name)
    
    try:
        content = f"{meaning}\n\n"

        if card.music_url:
            content += f"{card.music_url}\n\n"

        image_url = card.image_url or random.choice(settings.BASE_IMAGE_URLS)
        if image_url.startswith("./images/"):
             image_url = FSInputFile(image_url)
             
        await message.answer_photo(
            photo=image_url,
            caption=content,
            parse_mode="HTML"
        )
            
    except Exception as e:
        logger.error(f"Ошибка в tarot_card {card} : {e}")
        await message.answer("Произошла ошибка при выборе карты.")

@router.message(Command("daily_card_angry"))
async def cmd_daily_card(message: Message):
    if not settings.TAROT_DECK:
            logger.error("Колода карт пуста!")
            await message.answer("Извините, колода карт недоступна.")
            return
    
    card = get_card(settings.TAROT_DECK)
    
    try:
        content = (
            f"✨ Карта дня: {card.name} \n\n"
            f"Ключевые слова: {card.key_words} \n\n"
            f"Значение: {card.meaning} \n\n"
        )

        if card.music_url:
            content += f"{card.music_url}\n\n"

        builder = MediaGroupBuilder(
            caption=content
        )

        image_url = card.image_url or random.choice(settings.BASE_IMAGE_URLS)
        if image_url.startswith("./images/"):
             image_url = FSInputFile(image_url)
             
        builder.add_photo(image_url)

        await message.answer_media_group(builder.build())
        
            
    except Exception as e:
        logger.error(f"Ошибка в tarot_card {card} : {e}")
        await message.answer("Произошла ошибка при выборе карты.")


def register_card_day_handlers(dp):
    dp.include_router(router)