import asyncio
from aiogram import Bot
from app.database import get_watchers_by_plate

async def notify_watchers(bot: Bot, plate: str, message_text: str):
    user_ids = get_watchers_by_plate(plate)
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, message_text)
        except Exception as e:
            print(f"[notify] Ошибка отправки пользователю {user_id}: {e}")

async def delayed_notification(bot: Bot, plate: str, brand: str):
    await asyncio.sleep(1800)  # 30 минут
    msg = f"🔔 Ваша машина ({plate} / {brand}) была эвакуирована. Вы можете посмотреть подробности в боте."
    await notify_watchers(bot, plate, msg)
