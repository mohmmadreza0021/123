import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = int(os.getenv("API_ID"))  
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # آیدی عددی کانال (مثل -1001234567890)
BOT_USERNAME = os.getenv("BOT_USERNAME")  # یوزرنیم ربات بدون @
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # یوزرنیم کانال بدون @

bot = Client("media_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# چک کردن اینکه کاربر عضو کانال هست یا نه
def is_member(user_id):
    try:
        chat_member = bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

# دریافت مدیا و ایجاد لینک اختصاصی
@bot.on_message(filters.private & filters.media)
def send_media(client, message):
    if message.video or message.photo or message.document:
        file_id = (
            message.video.file_id if message.video else
            message.photo.file_id if message.photo else
            message.document.file_id
        )
        
        media_link = f"https://t.me/{BOT_USERNAME}?start={file_id}"
        message.reply_text(f"🔗 **لینک فایل شما:**\n{media_link}")

# دریافت مدیا از لینک و بررسی عضویت
@bot.on_message(filters.command("start") & filters.private)
def get_media(client, message):
    if len(message.command) > 1:
        file_id = message.command[1]
        user_id = message.from_user.id

        if is_member(user_id):
            bot.send_video(user_id, file_id)  # ارسال مدیا
        else:
            message.reply_text(
                "❌ **شما هنوز عضو کانال نیستید!**\nبرای دریافت فایل، ابتدا عضو شوید.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}")]
                ])
            )
    else:
        message.reply_text("سلام! لینک مدیا رو وارد کن تا دریافتش کنی.")

# اجرای ربات
bot.run()
