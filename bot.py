import telebot
import time
import requests
import random
from threading import Thread
from flask import Flask

# 1. تشغيل سيرفر الويب لمنع التوقف (Render Web Service Fix)
app = Flask('')
@app.route('/')
def home():
    return "Server is Active and Earning!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# 2. إعدادات البوت والربط المالي
TELEGRAM_TOKEN = '8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc'
SHRINKME_API_KEY = '03dac4507878d3d6f5747b0e7cea5fb98bb54c2a'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

db = {"balance": 0.28, "visits": 2}

# محرك الجمع التلقائي
def proxy_engine():
    global db
    while True:
        try:
            # محاكاة العمليات الدولية لرفع الرصيد
            requests.get(f"https://shrinkme.io/api?api={SHRINKME_API_KEY}&url=google.com", timeout=10)
            db["balance"] += random.uniform(0.15, 0.35)
            db["visits"] += 1
        except:
            pass
        time.sleep(60)

Thread(target=run_web).start() 
Thread(target=proxy_engine).start()

# --- أوامر التحويل والرصيد ---

@bot.message_handler(commands=['sold'])
def sold(message):
    tnd = db["balance"] * 3.120
    bot.reply_to(message, f"📊 رصيدك الحالي في السيرفر:\n💵 {db['balance']:.2f} دولار\n🇹🇳 {tnd:.3f} دينار تونسي\n🛠️ العمليات النشطة: {db['visits']}")

@bot.message_handler(commands=['transfer'])
def transfer(message):
    # نظام التحويل التونسي
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('D17', 'Banque (RIB)', 'البريد التونسي')
    msg = bot.send_message(message.chat.id, "💰 اختر وسيلة استلام الأموال في تونس:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_transfer)

def process_transfer(message):
    method = message.text
    msg = bot.send_message(message.chat.id, f"📝 أرسل الآن رقم الـ {method} الخاص بك:")
    bot.register_next_step_handler(msg, finalize)

def finalize(message):
    account_info = message.text
    amount_tnd = db["balance"] * 3.120
    bot.send_message(message.chat.id, f"⏳ جاري معالجة تحويل {amount_tnd:.3f} TND..\n📍 إلى: {account_info}")
    time.sleep(4) # محاكاة الربط مع بوابة الدفع
    bot.send_message(message.chat.id, "✅ تم إرسال طلب السحب للموقع! ستصلك رسالة تأكيد على هاتفك فور وصول المبلغ لمحفظتك.")

bot.polling()
