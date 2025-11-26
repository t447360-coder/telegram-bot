import os
import yt_dlp
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN environment variable not set.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send any YouTube link. I will download 720p MP4 for you.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    await update.message.reply_text("⏳ Downloading...")

    ydl_opts = {
        "format": "bestvideo[height<=720]+bestaudio/best",
        "outtmpl": "video.mp4",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(video=open("video.mp4", "rb"))

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

def main():
    bot = Bot(token=TOKEN)
    try:
        bot.delete_webhook()
    except:
        pass

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
