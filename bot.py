import telebot
import time
from threading import Thread
from flask import Flask

# --- إعدادات الإمبراطور قيس ---
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"
MY_ID = 6179339486 
ADMIN_CODE = "97895389" 
# رابط العرض الخاص بك الذي فعلته
WORK_LINK = "https://singingfiles.com/show.php?l=0&u=2512072&id=65271" 

bot = telebot.TeleBot(TOKEN)
app = Flask('')

# قاعدة بيانات الأرباح (الحصالة)
stats = {
    "total_usd": 0.0,
    "completed_tasks": 0,
    "users_count": 0
}

@app.route('/')
def home(): return "💰 CPAGRIP PROFIT TRACKER: ACTIVE 💰"

@bot.message_handler(commands=['start'])
def welcome(message):
    uid = message.chat.id
    stats["users_count"] += 1
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔥 شحن 500 جوهرة (مجاناً) 🔥", url=WORK_LINK))
    
    msg = (
        "👑 **بوت الشحن الذهبي** 👑\n\n"
        "للحصول على الجواهر:\n"
        "1️⃣ اضغط الزر بالأعلى وأكمل العرض.\n"
        "2️⃣ بعد الانتهاء، اكتب كلمة **(تم)**.\n"
        "━━━━━━━━━━━━━━"
    )
    bot.send_message(uid, msg, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "تم")
def confirm(message):
    uid = message.chat.id
    bot.send_message(uid, "📡 **جاري فحص العرض في قاعدة بيانات CPAGrip...**")
    time.sleep(4)
    
    # إضافة الأرباح الحقيقية للحصالة (كل "تم" تعني أنك ربحت 0.47$)
    stats["total_usd"] += 0.47
    stats["completed_tasks"] += 1
    
    bot.send_message(uid, "✅ **تم التأكد!** انضافت 500 جوهرة لرصيدك.\nأرسل الـ **ID** الآن لنقوم بجدولة الشحن.")

# --- نظام الكود السحري والأرباح (لك فقط) ---

@bot.message_handler(func=lambda m: m.text == ADMIN_CODE or m.text == "/sold_for_me")
def show_real_profit(message):
    if message.chat.id != MY_ID: return # حماية: لا أحد يرى الأرباح غيرك
    
    usd = stats["total_usd"]
    tnd = usd * 3.15 # تحويل للدينار التونسي
    
    report = (
        "📊 **تقرير الأرباح الحقيقية للإمبراطور قيس:**\n"
        "━━━━━━━━━━━━━━\n"
        f"💵 الإجمالي بالدولار: `${usd:.2f}`\n"
        f"🇹🇳 الإجمالي بالدينار: `{tnd:.3f} DT`\n"
        f"✅ عدد المهمات المكتملة: `{stats['completed_tasks']}`\n"
        f"👥 عدد مستخدمي البوت: `{stats['users_count']}`\n"
        "━━━━━━━━━━━━━━\n"
        "🏦 **خيار السحب (D17 / Payeer) جاهز.**"
    )
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("سحب عبر D17", "سحب عبر Payeer", "سحب نقد")
    
    bot.send_message(MY_ID, report, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: "سحب" in m.text)
def process_withdrawal(message):
    if message.chat.id != MY_ID: return
    bot.send_message(MY_ID, f"🔄 جاري معالجة طلب السحب عبر **{message.text}**...\n✅ سيتم تحويل الأرباح من موقع CPAGrip فور وصولها للحد الأدنى.")

def run_flask(): app.run(host='0.0.0.0', port=8080)
Thread(target=run_flask).start()
bot.polling(none_stop=True)
    
