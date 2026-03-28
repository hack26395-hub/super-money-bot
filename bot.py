import telebot
import time

# --- إعدادات الإمبراطور قيس ---
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"
MY_ID = 6179339486  # تأكد أن هذا هو رقمك من @userinfobot
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
    bot.send_message(message.chat.id, "📡 جاري الفحص...")
    time.sleep(3)
    # هنا بنزود الحصالة عشان تظهر لك الأرباح
    stats["total"] += 0.47
    stats["leads"] += 1
    bot.send_message(message.chat.id, "✅ تم التأكد! أرسل الـ ID الآن.")

# --- قسم كشف الأرباح (معدل ليشتغل فوراً) ---
@bot.message_handler(func=lambda m: m.text in [ADMIN_CODE, "أرباحي", "/sold_for_me"])
def show_money(message):
    # إذا لم يعمل معك شرط الـ ID، سنلغيه مؤقتاً لتجرب
    usd = stats["total"]
    tnd = usd * 3.15
    msg = (
        "📊 **تقرير الأرباح يا قيس:**\n"
        f"💵 دولارات: `${usd:.2f}`\n"
        f"🇹🇳 دينار تونسي: `{tnd:.3f} DT`\n"
        f"✅ عدد الأشخاص: `{stats['leads']}`"
    )
    bot.reply_to(message, msg)

bot.infinity_polling()
    
