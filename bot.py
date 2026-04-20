import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    await update.message.reply_text("⏳ Скачиваю...")

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            if "youtube.com" in text or "youtu.be" in text:
                info = ydl.extract_info(text, download=True)
            else:
                info = ydl.extract_info(f"ytsearch:{text}", download=True)
                info = info['entries'][0]

            filename = ydl.prepare_filename(info)

        await update.message.reply_audio(audio=open(filename, 'rb'))

        os.remove(filename)

    except Exception:
        await update.message.reply_text("❌ Ошибка")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
