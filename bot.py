import telebot
import requests
import time
from threading import Thread
from flask import Flask

# بياناتك
EMAIL = "Hack26395@gmail.com"
PASS = "kaissaya2006"
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"

bot = telebot.TeleBot(TOKEN)
app = Flask('')

# إحصائيات الجلسة
stats = {"total_watched": 0, "earned_now": 0.0, "start_time": time.time()}

@app.route('/')
def home(): return "💀 SYSTEM HACKED: PAYUP REVENUE BYPASS ACTIVE 💀"

# شعار الجمجمة المرعب
SKULL_ART = """
          ██████████████
      ████▒▒▒▒▒▒▒▒▒▒▒▒▒▒████
    ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
  ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
██▒▒▒▒████▒▒▒▒▒▒▒▒▒▒▒▒████▒▒▒▒██
██▒▒▒▒████▒▒▒▒▒▒▒▒▒▒▒▒████▒▒▒▒██
██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
  ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
    ██▒▒▒▒▒▒████████▒▒▒▒▒▒██
      ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
          ██  ██  ██  ██
           🔴 HACKED 🔴
"""

def watch_engine(cookie):
    headers = {'Cookie': f'PHPSESSID={cookie}', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    while True:
        try:
            v = requests.get("https://payup.video/video/get", headers=headers).json()
            if v.get('video_id'):
                time.sleep(12) 
                res = requests.get(f"https://payup.video/video/complete?id={v['video_id']}", headers=headers)
                if res.status_code == 200:
                    stats["total_watched"] += 1
                    stats["earned_now"] += 0.00021 # متوسط ربح الفيديو
        except: pass
        time.sleep(3)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f"```\n{SKULL_ART}\n```", parse_mode="Markdown")
    bot.send_message(message.chat.id, "💀 **نظام التسلل لـ Payup مفعل..**\n\nيتم الآن سحب البيانات من الحساب:\n`Hack26395@gmail.com`", parse_mode="Markdown")
    
    # محاكاة الاتصال
    session = requests.Session()
    login_res = session.post("https://payup.video/login", data={'email': EMAIL, 'password': PASS})
    cookie = session.cookies.get_dict().get('PHPSESSID')
    
    if cookie:
        for i in range(20): # 20 جيش شغالين سوا
            Thread(target=watch_engine, args=(cookie,)).start()
        bot.send_message(message.chat.id, "✅ **تم اختراق الجلسة! الجيش بدأ بجمع الدولارات الآن.**")
    else:
        bot.send_message(message.chat.id, "❌ فشل الدخول.. تأكد من البيانات.")

@bot.message_handler(commands=['sold'])
def show_balance(message):
    tnd = stats["earned_now"] * 3.120
    status_msg = (
        f"💀 **إحصائيات الاختراق الحالية:**\n"
        f"━━━━━━━━━━━━━━\n"
        f"🎬 فيديوهات تمت مشاهدتها: {stats['total_watched']}\n"
        f"💵 أرباح هذه الجلسة: ${stats['earned_now']:.5f}\n"
        f"🇹🇳 بالدينار التونسي: {tnd:.4f} TND\n"
        f"━━━━━━━━━━━━━━\n"
        f"🔥 قوة المعالجة: 20 Threads\n"
        f"🌐 الحالة: متصل بالسيرفر الروسي"
    )
    # إضافة زر للسحب
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("💸 تحويل الأموال (Withdraw)", callback_data="withdraw"))
    bot.send_message(message.chat.id, status_msg, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "withdraw")
def withdraw_request(call):
    bot.answer_callback_query(call.id, "🔄 جاري معالجة طلب السحب...")
    # هنا نقوم بمحاكاة طلب السحب للموقع
    bot.send_message(call.message.chat.id, "⚠️ **تنبيه:** الحد الأدنى للسحب هو 0.5$. رصيدك الحالي لم يكتمل بعد. استمر في التشغيل!")

Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
bot.polling()
        
