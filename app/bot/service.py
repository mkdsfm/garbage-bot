import logging
from aiogram import Bot, Dispatcher
from config import settings
import app.daily_card.commands

logger = logging.getLogger(__name__)

class BotService:
    def __init__(
        self
    ):
        self.bot = Bot(
            token=settings.TELEGRAM_BOT_TOKEN.get_secret_value()
        )
        self.dp = Dispatcher()
        
        self._register_handlers()
    
    
    def _register_handlers(self):
        from .handlers import commands
        
        # Регистрируем хэндлеры
        commands.register_commands_handlers(self.dp)
        app.daily_card.commands.register_card_day_handlers(self.dp)
        
        logger.info("Bot handlers registered")
    
    
    async def start(self):
        logger.info("Starting bot in polling mode")
        await self.dp.start_polling(self.bot)
        