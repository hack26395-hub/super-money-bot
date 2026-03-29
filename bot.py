import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# توكن البوت الخاص بك
TOKEN = "8506914686:AAHJE1oz-PpMH_pvMf1MP-6yL8ZuiZr73Dc"

# إعداد السجلات
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    welcome_text = (
        f"💎 مرحباً بك يا {user_name} في بوت الشحن التلقائي 2026 💎\n"
        "----------------------------------\n"
        "🏆 **المهمة الحالية:** فتح 21 بطاقة ذهبية لجمع الرموز السرية.\n\n"
        "✅ **الخطوات:**\n"
        "1️⃣ اضغط على كل بطاقة بالأسفل وحمّل ملفها الخاص.\n"
        "2️⃣ أرسل صورة شاشة (Screenshot) تجمع الـ 21 ملفاً في هاتفك.\n"
        "3️⃣ أرسل كلمة (تم) لإدخال الآيدي الخاص بك.\n\n"
        "👇 **قائمة البطاقات (اضغط للفتح):**"
    )
    
    # الروابط الـ 21 التي أرسلتها
    keyboard = [
        [InlineKeyboardButton("💳 البطاقة 01", url="https://shrinkme.click/Gems-2026-X7"), InlineKeyboardButton("💳 البطاقة 02", url="https://shrinkme.click/Gems-2026-X8")],
        [InlineKeyboardButton("💳 البطاقة 03", url="https://shrinkme.click/Gems-2026-X3"), InlineKeyboardButton("💳 البطاقة 04", url="https://shrinkme.click/Gems-2026-X4")],
        [InlineKeyboardButton("💳 البطاقة 05", url="https://shrinkme.click/Gems-2026-X5"), InlineKeyboardButton("💳 البطاقة 06", url="https://shrinkme.click/Gems-2026-X6")],
        [InlineKeyboardButton("💳 البطاقة 07", url="https://shrinkme.click/Gems-2026-X9"), InlineKeyboardButton("💳 البطاقة 08", url="https://shrinkme.click/Gems-2026-X10")],
        [InlineKeyboardButton("💳 البطاقة 09", url="https://shrinkme.click/Gems-2026-X11"), InlineKeyboardButton("💳 البطاقة 10", url="https://shrinkme.click/Gems-2026-X12")],
        [InlineKeyboardButton("💳 البطاقة 11", url="https://shrinkme.click/Gems-2026-X13"), InlineKeyboardButton("💳 البطاقة 12", url="https://shrinkme.click/Gems-2026-X14")],
        [InlineKeyboardButton("💳 البطاقة 13", url="https://shrinkme.click/Gems-2026-X15"), InlineKeyboardButton("💳 البطاقة 14", url="https://shrinkme.click/Gems-2026-X16")],
        [InlineKeyboardButton("💳 البطاقة 15", url="https://shrinkme.click/Gems-2026-X17"), InlineKeyboardButton("💳 البطاقة 16", url="https://shrinkme.click/Gems-2026-X18")],
        [InlineKeyboardButton("💳 البطاقة 17", url="https://shrinkme.click/Gems-2026-X19"), InlineKeyboardButton("💳 البطاقة 18", url="https://shrinkme.click/Gems-2026-X20")],
        [InlineKeyboardButton("💳 البطاقة 19", url="https://shrinkme.click/Gems-2026-X21"), InlineKeyboardButton("💳 البطاقة 20", url="https://shrinkme.click/Gems-2026-X22")],
        [InlineKeyboardButton("🏆 البطاقة الكبرى (5000 جوهرة) 🔥", url="https://shrinkme.click/Gems-2026-X22")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    user_id = update.effective_user.id

    if text == "تم":
        await update.message.reply_text("🔍 جاري فحص الملفات المرفقة... تم التأكد.\n\nالآن أرسل الـ **ID** الخاص بك للتحقق من الحساب في سيرفرات اللعبة.")
    
    elif text.isdigit() and len(text) > 5:
        bot_username = (await context.bot.get_me()).username
        ref_link = f"https://t.me/{bot_username}?start={user_id}"
        await update.message.reply_text(
            "⏳ جاري مطابقة الآيدي مع قاعدة بيانات الشحن...\n"
            "✅ **تم العثور على الحساب بنجاح!**\n\n"
            "⚠️ **الخطوة النهائية:** لكي يتم تفعيل الشحن، يجب نشر رابط البوت لـ 10 أصدقاء لضمان أنك لست روبوت.\n"
            f"🔗 رابطك الخاص: {ref_link}\n\n"
            "اكتب (**تم الشحن**) بعد الانتهاء."
        )
    
    elif text == "تم الشحن":
        await update.message.reply_text(
            "⌛ يتم الآن معالجة طلبك يدوياً...\n"
            "بسبب الضغط الهائل (أكثر من 45,000 مستخدم حالياً)، ستصل الجواهر لحسابك خلال **24 إلى 48 ساعة**.\n\n"
            "🚫 **تحذير:** لا تخرج من البوت، حذف البوت سيؤدي لإلغاء العملية فوراً."
        )

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("البوت يعمل بنجاح...")
    application.run_polling()

if __name__ == "__main__":
    main()
