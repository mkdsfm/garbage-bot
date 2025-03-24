import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from datetime import datetime
import json


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())