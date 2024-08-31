import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import imageio_ffmpeg as ffmpeg
from background import keep_alive 

keep_alive()

# Получаем путь к ffmpeg
ffmpeg_path = ffmpeg.get_ffmpeg_exe()

# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на токен вашего бота, полученный от BotFather
TELEGRAM_BOT_TOKEN = '7419412806:AAF7lzBbGzlitQxltaBy88Ny0gycTA7cZNc'

async def download_soundcloud_track(url: str, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': ffmpeg_path,  # Указываем путь к ffmpeg, установленному через imageio
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            mp3_filename = os.path.splitext(filename)[0] + ".mp3"

            # Отправка файла пользователю
            await context.bot.send_audio(chat_id=chat_id, audio=open(mp3_filename, 'rb'))

            # Удаление файла после отправки
            os.remove(mp3_filename)

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"Ошибка при скачивании трека: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Отправьте мне ссылку на трек SoundCloud, и я загружу его для вас.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    chat_id = update.message.chat_id

    if "soundcloud.com" in url:
        await update.message.reply_text('Скачиваю трек...')
        await download_soundcloud_track(url, chat_id, context)
    else:
        await update.message.reply_text('Пожалуйста, отправьте действительную ссылку на трек SoundCloud.')

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == '__main__':
    main()
