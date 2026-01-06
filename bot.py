import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os
import datetime
import pytz
import time

# ================= تنظیمات اختصاصی =================
API_TOKEN = '8583284736:AAF9PQFFVlwvu3d-wkSSa9IxjOPCq7PFDlA'
ADMIN_ID = 1129028195
CHANNEL_ID = -1003568177280
FOOTER_TEXT = "\n\n🆔 @azadiguilan \n\n🕊️آزادی خواهان دانشگاه گیلان"
# ======================================================

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id == ADMIN_ID:
        bot.reply_to(message, "✅ <b>مدیریت گرامی، سیستم فعال شد.</b>", parse_mode='HTML')
    else:
        bot.reply_to(message, "سلام! پیام را ارسال کنید تا به دست مدیریت برسد .")

@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'voice', 'video_note'])
def handle_all_messages(message):
    if message.chat.id == ADMIN_ID:
        return
import telebot
from telebot import types
from flask import Flask
from threading import Thread
import os
import datetime
import pytz
import time

# ================= تنظیمات اختصاصی =================
API_TOKEN = '8583284736:AAFZROjPTKIZFZdnKkMtAPs12a-lg3uMBBg'
ADMIN_ID = 1129028195
CHANNEL_ID = -1003568177280
FOOTER_TEXT = "\n\n🆔 @azadiguilan\n🕊️ آزادی خواهان دانشگاه گیلان"
# ======================================================

bot = telebot.TeleBot(API_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.id == ADMIN_ID:
        bot.reply_to(message, "✅ <b>مدیریت گرامی، سیستم فعال شد.</b>", parse_mode='HTML')
    else:
        bot.reply_to(message, "سلام! پیام را ارسال کنید تا به دست مدیریت برسد.")

@bot.message_handler(content_types=['text', 'photo', 'video', 'document', 'voice', 'video_note'])
def handle_all_messages(message):
    if message.chat.id == ADMIN_ID:
        return

    user = message.from_user
    tehran_tz = pytz.timezone('Asia/Tehran')
    now = datetime.datetime.now(tehran_tz)
    date_str = now.strftime('%Y/%m/%d')
    time_str = now.strftime('%H:%M:%S')
    chat_link = f"tg://user?id={user.id}"
    
    user_info = (
        f"📩 <b>گزارش جدید دریافت شد</b>\n"
        f"--------------------------\n"
        f"👤 <b>نام:</b> {user.first_name}\n"
        f"👤 <b>نام خانوادگی:</b> {user.last_name or 'ندارد'}\n"
        f"🆔 <b>آیدی عددی:</b> <code>{user.id}</code>\n"
        f"🆔 <b>یوزرنیم:</b> @{user.username or 'ندارد'}\n"
        f"🌐 <b>زبان:</b> {user.language_code or 'نامشخص'}\n"
        f"📅 <b>تاریخ:</b> {date_str}\n"
        f"⏰ <b>ساعت (تهران):</b> {time_str}\n\n"
        f"🔗 <a href='{chat_link}'>ورود مستقیم به پی‌وی کاربر</a>\n"
        f"--------------------------"
    )

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_app = types.InlineKeyboardButton("✅ تایید و انتشار", callback_data=f"app_{message.chat.id}_{message.message_id}")
    btn_rej = types.InlineKeyboardButton("❌ رد کردن و حذف", callback_data=f"rej_{message.chat.id}_{message.message_id}")
    markup.add(btn_app, btn_rej)

    try:
        bot.send_message(ADMIN_ID, user_info, parse_mode='HTML')
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        bot.send_message(ADMIN_ID, "📝 <b>مدیریت:</b> برای پیام بالا چه تصمیمی می‌گیرید؟", reply_markup=markup, parse_mode='HTML')
        bot.reply_to(message, "✅ پیام با موفقیت برای مدیریت ارسال شد.")
    except Exception as e:
        print(f"Error sending to admin: {e}")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    data = call.data.split('_')
    action, user_chat_id, msg_id = data[0], data[1], data[2]

    if action == "app":
        try:
            # فوروارد موقت برای دسترسی به محتوا
            temp_msg = bot.forward_message(ADMIN_ID, user_chat_id, msg_id)
            
            if temp_msg.content_type == 'text':
                bot.send_message(CHANNEL_ID, temp_msg.text + FOOTER_TEXT)
            elif temp_msg.content_type == 'photo':
                caption = (temp_msg.caption or "") + FOOTER_TEXT
                bot.send_photo(CHANNEL_ID, temp_msg.photo[-1].file_id, caption=caption)
            elif temp_msg.content_type == 'video':
                caption = (temp_msg.caption or "") + FOOTER_TEXT
                bot.send_video(CHANNEL_ID, temp_msg.video.file_id, caption=caption)
            else:
                bot.copy_message(CHANNEL_ID, user_chat_id, msg_id, caption=FOOTER_TEXT)

            bot.delete_message(ADMIN_ID, temp_msg.message_id)
            bot.answer_callback_query(call.id, "در کانال منتشر شد ✅")
            # اصلاح آیدی نمایش داده شده به مدیریت
            bot.edit_message_text(f"✅ <b>این گزارش در @azadiguilan منتشر شد.</b>", 
                                 chat_id=ADMIN_ID, message_id=call.message.message_id, parse_mode='HTML')
        except Exception as e:
            bot.answer_callback_query(call.id, "خطا در ارسال!")
            print(f"Final Send Error: {e}")
            
    elif action == "rej":
        try:
            bot.edit_message_text("❌ <b>این گزارش رد شد.</b>", 
                                 chat_id=ADMIN_ID, message_id=call.message.message_id, parse_mode='HTML')
            bot.answer_callback_query(call.id, "رد شد.")
        except: pass

if __name__ == "__main__":
    Thread(target=run_flask, daemon=True).start()
    
    # بخش حیاتی برای جلوگیری از خطای Conflict 409
    bot.remove_webhook()
    time.sleep(2) 
    
    print("--- 3-Step Full Bot is Online ---")
    bot.infinity_polling(timeout=20, skip_pending=True)
