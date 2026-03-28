import telebot
import time

# --- إعدادات الإمبراطور قيس ---
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"
MY_ID = 6179339486 
ADMIN_CODE = "97895389"
WORK_LINK = "https://singingfiles.com/show.php?l=0&u=2512072&id=65271"

bot = telebot.TeleBot(TOKEN)

# حصالة الأرباح
stats = {"total": 0.0, "leads": 0}

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔥 شحن 500 جوهرة (مجاناً) 🔥", url=WORK_LINK))
    bot.send_message(message.chat.id, "💎 **بوت الشحن الذهبي**\n\nاضغط الزر ونفذ المهمة، ثم اكتب (تم).", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "تم")
def confirmed(message):
    bot.send_message(message.chat.id, "📡 جاري الفحص في سيرفرات اللعبة...")
    time.sleep(3)
    stats["total"] += 0.47
    stats["leads"] += 1
    bot.send_message(message.chat.id, "✅ تم التأكد! أرسل الـ **ID** الخاص بك الآن لنقوم بالشحن.")

# --- 🚀 الإضافة الجديدة: إرسال الـ ID لك فوراً ---
@bot.message_handler(func=lambda m: m.text.isdigit() and len(m.text) > 5)
def handle_id(message):
    user_id_game = message.text
    # إرسال رسالة لك أنت (الأدمن)
    bot.send_message(MY_ID, f"📩 **وصلك ID جديد يا إمبراطور!**\n\nالـ ID المطلوب شحنه: `{user_id_game}`\nتأكد من حساب CPAGrip إذا اكتمل العرض.")
    # رد على المستخدم
    bot.reply_to(message, "✅ **تم استلام الـ ID بنجاح!**\nسيصلك الشحن خلال 12-24 ساعة بعد مراجعة العرض.")

# --- قسم كشف الأرباح بالتحويل التونسي ---
@bot.message_handler(func=lambda m: m.text in [ADMIN_CODE, "أرباحي"])
def show_money(message):
    if message.chat.id == MY_ID:
        usd = stats["total"]
        tnd = usd * 3.15
        msg = (
            "📊 **تقرير الأرباح يا قيس:**\n"
            f"💵 دولار: `${usd:.2f}`\n"
            f"🇹🇳 دينار تونسي: `{tnd:.3f} DT`\n"
            f"✅ عدد الأشخاص: `{stats['leads']}`"
        )
        bot.send_message(MY_ID, msg)

# تشغيل البوت
bot.infinity_polling()
    
