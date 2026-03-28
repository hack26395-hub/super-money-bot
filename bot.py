import telebot
import requests
import time
import random
from threading import Thread
from flask import Flask

# --- إعدادات الإمبراطورية ---
EMAIL = "Hack26395@gmail.com"
PASS = "kaissaya2006"
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"

bot = telebot.TeleBot(TOKEN)
app = Flask('')

# إحصائيات الاختراق
stats = {"watched": 0, "balance_usd": 0.0, "active": False}

@app.route('/')
def home(): 
    return "💀 RED SKULL SYSTEM: ONLINE & HACKING 💀"

# شعار الجمجمة الحمراء المرعب
SKULL_ART = """
```diff
- 🔴 SYSTEM HACKED 🔴
                ........                
            ..::::::::::::..            
          ..::::::::::::::::::..        
        ..::::::::::::::::::::::..      
       .::::::        ::::::        ::.     
      .:::::          ::::::          ::.   
     .:::::           ::::::           ::.  
     .:::::           ::::::           ::.  
     .:::::      ..::::::::::::..      ::.  
      .:::::    .::::::::::::::::.    ::.   
       .:::::: .::::::    ::::::. ::::::.   
        .::::::::::::::::::::::::::::::.    
          .::::::::::::::::::::::::::.      
            ..::::::::::::::::::::..        
               ..::::::::::::::..           
                   ..........      

                   def watch_engine(cookie):
headers = {
'Cookie': f'PHPSESSID={cookie}',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
'X-Requested-With': 'XMLHttpRequest'
}
while True:
try:
v_req = requests.get("https://www.google.com/search?q=https://payup.video/video/get", headers=headers, timeout=10).json()
if v_req.get('video_id'):
v_id = v_req['video_id']
time.sleep(random.randint(13, 17))
c_req = requests.get(f"https://www.google.com/search?q=https://payup.video/video/complete%3Fid%3D{v_id}", headers=headers, timeout=10)
if c_req.status_code == 200:
stats["watched"] += 1
stats["balance_usd"] += 0.00022
else:
time.sleep(20)
except:
time.sleep(10)
​@bot.message_handler(commands=['start'])
def start_hack(message):
bot.send_message(message.chat.id, SKULL_ART, parse_mode="MarkdownV2")
bot.send_message(message.chat.id, f"💀 بدء عملية التسلل والنهب...\n🎯 الهدف: payup.video\n📧 الحساب: {EMAIL}")
session = requests.Session()
try:
login_res = session.post("https://www.google.com/search?q=https://payup.video/login", data={'email': EMAIL, 'password': PASS}, timeout=15)
cookie = session.cookies.get_dict().get('PHPSESSID')
if cookie:
stats["active"] = True
bot.send_message(message.chat.id, "✅ تم اختراق الجلسة بنجاح!\n🚀 جيش الـ 20 خيط بدأ بجمع المال الآن.. ورا الشمس!")
for i in range(20):
t = Thread(target=watch_engine, args=(cookie,))
t.daemon = True
t.start()
else:
bot.send_message(message.chat.id, "❌ فشل الدخول! راجع بياناتك.")
except Exception as e:
bot.send_message(message.chat.id, f"❌ خطأ تقني: {e}")
​@bot.message_handler(commands=['sold'])
def check_status(message):
tnd = stats["balance_usd"] * 3.125
msg = (f"💀 إحصائيات الإمبراطورية:\n"
f"━━━━━━━━━━━━━━\n"
f"🎬 فيديوهات تم نهبها: {stats['watched']}\n"
f"💵 الربح الإجمالي: ${stats['balance_usd']:.5f}\n"
f"🇹🇳 بالدينار التونسي: {tnd:.3f} TND\n"
f"━━━━━━━━━━━━━━\n"
f"⚙️ الحالة: متصل بالخفاء 24/7")
markup = telebot.types.InlineKeyboardMarkup()
markup.add(telebot.types.InlineKeyboardButton("💸 سحب الأرباح إلى D17 / Payeer", callback_data="withdraw"))
bot.send_message(message.chat.id, msg, reply_markup=markup)
​@bot.callback_query_handler(func=lambda call: call.data == "withdraw")
def handle_withdraw(call):
bot.answer_callback_query(call.id)
bot.send_message(call.message.chat.id, "⚠️ تنبيه: الحد الأدنى للسحب هو 0.5$. استمر بالهجوم!")
​def run_flask():
app.run(host='0.0.0.0', port=8080)
​if name == "main":
Thread(target=run_flask).start()
bot.polling(none_stop=True)
