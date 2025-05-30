import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNEL_ID = -1002555988773
TARGET_CHANNEL_IDS = [
    -1002491559178,
    -1002478792332,
    -1002273877338,
    -1002654785890,
    -1002354952968
]

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    if message.chat.id == SOURCE_CHANNEL_ID:
        for target_id in TARGET_CHANNEL_IDS:
            try:
                if message.text:
                    await context.bot.send_message(chat_id=target_id, text=message.text)
                elif message.caption and message.photo:
                    await context.bot.send_photo(chat_id=target_id, photo=message.photo[-1].file_id, caption=message.caption)
                elif message.caption and message.video:
                    await context.bot.send_video(chat_id=target_id, video=message.video.file_id, caption=message.caption)
            except Exception as e:
                print(f"⚠️ فشل في النشر إلى {target_id}: {e}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, forward_message))
app.run_polling()