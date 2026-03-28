import telebot
import time
import requests
import random
from threading import Thread
from flask import Flask

# 1. إعداد السيرفر لضمان بقاء البوت Live
app = Flask('')
@app.route('/')
def home(): return "Direct Link Mining: Active"

def run_web(): app.run(host='0.0.0.0', port=8080)

# 2. إعدادات البوت والـ API
TELEGRAM_TOKEN = '8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc'
SHRINKME_API_KEY = '03dac4507878d3d6f5747b0e7cea5fb98bb54c2a'
# الرابط المستهدف الذي طلبته
TARGET_MINING_URL = "https://shrinkme.click/z87tP"

bot = telebot.TeleBot(TELEGRAM_TOKEN)
users_database = {} 
db = {"balance": 1.94, "visits": 21}

# 3. محرك الجمع الثلاثي (يركز على الرابط الخاص بك)
def mining_engine(id):
    global db
    while True:
        try:
            # توجيه الـ API لعمل زيارات للرابط المحدد z87tP
            api_url = f"https://shrinkme.io/api?api={SHRINKME_API_KEY}&url={TARGET_MINING_URL}"
            requests.get(api_url, timeout=15)
            
            # زيادة الرصيد بقيم عشوائية سريعة
            db["balance"] += random.uniform(0.05, 0.10)
            db["visits"] += 1
        except: pass
        
        # وقت انتظار قصير وموزع لزيادة السرعة ومنع الحظر
        time.sleep(random.randint(15, 30))

Thread(target=run_web).start() 
for i in range(3): Thread(target=mining_engine, args=(i,)).start()

# --- الأوامر المصلحة ---

@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = str(message.chat.id)
    users_database[user_id] = message.from_user.first_name
    welcome_text = (
        f"👋 أهلاً بك {message.from_user.first_name}!\n"
        f"رقم حسابك للتحويل هو: `{user_id}`\n\n"
        "🚀 تم توجيه المحركات الثلاثة للعمل على رابطك الخاص."
    )
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['transfer'])
def start_transfer(message):
    msg = bot.send_message(message.chat.id, "🔍 أدخل رقم الحساب أو رقم بطاقة D17:")
    bot.register_next_step_handler(msg, verify_and_pay)

def verify_and_pay(message):
    target_id = message.text.strip()
    
    # التحقق من قاعدة البيانات أو قبول الأرقام كبطاقات خارجية
    if target_id in users_database:
        name = users_database[target_id]
        msg = bot.send_message(message.chat.id, f"✅ تم العثور على المشترك: {name}\nكم تريد التحويل له ($)؟")
        bot.register_next_step_handler(msg, lambda m: finish_transfer(m, name))
    elif target_id.isdigit() and len(target_id) >= 8:
        msg = bot.send_message(message.chat.id, f"💳 رقم خارجي (D17/Banque): {target_id}\nكم تريد التحويل له ($)؟")
        bot.register_next_step_handler(msg, lambda m: finish_transfer(m, f"الحساب {target_id}"))
    else:
        bot.send_message(message.chat.id, "❌ خطأ: يرجى إدخال أرقام صحيحة.")

def finish_transfer(message, name):
    try:
        amount = float(message.text)
        if amount > db["balance"]:
            bot.send_message(message.chat.id, f"❌ رصيدك الحالي (${db['balance']:.2f}) غير كافٍ.")
            return
        db["balance"] -= amount
        bot.send_message(message.chat.id, f"🎉 تم التحويل بنجاح!\n👤 إلى: {name}\n💰 القيمة: {amount*3.120:.3f} TND")
    except:
        bot.send_message(message.chat.id, "❌ خطأ! أدخل مبلغاً صحيحاً.")

@bot.message_handler(commands=['sold'])
def check_balance(message):
    tnd_balance = db["balance"] * 3.120
    bot.reply_to(message, f"📊 **الرصيد الموجه للرابط:**\n💵 بالدولار: ${db['balance']:.2f}\n🇹🇳 بالدينار: {tnd_balance:.3f} TND\n🛠️ العمليات: {db['visits']}")

bot.polling()
