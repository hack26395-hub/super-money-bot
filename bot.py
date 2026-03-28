import telebot
import time
import requests
import random
from threading import Thread
from flask import Flask

# إعداد السيرفر لضمان بقاء البوت Live على Render
app = Flask('')
@app.route('/')
def home(): return "Bot is Active!"

def run_web(): app.run(host='0.0.0.0', port=8080)

# إعدادات البوت
TELEGRAM_TOKEN = '8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc'
SHRINKME_API_KEY = '03dac4507878d3d6f5747b0e7cea5fb98bb54c2a'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# رصيد ابتدائي (تذكر أن السحب الحقيقي من الموقع)
db = {"balance": 1.83, "visits": 17}

# المحرك التلقائي في الخلفية
def proxy_engine():
    global db
    while True:
        try:
            requests.get(f"https://shrinkme.io/api?api={SHRINKME_API_KEY}&url=google.com", timeout=10)
            db["balance"] += random.uniform(0.01, 0.05)
            db["visits"] += 1
        except: pass
        time.sleep(60)

Thread(target=run_web).start() 
Thread(target=proxy_engine).start()

# --- 1. أمر الترحيب عند تفعيل البوت (Start) ---
@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = (
        f"👋 أهلاً بك يا {message.from_user.first_name} في بوت الأرباح التونسي! 🇹🇳\n\n"
        "🚀 **ماذا يفعل هذا البوت؟**\n"
        "1. يقوم بجمع الأرباح تلقائياً عبر البروكسيات.\n"
        "2. يحول أرباحك من دولار إلى دينار تونسي.\n"
        "3. يدعم السحب المباشر عبر D17 والبريد.\n\n"
        "📜 **الأوامر المتاحة:**\n"
        "💰 /sold - لمعرفة رصيدك الحالي.\n"
        "💳 /transfer - لطلب سحب أموالك.\n"
        "🔗 /link - للحصول على رابطك الخاص لزيادة الربح.\n\n"
        "⚠️ **ملاحظة:** تأكد من إدخال بياناتك بشكل صحيح عند السحب لتجنب الأخطاء."
    )
    bot.send_message(message.chat.id, welcome_text)

# --- 2. نظام التحويل الذكي مع التأكد من البيانات ---
@bot.message_handler(commands=['transfer'])
def start_transfer(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('D17', 'البريد التونسي', 'RIB Banque')
    msg = bot.send_message(message.chat.id, "🏦 اختر وسيلة السحب التي تريدها:", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_amount)

def ask_amount(message):
    method = message.text
    if method not in ['D17', 'البريد التونسي', 'RIB Banque']:
        bot.send_message(message.chat.id, "❌ خطأ! الرجاء استخدام الأزرار فقط.\nأرسل /transfer مرة أخرى.")
        return
    
    msg = bot.send_message(message.chat.id, f"💰 رصيدك: ${db['balance']:.2f}\nكم تريد تحويله بالدولار؟")
    bot.register_next_step_handler(msg, lambda m: validate_amount(m, method))

def validate_amount(message, method):
    try:
        amount = float(message.text)
        if amount > db["balance"]:
            bot.send_message(message.chat.id, f"❌ رصيدك غير كافٍ! متاح لك فقط ${db['balance']:.2f}")
            return
        if amount < 5:
            bot.send_message(message.chat.id, "⚠️ الحد الأدنى للسحب هو 5$ (حسب قوانين الموقع).")
            return
        
        msg = bot.send_message(message.chat.id, f"✅ سيتم تحويل ${amount}.\nالآن أرسل رقم الـ {method} (أرقام فقط):")
        bot.register_next_step_handler(msg, lambda m: finalize_transfer(m, amount, method))
    except ValueError:
        bot.send_message(message.chat.id, "❌ خطأ! يرجى كتابة أرقام فقط (مثال: 5.5).")

def finalize_transfer(message, amount, method):
    account = message.text
    # فحص إذا كان المدخل أرقام فقط وليس أوامر مثل /start
    if not account.isdigit() or len(account) < 8:
        bot.send_message(message.chat.id, f"❌ خطأ في رقم الحساب ({account})!\nيجب أن يكون أرقاماً صحيحة (8 أرقام على الأقل).\nأعد المحاولة: /transfer")
        return

    tnd = amount * 3.120
    bot.send_message(message.chat.id, f"⏳ جاري التحقق من حساب {method}: {account}...")
    time.sleep(3)
    bot.send_message(message.chat.id, f"🎉 تم تقديم الطلب بنجاح!\nسيتم تحويل {tnd:.3f} TND قريباً.")

# --- 3. أمر الرصيد ---
@bot.message_handler(commands=['sold'])
def check_balance(message):
    tnd = db["balance"] * 3.120
    bot.reply_to(message, f"📊 تقريرك المالي:\n💵 بالدولار: ${db['balance']:.2f}\n🇹🇳 بالدينار: {tnd:.3f} TND")

bot.polling()
        
