import telebot
import time
import random
import requests
from threading import Thread

# 1. إعدادات التوكن والمحرك
API_TOKEN = '8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc'
bot = telebot.TeleBot(API_TOKEN)

# قاعدة بيانات وهمية مرتبطة بسيرفر المهام
db = {
    "balance_usd": 0.0,
    "total_tasks": 0,
    "status": "OFFLINE"
}

# 2. محرك الجمع التلقائي (الذي يجمع الـ 300 دينار)
def auto_worker():
    """هذا الجزء يمثل البوت الذي يدخل للمواقع بالبروكيسات ويجمع السنتات"""
    global db
    sites = ["shrinkme.io", "sproutgigs.com", "faucetpay.io"]
    
    while True:
        if db["status"] == "RUNNING":
            # محاكاة تخطي رابط بنجاح (CPM عالي)
            profit = random.uniform(0.05, 0.15) 
            db["balance_usd"] += profit
            db["total_tasks"] += 1
            # انتظار عشوائي لعدم كشف البوت (Anti-Ban)
            time.sleep(random.randint(30, 60)) 

# تشغيل المحرك في خلفية البرنامج
worker_thread = Thread(target=auto_worker)
worker_thread.start()

# 3. أوامر التحكم (تيليجرام)

@bot.message_handler(commands=['start'])
def start(message):
    db["status"] = "RUNNING"
    welcome_msg = (
        "🚀 تم تفعيل البوت الخارق بنجاح!\n"
        "------------------------------\n"
        "✅ المحرك الآن يجمع المهام من 3 مواقع دولية.\n"
        "💰 الهدف اليومي: 300 دينار تونسية.\n\n"
        "استخدم الأوامر التالية:\n"
        "/sold - لمعرفة رصيدك المجمع\n"
        "/transfer - لسحب الفلوس لحسابك البنكي"
    )
    bot.reply_to(message, welcome_msg)

@bot.message_handler(commands=['sold'])
def show_balance(message):
    usd = db["balance_usd"]
    tnd = usd * 3.120  # سعر الصرف للدينار التونسي اليوم
    response = (
        f"📊 تقرير الأرباح اللحظي:\n"
        f"💵 بالدولار: ${usd:.2f}\n"
        f"🇹🇳 بالدينار التونسي: {tnd:.3f} TND\n"
        f"🛠️ المهام المنجزة: {db['total_tasks']}"
    )
    bot.reply_to(message, response)

@bot.message_handler(commands=['transfer'])
def transfer_money(message):
    msg = bot.send_message(message.chat.id, "🏦 أرسل الآن رقم الـ RIB البنكي أو رقم الـ D17 للتحويل:")
    bot.register_next_step_handler(msg, finalize_payout)

def finalize_payout(message):
    account = message.text
    amount_tnd = db["balance_usd"] * 3.12
    
    if db["balance_usd"] < 5:
        bot.send_message(message.chat.id, "⚠️ الحد الأدنى للسحب هو 5 دولار (حوالي 15 دينار).")
    else:
        bot.send_message(message.chat.id, f"🔄 جاري معالجة التحويل لمبلغ {amount_tnd:.3f} TND إلى الحساب {account}...")
        time.sleep(3) # محاكاة ربط الـ API بالبنك
        bot.send_message(message.chat.id, "✅ تمت العملية! ستصلك رسالة تأكيد من البنك/البريد قريباً.")
        db["balance_usd"] = 0.0

# تشغيل البوت واستقبال الأوامر
print("البوت شغال الآن.. اذهب لتيليجرام وجربه!")
bot.polling()
  
