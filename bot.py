import os
import yt_dlp
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

# TOKEN from Railway Environment
TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN not found in environment")

async def start(update: Update, context):
    await update.message.reply_text("👋 Send any YouTube link to download")

async def download_video(update: Update, context):
    url = update.message.text.strip()
    await update.message.reply_text("⏳ Downloading... Please wait...")

    opts = {
        "format": "bestvideo[height<=720]+bestaudio/best",
        "outtmpl": "video.mp4",
        "quiet": True,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        await update.message.reply_video("video.mp4")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

app.run_polling()
