import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

TOKEN = "7767854602:AAFfzfY9wYGJN6kBiKyv0QMXgaTLJEh4-p0"

async def start(update: Update, context):
    await update.message.reply_text("👋 Send any YouTube link. I will download it in 720p MP4.")

async def download_video(update: Update, context):
    url = update.message.text

    await update.message.reply_text("⏳ Downloading... Please wait...")

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

        await update.message.reply_video("video.mp4")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()

if __name__ == "__main__":
    main()
