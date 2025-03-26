import asyncio
import logging
from modules.bot.service import BotService

logger = logging.getLogger(__name__)

async def main():
    logger.info("Start tarot bot")

    bot_service = BotService()
    await bot_service.start()


if __name__ == "__main__":
    asyncio.run(main())