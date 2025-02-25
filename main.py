import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # آیدی عددی کانال (مثلاً -1001234567890)
BOT_USERNAME = os.getenv("BOT_USERNAME")  # یوزرنیم ربات بدون @
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # یوزرنیم کانال بدون @
OWNER_ID = int(os.getenv("OWNER_ID"))  # آی‌دی عددی مالک ربات

bot = Client("media_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# چک کردن اینکه کاربر ادمین یا مالک هست
async def is_admin_or_owner(user_id):
    if user_id == OWNER_ID:
        return True
    try:
        chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ["administrator", "creator"]
    except:
        return False

# دریافت مدیا و ایجاد لینک اختصاصی (برای ادمین/مالک)
@bot.on_message(filters.private & filters.media)
async def send_media(client, message):
    if await is_admin_or_owner(message.from_user.id):  # فقط ادمین و مالک می‌توانند فایل ارسال کنند
        if message.video or message.photo or message.document:
            file_id = (
                message.video.file_id if message.video else
                message.photo.file_id if message.photo else
                message.document.file_id
            )

            # ساخت لینک اختصاصی برای فایل
            media_link = f"https://t.me/{BOT_USERNAME}?start={file_id}"
            await message.reply_text(f"🔗 **لینک فایل شما:**\n{media_link}")
    else:
        await message.reply_text("❌ فقط ادمین و مالک می‌توانند فایل ارسال کنند.")

# بررسی عضویت کاربر در کانال و ارسال فایل
@bot.on_message(filters.command("start") & filters.private)
async def get_media(client, message):
    if len(message.command) > 1:
        file_id = message.command[1]
        user_id = message.from_user.id

        # بررسی عضویت کاربر در کانال
        if await is_member(user_id):  # فرض بر اینه که شما قبلاً تابع is_member رو درست نوشتید
            try:
                # ارسال فایل به کاربر
                await bot.send_cached_media(user_id, file_id)
            except Exception as e:
                await message.reply_text(f"❌ خطا در ارسال فایل: {e}")
        else:
            await message.reply_text(
                "❌ **شما هنوز عضو کانال نیستید!**\nبرای دریافت فایل، ابتدا عضو شوید.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME}")]
                ])
            )
    else:
        await message.reply_text("🎉 به ربات خوش آمدید! لطفاً لینک مدیا رو وارد کن تا دریافتش کنی.")

# چک کردن عضویت در کانال
async def is_member(user_id):
    try:
        chat_member = await bot.get_chat_member(CHANNEL_ID, user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

# اجرای ربات با سیستم اتورستارت
async def main():
    while True:
        try:
            print("✅ ربات با موفقیت راه‌اندازی شد.")
            await bot.start()
            await asyncio.Event().wait()  # جلوگیری از بسته شدن برنامه
        except Exception as e:
            print(f"⚠️ خطا رخ داد: {e}")
            await asyncio.sleep(5)  # ۵ ثانیه صبر کن و دوباره اجرا کن

# اجرای اسکریپت اصلی
if __name__ == "__main__":
    asyncio.run(main())
