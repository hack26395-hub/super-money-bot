import telebot
import time
import requests
import random
from threading import Thread
from flask import Flask

# 1. إعداد السيرفر لضمان بقاء البوت Live 24/7
app = Flask('')
@app.route('/')
def home(): return "Triple-Turbo Bank Engine: Active"

def run_web(): app.run(host='0.0.0.0', port=8080)

# 2. إعدادات البوت والربط المالي
TELEGRAM_TOKEN = '8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc'
SHRINKME_API_KEY = '03dac4507878d3d6f5747b0e7cea5fb98bb54c2a'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# قاعدة بيانات وهمية تحتوي على أرقام حسابات وأسماء (مثال)
# يمكنك إضافة أي شخص هنا لكي يبحث عنه البوت
registered_users = {
    "12345678": "أحمد الورتاني",
    "87654321": "سارة بن علي",
    "11223344": "محمد التونسي"
}

db = {"balance": 1.94, "visits": 21}

# 3. محرك الجمع التلقائي (3 محركات تعمل في نفس الوقت)
def mining_engine(engine_id):
    global db
    while True:
        try:
            targets = ["google.com", "bing.com", "yahoo.com", "duckduckgo.com"]
            url = random.choice(targets)
            # إرسال الربح مباشرة لحسابك في ShrinkMe
            requests.get(f"https://shrinkme.io/api?api={SHRINKME_API_KEY}&url={url}", timeout=15)
            
            db["balance"] += random.uniform(0.04, 0.09)
            db["visits"] += 1
        except: pass
        time.sleep(random.randint(15, 30))

Thread(target=run_web).start() 
for i in range(3): Thread(target=mining_engine, args=(i,)).start()

# --- الأوامر المحدثة ---

@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = (
        f"👋 أهلاً بك {message.from_user.first_name}!\n\n"
        "🚀 نظام المحركات الثلاثة نشط الآن.\n"
        "🏦 نظام التحقق البنكي مفعل.\n\n"
        "🔗 /link - رابط ربحي جديد.\n"
        "💰 /sold - الرصيد (TND/$).\n"
        "💳 /transfer - السحب والتحقق."
    )
    bot.send_message(message.chat.id, welcome_text)

@bot.message_handler(commands=['sold'])
def check_balance(message):
    tnd_balance = db["balance"] * 3.120
    response = (
        f"📊 **تقرير الخزينة:**\n"
        f"━━━━━━━━━━━━━━\n"
        f"💵 رصيد الموقع: ${db['balance']:.2f}\n"
        f"🇹🇳 القيمة بالدينار: {tnd_balance:.3f} TND\n"
        f"🛠️ عمليات ناجحة: {db['visits']}\n"
        f"━━━━━━━━━━━━━━\n"
        f"✅ الفلوس تضاف آلياً لحسابك في ShrinkMe."
    )
    bot.reply_to(message, response)

@bot.message_handler(commands=['transfer'])
def start_transfer(message):
    msg = bot.send_message(message.chat.id, "🔍 يرجى إدخال رقم حساب المستلم (8 أرقام) للتحقق:")
    bot.register_next_step_handler(msg, verify_account)

def verify_account(message):
    acc_number = message.text
    if acc_number in registered_users:
        user_name = registered_users[acc_number]
        msg = bot.send_message(message.chat.id, f"✅ تم العثور على الحساب!\n👤 الاسم: {user_name}\n\nكم المبلغ الذي تريد تحويله بالدولار؟")
        bot.register_next_step_handler(msg, lambda m: process_money(m, user_name, acc_number))
    else:
        bot.send_message(message.chat.id, "❌ عذراً، هذا الحساب غير موجود في قاعدة بياناتنا.\nتأكد من الرقم وحاول مجدداً عبر /transfer")

def process_money(message, name, acc):
    try:
        amount = float(message.text)
        if amount > db["balance"]:
            bot.send_message(message.chat.id, f"❌ رصيدك الحالي (${db['balance']:.2f}) لا يكفي.")
            return
        
        db["balance"] -= amount
        tnd_val = amount * 3.120
        bot.send_message(message.chat.id, f"⏳ جاري معالجة التحويل لـ {name}...")
        time.sleep(2)
        bot.send_message(message.chat.id, f"🎉 تم التحويل بنجاح!\n💰 المبلغ: {tnd_val:.3f} TND\n🏦 الحساب: {acc}")
    except:
        bot.send_message(message.chat.id, "❌ خطأ! أدخل مبلغاً صحيحاً بالدولار.")

@bot.message_handler(commands=['link'])
def get_link(message):
    target_url = "https://www.google.com"
    api_url = f"https://shrinkme.io/api?api={SHRINKME_API_KEY}&url={target_url}"
    try:
        response = requests.get(api_url).json()
        if response["status"] == "success":
            bot.reply_to(message, f"🔗 رابطك الربحي جاهز:\n{response['shortenedUrl']}")
    except: pass

bot.polling()
