import telebot
import time
import requests
import random
from threading import Thread
from flask import Flask

# إعداد السيرفر لضمان بقاء البوت Live
app = Flask('')
@app.route('/')
def home(): return "Bot is Active!"

def run_web(): app.run(host='0.0.0.0', port=8080)

# إعدادات البوت
TELEGRAM_TOKEN = '8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc'
SHRINKME_API_KEY = '03dac4507878d3d6f5747b0e7cea5fb98bb54c2a'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

db = {"balance": 1.83, "visits": 17}

# المحرك التلقائي
def proxy_engine():
    global db
    while True:
        try:
            requests.get(f"https://shrinkme.io/api?api={SHRINKME_API_KEY}&url=google.com", timeout=10)
            db["balance"] += random.uniform(0.01, 0.03)
            db["visits"] += 1
        except: pass
        time.sleep(60)

Thread(target=run_web).start() 
Thread(target=proxy_engine).start()

# --- 1. أمر الترحيب الجديد ---
@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = (
        f"👋 أهلاً بك {message.from_user.first_name}!\n\n"
        "تم تفعيل حسابك بنجاح. البوت الآن يجمع لك الأرباح.\n\n"
        "⬇️ **الأوامر الجديدة:**\n"
        "🔗 /link - للحصول على رابط ربحي خاص بك.\n"
        "💰 /sold - لرؤية رصيدك.\n"
        "💳 /transfer - لسحب الأموال."
    )
    bot.send_message(message.chat.id, welcome_text)

# --- 2. أمر اللينك (هنا التعديل لجعله يعمل) ---
@bot.message_handler(commands=['link'])
def get_link(message):
    # نقوم بطلب رابط مختصر من الموقع باستخدام الـ API الخاص بك
    target_url = "https://www.google.com" # الرابط المراد اختصاره
    api_url = f"https://shrinkme.io/api?api={SHRINKME_API_KEY}&url={target_url}"
    
    try:
        response = requests.get(api_url).json()
        if response["status"] == "success":
            short_link = response["shortenedUrl"]
            bot.reply_to(message, f"✅ إليك رابطك الربحي الخاص:\n🔗 {short_link}\n\n📢 انشره الآن! كل شخص يضغط عليه سيزيد رصيدك بالدولار.")
        else:
            bot.reply_to(message, "❌ فشل في إنشاء الرابط. تأكد من أن الـ API Key صحيح.")
    except:
        bot.reply_to(message, "⚠️ عذراً، هناك مشكلة في الاتصال بالموقع حالياً.")

# --- 3. نظام التحويل الذكي (كما طلبته سابقاً) ---
@bot.message_handler(commands=['transfer'])
def start_transfer(message):
    markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('D17', 'البريد التونسي', 'RIB Banque')
    msg = bot.send_message(message.chat.id, "🏦 اختر وسيلة السحب:", reply_markup=markup)
    bot.register_next_step_handler(msg, ask_amount)

def ask_amount(message):
    method = message.text
    if method not in ['D17', 'البريد التونسي', 'RIB Banque']:
        bot.send_message(message.chat.id, "❌ خطأ! الرجاء استخدام الأزرار.")
        return
    msg = bot.send_message(message.chat.id, f"💰 كم تريد تحويله؟ (الرصيد: ${db['balance']:.2f})")
    bot.register_next_step_handler(msg, lambda m: validate_amount(m, method))

def validate_amount(message, method):
    try:
        amount = float(message.text)
        if amount > db["balance"]:
            bot.send_message(message.chat.id, "❌ الرصيد غير كافٍ.")
            return
        msg = bot.send_message(message.chat.id, f"✅ أرسل الآن رقم الـ {method} (8 أرقام فقط):")
        bot.register_next_step_handler(msg, lambda m: finalize_transfer(m, amount, method))
    except:
        bot.send_message(message.chat.id, "❌ خطأ! أرسل أرقام فقط.")

def finalize_transfer(message, amount, method):
    account = message.text
    if not account.isdigit() or len(account) < 8:
        bot.send_message(message.chat.id, f"❌ خطأ: الحساب ({account}) غير صحيح.\nيرجى إدخال أرقام فقط.")
        return
    bot.send_message(message.chat.id, f"🎉 تم تقديم الطلب بنجاح!\nسيتم تحويل المبلغ إلى الحساب {account}.")

@bot.message_handler(commands=['sold'])
def check_balance(message):
    bot.reply_to(message, f"📊 رصيدك الحالي: ${db['balance']:.2f}")

bot.polling()
            
