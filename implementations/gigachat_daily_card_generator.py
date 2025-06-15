import logging
import os
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from app.tarot_daily_card.manager import ITarotDailyCardGenerator
logger = logging.getLogger(__name__)

class GigaChatTarotDailyCardGenerator(ITarotDailyCardGenerator):
    def __init__(self, credentials, scope, model, ca_bundle_file):
        self.giga = GigaChat(
            credentials=credentials,
            scope=scope,
            model=model,
            ca_bundle_file=ca_bundle_file
        )
        self.SYSTEM_PROMPT = """Ты — генератор кратких описаний карт Таро для ежедневных раскладов. При получении названия карты и позиции (прямая/перевернутая) выдавай краткое описание карты с основными значениями, интерпретацией на сегодняшний день и подходящими эмодзи.
Пример ввода: Императрица (прямое положение)
Пример ответа:
🃏 <b>Карта</b> : Императрица (прямое положение) 🌿👩‍🍼✨
🌟 <b>Основные значения</b> : изобилие, забота, творчество, связь с природой.
📅 <b>Интерпретация на сегодня</b> : день благоприятен для заботы о себе и близких 💗, проявления креативности 🎨 или занятия любимыми делами. Возможны небольшие бытовые радости или ощущение уюта 🕯️🍵."""


    async def generate_meaning_from_name_async(self, name: str) -> str:

        logger.info(f"system prompt: {self.SYSTEM_PROMPT}")

        payload = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content=self.SYSTEM_PROMPT
                ),
                Messages(
                    role=MessagesRole.USER,
                    content=name
                )
            ]
        )

        response = self.giga.chat(payload)
        content = response.choices[0].message.content
        logger.info(f"content: {content}")

        return content