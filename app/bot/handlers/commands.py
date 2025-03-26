from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command


router = Router()


# Хендлер команды /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я телеграм бот. Напиши /help для списка команд.")

# Хендлер команды /help
@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = """
    Доступные команды:
    /start - начать работу с ботом
    /help - получить справку
    /day_card - получить карту дня
    """
    await message.answer(help_text)


def register_commands_handlers(dp):
    dp.include_router(router)