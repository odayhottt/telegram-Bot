from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio
import os
import logging

# إعداد لوقات واضحة
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Token من Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")

# إعداد البوت مع ParseMode
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# معرف القناة المركزية
SOURCE_CHANNEL_ID = -1002555988773

# معرفات القنوات الفرعية
TARGET_CHANNEL_IDS = [
    -1002491559178,
    -1002478792332,
    -1002273877338,
    -1002654785890,
    -1002354952968
]

# التقاط جميع منشورات القناة المركزية (عادية + محوّلة)
@dp.channel_post(F.chat.id == SOURCE_CHANNEL_ID)
async def forward_channel_post(message: Message):
    logger.info(f"📢 استقبلنا منشور جديد في القناة المركزية: {message.message_id}")

    for target_id in TARGET_CHANNEL_IDS:
        try:
            # نص عادي
            if message.text:
                await bot.send_message(chat_id=target_id, text=message.text)

            # صورة مع كابتشن
            elif message.caption and message.photo:
                await bot.send_photo(chat_id=target_id, photo=message.photo[-1].file_id, caption=message.caption)
            
            # صورة بدون كابتشن
            elif message.photo:
                await bot.send_photo(chat_id=target_id, photo=message.photo[-1].file_id)

            # فيديو مع كابتشن
            elif message.caption and message.video:
                await bot.send_video(chat_id=target_id, video=message.video.file_id, caption=message.caption)

            # فيديو بدون كابتشن
            elif message.video:
                await bot.send_video(chat_id=target_id, video=message.video.file_id)

            # رسالة محوّلة
            elif message.forward_from or message.forward_from_chat:
                if message.text:
                    await bot.send_message(chat_id=target_id, text=message.text)
                elif message.photo:
                    await bot.send_photo(chat_id=target_id, photo=message.photo[-1].file_id)
                elif message.video:
                    await bot.send_video(chat_id=target_id, video=message.video.file_id)

            logger.info(f"✅ تم النشر بنجاح إلى القناة: {target_id}")

        except Exception as e:
            logger.error(f"⚠️ فشل في النشر إلى {target_id}: {e}")

# حلقة Auto polling فيها Retry لو صار Conflict
async def polling_loop():
    while True:
        try:
            logger.info("🚀 البوت بدأ الآن - Start polling...")
            await dp.start_polling(bot)
        except Exception as e:
            logger.error(f"❌ خطأ في polling: {e}")
            logger.info("🔄 إعادة محاولة الاتصال بعد 5 ثواني...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(polling_loop())