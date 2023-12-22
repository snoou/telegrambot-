import telebot
from pytube import YouTube
import os

TOKEN = "توکن"
bot = telebot.TeleBot(TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

# تعریف تابع دانلود که پیام مناسب را به کاربر ارسال می‌کند
def download_and_send(url, chat_id):
    try:
        bot.send_message(chat_id , 'شروع دانلود...')
        # دانلود ویدئو
        yt = YouTube(url)
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        video_file_path = video_stream.download()
        
        # ارسال پیام موفقیت به کاربر
        bot.send_message(chat_id, "ویدئو با موفقیت دانلود شد. در حال آماده‌سازی برای ارسال...")

        # ارسال ویدئو به کاربر
        video_file = open(video_file_path, 'rb')
        bot.send_video(chat_id, video_file)
        video_file.close()

        # حذف فایل دانلود شده از سیستم
        os.remove(video_file_path)
    except Exception as e:
        # در صورت بروز خطا، ارسال پیام خطا به کاربر
        bot.send_message(chat_id, f"متاسفانه خطایی در دانلود ویدئو رخ داد: {e}")

@bot.message_handler(commands=['youtube'])
def ask_for_youtube_url(message):
    # این پیام از کاربر درخواست URL می‌کند.
    msg = bot.reply_to(message, "لطفا URL یوتیوب را وارد کنید:")
    bot.register_next_step_handler(msg, receive_youtube_url)

def receive_youtube_url(message):
    # این تابع URL دریافتی را پردازش می‌کند.
    chat_id = message.chat.id
    url = message.text
    # فرض بر این است که URL معتبر است. در عمل باید چک شود که آیا یک URL یوتیوب معتبر است.
    download_and_send(url, chat_id)
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "دانلود از یوتیوب با /youtube")

bot.polling(none_stop=True)
